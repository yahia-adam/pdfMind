# 2. Fonction de nettoyage optimisée pour le Français
import re
def clean_french_text(text):
    text = text.replace('\xa0', ' ').replace('\n', ' ')
    text = text.replace("’", "'").replace("‘", "'")
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def clean_documents(documents):
    cleaned_documents = []
    for doc in documents:
        doc.page_content = clean_french_text(doc.page_content)
        if len(doc.page_content) > 20:
            cleaned_documents.append(doc)
    return cleaned_documents
