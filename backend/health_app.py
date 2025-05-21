from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
@app.head("/")
def read_root():
    return {"mensagem": "Copiloto Checkmob IA rodando com sucesso 🚀"}

class Pergunta(BaseModel):
    texto: str

@app.post("/pergunta")
async def responder(pergunta: Pergunta):
    texto = pergunta.texto
    # Aqui você pode conectar com OpenAI, LlamaIndex, etc.
    resposta = f"Recebi sua pergunta: '{texto}'. Em breve responderei com base nos documentos. 🤖"
    return {"resposta": resposta}
