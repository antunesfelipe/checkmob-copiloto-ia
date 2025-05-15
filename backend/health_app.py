from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensagem": "Copiloto Checkmob IA rodando com sucesso 🚀"}
