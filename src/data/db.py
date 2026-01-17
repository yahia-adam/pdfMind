from langchain_chroma import Chroma

def create_db(chunks, embeddings, chroma_path):
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )
    return vector_store

def load_db(chroma_path, embedding_function):
    vector_store = Chroma(persist_directory=chroma_path, embedding_function=embedding_function)
    return vector_store