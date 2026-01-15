import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Configuration
DATA_PATH = "data"
MODEL_NAME = "llama3"  # Change this to your pulled model, e.g., "mistral", "llama2"
CHROMA_PATH = "chroma_db"

def main():
    print(f"Loading documents from {DATA_PATH}...")
    # 2. Load Documents
    loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    if not documents:
        print("No documents found in data/ directory.")
        return

    print(f"Loaded {len(documents)} documents.")

    # 3. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # 4. Initialize Embeddings & Vector Store
    print("Creating embeddings and vector store (this may take a moment)...")
    embeddings = OllamaEmbeddings(model=MODEL_NAME)
    
    # Create Chroma vector store from documents
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    # 5. Setup Retrieval
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 6. Setup LLM & Prompt
    llm = ChatOllama(model=MODEL_NAME)
    
    template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    # 7. Create Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 8. Run Query
    print("\n--- RAG System Ready ---")
    while True:
        query = input("\nAsk a question (or 'exit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            break
        
        print("\nThinking...")
        response = rag_chain.invoke(query)
        print(f"\nAnswer: {response}")

if __name__ == "__main__":
    main()
