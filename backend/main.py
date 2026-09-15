import os
from urllib.parse import urlparse

import uvicorn
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    backend_url = os.environ.get("BACKEND_URL", "http://127.0.0.1:8000")
    parsed = urlparse(backend_url)
    uvicorn.run(
        "main:app",
        host=parsed.hostname or "127.0.0.1",
        port=parsed.port or 8000,
        reload=True,
        app_dir="src",
    )
