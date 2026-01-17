from langchain_community.document_loaders import DirectoryLoader, PDFMinerLoader

# 2. Load Documents
def load_pdf(data_path):
    loader = DirectoryLoader(data_path, glob="*.pdf", loader_cls=PDFMinerLoader)
    documents = loader.load()
    if not documents:
        raise ValueError("No documents found in data/ directory.")
    return documents
