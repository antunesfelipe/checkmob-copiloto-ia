import os
import uvicorn
from onyx.main import app  # isso importa seu app correto

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
