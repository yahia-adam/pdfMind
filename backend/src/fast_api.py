from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.build_rag import build_rag, rag_bot
from src.config import settings

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    if chat_model and retriever:
        question = "Quel est le code de qualification pour la maçonnerie ?"
        res = rag_bot(question, retriever, chat_model)
        return {"status_code": 200, "response": {"answer": res["answer"], "documents": res["documents"]}}
    else:
        return {"status_code": 500, "response": {"answer": "Chat model or retriever not initialized", "documents": []}}

@app.post("/ask")
def ask(request: QuestionRequest):
    if chat_model and retriever:
        res = rag_bot(request.question, retriever, chat_model)
        return {"status_code": 200, "response": {"answer": res["answer"], "documents": res["documents"]}}
    else:
        return {"status_code": 500, "response": {"answer": "Chat model or retriever not initialized", "documents": []}}
