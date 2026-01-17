from langchain_ollama import OllamaEmbeddings

# 4. Initialize Embeddings
def create_embedding(model_name):
    embeddings = OllamaEmbeddings(model=model_name)
    if not embeddings:
        raise ValueError(f"Failed to create embeddings for model: {model_name}")
    return embeddings