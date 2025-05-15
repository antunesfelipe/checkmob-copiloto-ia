from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Running on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
