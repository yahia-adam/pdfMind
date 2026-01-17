from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_pdf_by_size(documents, chunk_size=500, chunk_overlap=50):
    # 3. Split Text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No chunks found.")
    return chunks
