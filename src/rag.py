import os
from langchain_chroma import Chroma
from src.data.load_data import load_pdf
from src.data.chunk_data import chunk_pdf_by_size
from src.data.embedding import create_embedding
from src.data.db import create_db, load_db
from src.model.get_model import get_model, get_prompt, create_rag_chain

# 1. Configuration
DATA_PATH = "data"
MODEL_NAME = "llama3.2"
CHROMA_PATH = "chroma_db"

def initialize_rag_system():
    # 4. Initialize Embeddings (needed for both load and create)
    embeddings = create_embedding(MODEL_NAME)
    
    vector_store = None
    
    # Check if DB exists and is not empty
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        print(f"Loading existing vector store from {CHROMA_PATH}...")
        vector_store = load_db(CHROMA_PATH, embeddings)
    else:
        print(f"Creating new vector store from documents in {DATA_PATH}...")
        # 2. Load Documents
        documents = load_pdf(DATA_PATH)

        # 3. Split Text
        chunks = chunk_pdf_by_size(documents)

        # Create Chroma vector store from documents
        vector_store = create_db(chunks, embeddings, CHROMA_PATH)

    # 5. Setup Retrieval
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 6. Setup LLM & Prompt
    llm = get_model(MODEL_NAME)
    
    # 6.1 Setup Prompt
    prompt = get_prompt()

    # 7. Create Chain
    rag_chain = create_rag_chain(llm, prompt, retriever)
    return rag_chain

def main():
    rag_chain = initialize_rag_system()

    # 8. Run Query
    print("\n--- RAG System Ready ---")
    while True:
        query = input("\nAsk a question (or 'exit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            break
        
        print("\nThinking...")
        response = process_query(rag_chain, query)
        print(f"\nAnswer: {response}")

def process_query(rag_chain, query):
     return rag_chain.invoke(query)

if __name__ == "__main__":
    main()
