# SOC 2 Control Tracker

A small dashboard for tracking the status of SOC 2 trust-service controls —
single sign-on, SAST, dependency scanning, vulnerability remediation, access
reviews, and more. Built after leading the engineering side of a SOC 2 audit
and wanting a lightweight way to see control status and audit-readiness at a
glance, instead of tracking it in a spreadsheet.

**Live demo:** <https://jaysingh10406.github.io/soc2-control-tracker/>

The deployed demo runs entirely client-side against bundled sample data —
no backend required, and changes reset on reload. To persist data, run the
FastAPI backend as described below.

## Stack

- **Backend:** FastAPI + SQLAlchemy + SQLite, fully tested with `pytest`
- **Frontend:** React + Vite, plain CSS (no framework dependency)

## Features

- Track controls by name, category (security / availability /
  confidentiality / processing integrity / privacy), owner, and status
- Update status inline (not started → in progress → implemented → verified)
- Add and remove controls
- Live summary stats, including an "audit-ready" percentage
- Filter by status

## Running locally

### Backend (real API)

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API comes up on `http://localhost:8000` with interactive docs at
`http://localhost:8000/docs`. It seeds itself with 13 realistic SOC 2 controls
on first run.

Run the test suite:

```bash
pytest tests/ -v
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

By default the frontend runs in **demo mode** — it works standalone against
bundled mock data with no backend needed, which is what makes it deployable
straight to GitHub Pages. To point it at the real FastAPI backend instead:

```bash
VITE_API_MODE=live VITE_API_URL=http://localhost:8000 npm run dev
```

## Deploying the frontend to GitHub Pages

```bash
cd frontend
npm run build
```

This produces a `dist/` folder ready to be served as a static site (demo
mode, bundled data) — publish it via GitHub Pages, e.g. with the
`gh-pages` package or a GitHub Actions workflow that deploys `dist/` on
push to `main`.

## Why this project

This isn't a toy CRUD app picked at random — it's a working model of the
exact controls I built and ran in-house while leading a company through a
SOC 2 audit with no prior compliance tooling in place: single sign-on, SAST
and dependency scanning wired into CI, and a defined vulnerability
remediation SLA.
