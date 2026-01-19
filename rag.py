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
CHROMA_PATH = f"chroma_db/{MODEL_NAME}"

def initialize_rag():
    print("Creating embeddings and vector store (this may take a moment)...")
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    
    if os.path.exists(CHROMA_PATH):
        print("Loading existing vector store...")
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
    else:
        print(f"Loading documents from {DATA_PATH}...")
        # 2. Load Documents
        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyMuPDFLoader)
        documents = loader.load()
    
        if not documents:
            print("No documents found in data/ directory.")
            return None

        print(f"Loaded {len(documents)} documents.")

        for d in documents[:5]:
            print(d.page_content)
            print("*"*100)
        exit(0)

        print("Creating new vector store...")
        # 3. Split Text
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200, separators=["\n\n", "\n", " ", ""])
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks.")

        # Create Chroma vector store from documents
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_PATH
        )

    # 5. Setup Retrieval
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})

    # 6. Setup LLM & Prompt
    llm = ChatOllama(model=MODEL_NAME)
    
    template = """Repondez la question suivante en vous appuyant sur le contexte suivant:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    # 7. Create Chain
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

    return rag_chain

def main():
    rag_chain = initialize_rag()
    if rag_chain is None:
        return

    print("\n--- RAG System Ready ---")
    
    def chat_function(message, history):
        response = rag_chain.invoke(message)
        answer = response["answer"]
        context_docs = response["context"]
        
        print("**"*10)
        for doc in context_docs:
            print(doc.page_content)
            print("**"*10)

        sources = set()
        for doc in context_docs:
            if 'source' in doc.metadata:
                sources.add(os.path.basename(doc.metadata['source']))
        
        if sources:
            answer += "\n\n**Sources:**\n" + "\n".join(f"- {s}" for s in sources)
        return answer

    demo = gr.ChatInterface(
        fn=chat_function,
        title="QualiBot - Assistant Expert Qualibat",
        description="Assistant intelligent dédié à la Nomenclature officielle de QUALIBAT. Posez vos questions sur les qualifications, les codes techniques, les mentions RGE et les 9 familles de travaux.",
        examples=[
            "Quelles sont les activités de la Famille 5 ?",
            "C'est quoi la mention RGE ?",
            "Comment décrypter le code à 4 chiffres ?",
            "Quels travaux nécessitent une certification Amiante ?"
        ]
    )
    demo.launch()

if __name__ == "__main__":
    main()
