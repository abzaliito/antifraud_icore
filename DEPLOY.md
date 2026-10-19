# Deploy — ScamCheck KZ

Two parts: a static **frontend** (Vite/React) and a **backend** (FastAPI).
The frontend works on its own — if the backend is unreachable (or a free-tier
server is cold), it analyzes in the browser with a built-in port of the detector
(a 4s request timeout triggers the fallback). Connect the backend to serve the
real Python engine.

Recommended: **frontend → Vercel**, **backend → Render**.

## 1. Frontend → Vercel (~2 min)

1. Go to <https://vercel.com/new> → **Import** `abzaliito/antifraud_icore`.
2. Leave **Root Directory = repo root** — the root `vercel.json` builds `frontend/`
   and serves `frontend/dist`. (Or set Root Directory = `frontend`; both work.)
3. **Deploy** → public URL like `https://scamcheck-kz.vercel.app`.
4. After the backend is live (part 2), add env var **`VITE_API_BASE`** =
   your backend URL in **Settings → Environment Variables**, then **Redeploy**.

CLI alternative: `cd frontend && vercel --prod` (needs `vercel login`).

## 2. Backend → Render (~3 min, free)

The repo has a `render.yaml` blueprint.

1. Go to <https://dashboard.render.com> → **New → Blueprint**.
2. Connect this repo and **Apply** — it reads `render.yaml` and creates a
   Python web service:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health check: `/api/v1/health`
3. You get a URL like `https://scamcheck-kz-api.onrender.com`.
   Check it: open `.../api/v1/health` → `{"status":"healthy",...}`, docs at `/docs`.

Manual alternative (no blueprint): New → Web Service → Root Directory `backend`,
same build/start commands as above.

CORS is open (`allow_origins=["*"]`), so the Vercel frontend can call it cross-origin.

> Free tier sleeps when idle (first request cold ~30–50s). That's fine here: the
> frontend's 4s timeout falls back to the in-browser engine, so the demo never hangs.
> For a judged live demo with no cold starts, the static-only path is the safest.

## 3. Wire them together

In Vercel → the project → Settings → Environment Variables:

```
VITE_API_BASE = https://scamcheck-kz-api.onrender.com
```

Redeploy the frontend. Now the live demo uses the real backend; if it's cold or
down, it falls back locally automatically.

## Local run

```bash
# backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --port 8000

# frontend (proxies /api -> :8000)
cd frontend && npm install && npm run dev   # http://localhost:5173
```
