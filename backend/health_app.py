# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# @app.head("/")
# def read_root():
#     return {"mensagem": "Copiloto Checkmob IA rodando com sucesso 🚀"}
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

@app.get("/")
def home():
    return {"mensagem": "Copiloto Checkmob IA rodando com sucesso 🚀"}

@app.post("/pergunta")
def responder(pergunta: Pergunta):
    return {"resposta": f"Você perguntou: {pergunta.pergunta}"}

