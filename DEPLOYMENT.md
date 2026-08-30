# 🚀 Deployment Guide

This guide walks you through deploying your projects to free platforms.

## Quick Start

### 1. Deploy Backend to Render (Free)

**soc2-control-tracker Backend:**
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select the `soc2-control-tracker` repository
5. Configure:
   - **Name:** `soc2-control-tracker-api`
   - **Environment:** Python
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
6. Click "Create Web Service"
7. Wait 2-3 minutes for deployment
8. Copy the URL (e.g., `https://soc2-control-tracker-api.onrender.com`)

**webhook-inspector Backend:**
- Repeat the same process for `webhook-inspector` repository

### 2. Deploy Frontend to Vercel (Free)

**soc2-control-tracker Frontend:**
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository (`soc2-control-tracker`)
4. Configure:
   - **Framework:** Vite
   - **Root Directory:** `frontend`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
5. Set Environment Variables:
   - **Key:** `VITE_API_URL`
   - **Value:** `https://soc2-control-tracker-api.onrender.com` (from step 1)
6. Click "Deploy"
7. Your site is now live at `https://your-project.vercel.app`

**webhook-inspector Frontend:**
- Repeat the same process for `webhook-inspector` repository

### 3. Update Backend CORS (Important!)

Your FastAPI backend needs to allow requests from your Vercel frontend.

Edit `backend/app/main.py` and add:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Push this change:
```bash
git add .
git commit -m "Enable CORS for production"
git push
```

Render will auto-redeploy when you push.

## Project Deployment Summary

| Project | Backend | Frontend | Status |
|---------|---------|----------|--------|
| **soc2-control-tracker** | Render | Vercel | Ready |
| **webhook-inspector** | Render | Vercel | Ready |
| **quotebuster** | N/A (CLI) | N/A | [See PyPI guide below] |
| **portfolio** | N/A | GitHub Pages | ✅ Live |

## Advanced: Deploy quotebuster to PyPI (Optional)

Make your CLI tool available via pip:

1. Create a PyPI account at https://pypi.org
2. Create `~/.pypirc` with your credentials
3. Build and publish:
```bash
cd quotebuster
python -m build
python -m twine upload dist/*
```

Users can then install with:
```bash
pip install quotebuster
```

## Troubleshooting

**Frontend shows 404 API errors?**
- Check backend URL in Vercel environment variables
- Ensure backend has CORS enabled
- Check backend health: `https://your-api.onrender.com/docs`

**Backend deployment fails?**
- Check logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `render.yaml` paths are correct

**Vercel build fails?**
- Check Node version (use Node 18+)
- Run `npm install` locally to verify no errors
- Check that root directory is correct

## Next Steps

1. Deploy backends to Render
2. Deploy frontends to Vercel
3. Test your live applications
4. Share your project URLs with others!

Need help? Check the platform docs:
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- PyPI: https://packaging.python.org
