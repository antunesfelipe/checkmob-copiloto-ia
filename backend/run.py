import os
import uvicorn

port = int(os.environ.get("PORT", 10000))  # <-- isso aqui é essencial na Render

if __name__ == "__main__":
    uvicorn.run("health_app:app", host="0.0.0.0", port=port)
