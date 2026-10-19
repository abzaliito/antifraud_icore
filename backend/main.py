"""
Composition Root & Root Entrypoint for ScamCheck KZ API
Enables launching via either `uvicorn app.main:app` or `uvicorn main:app`.
"""

import sys
import os

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
