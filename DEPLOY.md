# Deploy — ScamCheck KZ

**One Vercel project serves everything:** the static React frontend **and** the
FastAPI backend as a Python serverless function under `/api/*` (same origin — no
CORS, no separate server, no cold-start sleeping). If the function ever fails,
the frontend still analyzes in the browser via its built-in engine.

## Deploy to Vercel (~2 min)

1. Go to <https://vercel.com/new> → **Import** `abzaliito/antifraud_icore`.
2. **Root Directory = repo root** (leave as is). The root `vercel.json`:
   - builds the frontend (`cd frontend && npm install && npm run build` → `frontend/dist`),
   - serves `backend/app/main.py` as a Python function at `/api/*` (`api/index.py`).
3. **Deploy**. Done — one URL, e.g. `https://scamcheck-kz.vercel.app`.

**Do NOT set `VITE_API_BASE`** — the frontend calls same-origin `/api`, which the
serverless function handles.

### Verify after deploy
- `https://<proj>.vercel.app/` → the site, live scanner works
- `https://<proj>.vercel.app/api/v1/health` → `{"status":"healthy", ...}`
- `https://<proj>.vercel.app/api/docs` → Swagger UI (B2B bank API, schemes, etc.)

## How it fits together

```
Browser ──/              → frontend/dist (static, CDN)
        └─/api/v1/...     → api/index.py → backend/app/main.py (FastAPI, @vercel/python)
```

- `api/index.py` adds `backend/` to `sys.path` and re-exports the FastAPI `app`.
- `requirements.txt` (repo root) installs the function deps (fastapi, pydantic,
  python-multipart).
- `vercel.json` wires the build + routes `/api/*` to the function and other paths
  to the SPA.

> Note: OCR (screenshot) uses the built-in heuristic extractor on Vercel
> (tesseract isn't installed in the serverless runtime). Text analysis is full.

## Alternatives

- **Static only (no backend):** deploy just `frontend/` to any static host; the
  in-browser engine handles analysis. Simplest, zero servers.
- **Separate backend on Render:** a `render.yaml` blueprint is included; then set
  `VITE_API_BASE` in Vercel to the Render URL. (Free tier cold-starts ~30–50s.)

## Local run

```bash
# backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --port 8000         # Swagger: http://localhost:8000/api/docs

# frontend (proxies /api -> :8000)
cd frontend && npm install && npm run dev  # http://localhost:5173
```
