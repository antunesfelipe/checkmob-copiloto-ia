from fastapi import FastAPI

app = FastAPI()

@app.get("/")
@app.head("/")
def read_root():
    return {"mensagem": "Copiloto Checkmob IA rodando com sucesso 🚀"}
