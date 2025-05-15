import os
import uvicorn
from health_app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 Iniciando Copiloto na porta {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
