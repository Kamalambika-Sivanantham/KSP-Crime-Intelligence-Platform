# KSP Crime Intelligence & Analytics Platform

An enterprise crime intelligence platform for Karnataka State Police: crime records
management, GIS mapping, suspect network analysis, and ML-driven hotspot/risk
prediction.

This repository is being built **incrementally, in real working phases** rather
than as one monolithic generation. See [Project Status](#project-status) below
for exactly what's implemented vs. planned.

## Tech Stack

- **Frontend:** React 19, Vite, TypeScript, Tailwind CSS, Redux Toolkit, React Query,
  React Hook Form + Zod, Leaflet, Recharts, Cytoscape.js
- **Backend:** FastAPI, SQLAlchemy 2.0, Alembic, PostgreSQL + PostGIS, Redis, Celery
- **ML:** scikit-learn (DBSCAN hotspots, Gradient Boosting risk score), NetworkX
  (community detection, centrality, shortest path)
- **Infra:** Docker Compose, NGINX reverse proxy, MinIO (object storage), GitHub Actions CI

## Quick Start

```bash
git clone <this-repo>
cd ksp-platform
cp backend/.env.example backend/.env   # already done in this scaffold — edit SECRET_KEY before real use
docker compose up --build
```

- App (via NGINX gateway): http://localhost
- Frontend directly: http://localhost:5173
- Backend API docs (Swagger): http://localhost:8000/api/docs
- MinIO console: http://localhost:9001

The backend container seeds demo data on first boot: 5 districts, 15 police
stations, 7 demo users (one per role), 300 sample crime records, and sample
network-graph edges.

**Demo login (any role):** e.g. `admin@ksp.gov.in` / `Passw0rd!123`
(see `backend/scripts/seed.py` for all seeded accounts).

## Generating the first database migration

This scaffold bootstraps tables via `Base.metadata.create_all()` in the seed
script for fast local iteration. Before deploying anywhere real, generate a
proper Alembic migration against a live Postgres instance:

```bash
cd backend
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```

## Running tests

```bash
cd backend
pip install -r requirements.txt pytest httpx
pytest -v
```

## Project Status

### ✅ Phase 1 — Implemented now (real, functional code)
- JWT auth (access + refresh tokens), 7-role RBAC, login history, audit log tables
- Crime CRUD API + Crime List/Form/Detail pages
- Districts & police stations reference data
- Dashboard summary API + charts (trend, category breakdown, top districts)
- GIS Crime Map (Leaflet) with live hotspot overlay
- Hotspot detection (DBSCAN over haversine distance)
- Risk scoring model (Gradient Boosting, with heuristic fallback until trained)
- Crime Network Analysis (NetworkX: betweenness/pagerank centrality, greedy
  modularity community detection, shortest path) + Cytoscape.js graph UI
- Docker Compose stack: Postgres+PostGIS, Redis, MinIO, Celery worker, NGINX gateway
- GitHub Actions CI (backend tests, frontend build, Docker image builds)
- Seed data generator

### 🚧 Phase 2 — Planned next
- Repeat Offender Intelligence module (suspect profile, timeline, MO history)
- Predictive Intelligence (Prophet/XGBoost forecasting, SHAP explainability)
- Sociological Dashboard (socioeconomic overlay + correlation analysis)
- Anomaly Detection (Isolation Forest / Local Outlier Factor)
- Intelligence Reports (PDF/Excel/PowerPoint generation, scheduled reports)
- Notification Center (email/SMS/push, wired through the Celery worker already
  scaffolded in `app/services/tasks.py`)
- Natural-language AI Assistant (LLM-backed query interface)
- File upload pipeline to MinIO (FIR/images/video/documents) with evidence chain-of-custody
- Full RBAC enforcement across every endpoint + row-level district scoping
- Production hardening: rate limiting, HTTPS/TLS termination, secrets management

## Repository Structure

```
backend/         FastAPI application, models, ML modules, Alembic, tests
frontend/        React + Vite + TypeScript SPA
database/        Postgres init SQL (extensions)
docker/          Root NGINX gateway config
.github/         CI workflow
docker-compose.yml
```

## Security Notes for Production

Before deploying beyond local dev:
- Replace `SECRET_KEY` in `backend/.env` with a long random value from a secrets manager
- Replace all seeded demo passwords
- Put the NGINX gateway behind TLS (Let's Encrypt / your org's cert)
- Review and tighten CORS origins in `backend/app/core/config.py`
- Enable MFA (`mfa_enabled` field already exists on the User model — TOTP flow not yet wired)
