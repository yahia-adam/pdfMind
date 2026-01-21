import os
from fastapi import FastAPI
from src.pdf_mind.build_rag import build_rag, rag_bot
from src.pdf_mind.config import settings

app = FastAPI()

chat_model, retriever = build_rag(is_train=False, is_debug=settings.debug_mode)

@app.get("/")
def read_root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "endpoints": {
            "health": "/health",
            "ask": "/ask"
        }
    }

@app.get("/health")
def health_check():
    # test with "quel est la mission principale de QUALIBAT ?"
    if chat_model and retriever:
        question = "Quel est le code de qualification pour la maçonnerie ?"
        res = rag_bot(question, retriever, chat_model)
        return {"status": "ok", "question": question, "answer": res["answer"], "documents": res["documents"]}
    else:
        return {"status": "error", "message": "Chat model or retriever not initialized"}

@app.post("/ask")
def ask(question: str):
    if chat_model and retriever:
        res = rag_bot(question, retriever, chat_model)
        return {"status": "ok", "question": question, "answer": res["answer"], "documents": res["documents"]}
    else:
        return {"status": "error", "message": "Chat model or retriever not initialized"}
