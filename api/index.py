"""
Vercel Python serverless entry point.
Exposes the existing FastAPI app (backend/app/main.py) so Vercel serves it
under /api/* in the same project as the static frontend — no separate backend.
Vercel's Python runtime serves the module-level ASGI `app`.
"""
import os
import sys

# Make the backend package importable (backend/app, backend/domain, ...).
_BACKEND = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if _BACKEND not in sys.path:
    sys.path.insert(0, _BACKEND)

from app.main import app  # noqa: E402  (re-exported for Vercel)

__all__ = ["app"]
