import os
from health_app import app
from threading import Thread

if __name__ == "__main__":
    # Só para manter compatibilidade com Render (mesmo se sem HTTP)
    port = int(os.environ.get("PORT", 10000))
    
    # Rodando FastAPI para manter porta aberta e evitar erro de "No open ports"
    import uvicorn
    Thread(target=lambda: uvicorn.run(app, host="0.0.0.0", port=port)).start()
