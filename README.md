import os
import gradio as gr
from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
# 1. Configuration
DATA_PATH = "data"
MODEL_NAME = "mistral-nemo:latest"
CHROMA_PATH = f"/home/adam/Documents/adam/pdfMind/chroma_db/{MODEL_NAME}"
print("Creating embeddings and vector store (this may take a moment)...")
embeddings = OllamaEmbeddings(model=MODEL_NAME)
llm = ChatOllama(model=MODEL_NAME)
# 2. Load Documents
loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyMuPDFLoader)
documents = loader.load()
# 2. Fonction de nettoyage optimisée pour le Français
import re
def clean_french_text(text):
    text = text.replace('\xa0', ' ').replace('\n', ' ')
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text
cleaned_documents = []
for doc in documents:
    doc.page_content = clean_french_text(doc.page_content)
    if len(doc.page_content) > 20:
        cleaned_documents.append(doc)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " ", ""])
chunks = text_splitter.split_documents(cleaned_documents)
print(f"Split into {len(chunks)} chunks.")
# Create Chroma vector store from documents
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH
)
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
template = """
RÔLE :
Tu es un consultant expert en qualifications du bâtiment (Qualibat, RGE, Normes).
Ta mission est d'expliquer les documents techniques fournis de manière pédagogique, structurée et synthétique.

RÈGLES DE RÉDACTION (À SUIVRE IMPÉRATIVEMENT) :

1. STRUCTURE VISUELLE :
   - Commence toujours par une phrase d'introduction qui pose le contexte global.
   - Utilise des **titres de sections** clairs pour séparer les thématiques.
   - Utilise systématiquement des listes à puces (•) pour énumérer les détails.

2. PÉDAGOGIE ET DÉTAILS :
   - Si la question porte sur une **nomenclature ou un code** : Décortique la logique (ex: 1er chiffre = Famille). Donne un exemple concret (comme le code 2111 ou autre présent dans le contexte) pour illustrer.
   - Si la question porte sur des **règles/normes** : Cite précisément les références (ex: NF X 46-010) et les durées de validité.
   - Mets en **gras** les termes techniques importants, les chiffres clés et les concepts définis.

3. TON :
   - Professionnel, instructif et précis.
   - Ne dis jamais "D'après le contexte", intègre l'information comme une connaissance établie.

4. CONTRAINTE : Si la réponse n'est pas dans le contexte, dis "Je ne sais pas". N'invente rien.

CONTEXTE DOCUMENTAIRE :
{context}

---
QUESTION : 
{question}

RÉPONSE STRUCTURÉE :
"""
prompt = ChatPromptTemplate.from_template(template)
def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain = RunnableParallel(
    {"context": retriever, "question": RunnablePassthrough()}
).assign(answer=rag_chain_from_docs)

response = rag_chain.invoke("Quelles sont les 9 Famille d'activités ?")
answer = response["answer"]
context_docs = response["context"]
print(answer)
print("*"*100)

for doc in context_docs:
    print(doc.page_content)
    print("*"*100)
for dc in context_docs:
    print(f"{dc.page_content[:100]}\n{dc.metadata.get("page", "")}\n{"*"*100}")