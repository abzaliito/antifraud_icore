# Deploy — ScamCheck KZ

Two parts: a static **frontend** (Vite/React) and an optional **backend** (FastAPI).
The frontend works on its own — if no backend is reachable it analyzes in the
browser with a built-in port of the detector, so a static deploy is enough for a
live demo. Connect the backend when you want the real Python engine to serve results.

## 1. Frontend → Vercel (recommended, ~2 min)

Easiest path — no CLI:

1. Push this repo to GitHub (done: branch `feat/react-frontend-aimprove`).
2. Go to <https://vercel.com/new> → **Import** this repository.
3. Set **Root Directory** = `frontend` (Framework auto-detects as **Vite**).
4. (Optional) add env var `VITE_API_BASE` = your backend URL (see part 2).
5. **Deploy**. You get a public URL like `https://scamcheck-kz.vercel.app`.

CLI alternative (needs `npm i -g vercel` and `vercel login`):

```bash
cd frontend
vercel --prod
```

Any static host works too (Netlify, Cloudflare Pages, GitHub Pages):
`cd frontend && npm run build` → deploy the `dist/` folder.

## 2. Backend → Render / Railway (optional)

Deploys the FastAPI engine so the live demo uses real server-side analysis.

**Render** (<https://render.com> → New → Web Service → point at this repo):

- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  (a `backend/Procfile` already declares this)

CORS is open (`allow_origins=["*"]`), so the Vercel frontend can call it
cross-origin. After it's live, set `VITE_API_BASE` in Vercel to the backend URL
and redeploy the frontend.

> Note: free tiers sleep when idle (cold start ~30s). For a judged live demo the
> static-only path (built-in detector) avoids cold starts.

## Local run

```bash
# backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --port 8000

# frontend (proxies /api -> :8000)
cd frontend && npm install && npm run dev   # http://localhost:5173
```
