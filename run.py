import os
import uvicorn
import health_app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(health_app.app, host="0.0.0.0", port=port)
