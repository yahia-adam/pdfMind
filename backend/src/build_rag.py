import os
import shutil
import gradio as gr
import pandas as pd
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from langchain_chroma import Chroma
from typing_extensions import Annotated, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from src.config import settings

# 2. Evaluation
from langsmith import Client, wrappers, traceable
from openevals.llm import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT
from src.data_processing import clean_documents

@traceable()
def rag_bot(question: str, retriever: Chroma, llm: ChatOllama) -> dict:
   docs = retriever.invoke(question)
   
   context_parts = []
   for doc in docs:
       chunk_id = doc.metadata.get('id', 'inconnu')
       context_parts.append(f"--- DÉBUT CHUNK ID: {chunk_id} ---\n{doc.page_content}\n--- FIN CHUNK ID: {chunk_id} ---")
   
   docs_string = "\n\n".join(context_parts)

   instructions = f"""Tu es un consultant expert en qualifications du bâtiment (Qualibat, RGE, Normes).
Ta mission est d'expliquer les documents techniques fournis de manière pédagogique, structurée et synthétique.

RÈGLES DE RÉDACTION (À SUIVRE IMPÉRATIVEMENT) :

1. CITATIONS OBLIGATOIRES (RÈGLE D'OR) :
   - Pour chaque affirmation, fait technique ou chiffre, tu DOIS insérer l'ID du chunk correspondant entre crochets juste après l'information.
   - Exemple : "Le code 2111 correspond à la maçonnerie [45]."
   - Si une information provient de plusieurs chunks, liste les IDs : [12][14].
   - Ne crée jamais de citation si l'ID n'est pas explicitement dans le contexte fourni.

2. STRUCTURE VISUELLE :
   - Commence par une introduction globale.
   - Utilise des **titres de sections** (##).
   - Utilise des listes à puces (•).

3. PÉDAGOGIE :
   - Décortique la logique des codes (ex: 1er chiffre = Famille).
   - Mets en **gras** les termes techniques et chiffres clés.

4. TON ET CONTRAINTES :
   - Professionnel et précis.
   - Si la réponse n'est pas dans le contexte, dis "Je ne sais pas".

5. PÉRIMÈTRE STRICT DE COMPÉTENCE (RÈGLE BLOQUANTE) :

   - Tu es strictement limité aux sujets suivants :
    - Qualifications Qualibat
    - Dispositif RGE
    - Normes techniques du bâtiment
    - Codes métiers, référentiels officiels, exigences de qualification
    - Documents fournis dans le CONTEXTE DOCUMENTAIRE

   - Si une question sort de ce périmètre (ex : juridique général, fiscalité, gestion d’entreprise, RH, informatique, culture générale, etc.), tu DOIS répondre UNIQUEMENT par :
    "Cette question est hors de mon domaine de compétence."

   - Tu n’as pas le droit :
    - de reformuler la question
    - de donner une réponse partielle
    - de faire des suppositions
    - d’apporter un avis personnel

CONTEXTE DOCUMENTAIRE :
{docs_string}
"""

   ai_msg = llm.invoke([
           {"role": "system", "content": instructions},
           {"role": "user", "content": question},
       ],
   )
   
   return {"answer": ai_msg.content, "documents": docs}

def build_rag(is_train=False, is_debug=False):
    if settings.model_provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        embeddings = OpenAIEmbeddings(
            model=settings.embedding_model_name,
            api_key=settings.openai_api_key,
            openai_api_base=settings.openai_url
        )
    else:
        embeddings = OllamaEmbeddings(model=settings.embedding_model_name)
    
    if is_train:
        if (os.path.exists(settings.chroma_db_dir)):
            if is_debug:
                print("Removing existing vector store...")
            shutil.rmtree(settings.chroma_db_dir)

    if not os.path.exists(settings.chroma_db_dir):
        os.makedirs(settings.chroma_db_dir)
        
        if is_debug:
            print("Loading documents...")
        loader = DirectoryLoader(settings.train_data_dir, glob="*.pdf", loader_cls=PyMuPDFLoader)
        documents = loader.load()
        
        if is_debug:
            print("Cleaning documents...")
        documents = clean_documents(documents)

        if is_debug:
            print("Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " ", ""])
        chunks = text_splitter.split_documents(documents)
        for i, chunk in enumerate(chunks):
            chunk.metadata['id'] = i

        if is_debug:
            print("Creating vector store...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=settings.chroma_db_dir
        )
    else:
        if is_debug:
            print("Loading vector store...")
        vector_store = Chroma(persist_directory=settings.chroma_db_dir, embedding_function=embeddings)
    
    if is_debug:
        print("Creating retriever...")
    retriever = vector_store.as_retriever(type="similarity", search_kwargs={"k": 5})
    
    if is_debug:
        print("Creating chat model...")
        
    if settings.model_provider == "openai":
        from langchain_openai import ChatOpenAI
        chat_model = ChatOpenAI(
            model=settings.chat_model_name,
            api_key=settings.openai_api_key,
            openai_api_base=settings.openai_url
        )
    else:
        chat_model = ChatOllama(model=settings.chat_model_name)
    
    if is_debug:
        print("Chat model and retriever created successfully.")
    return chat_model, retriever

if __name__ == "__main__":
    chat_model, retriever = build_rag(is_train=False, is_debug=settings.debug_mode)

    print("test avec : Quelle est la mission principale de QUALIBAT ?")
    res = rag_bot("Quelle est la mission principale de QUALIBAT ?", retriever, chat_model)
    print(res)