# Homelab Notes + Tasks (monolith-first, modular boundaries)

This is a single FastAPI app that includes:
- Notes (CRUD + tags)
- Tasks (CRUD + due date + status + tags)
- Minimal server-rendered UI + JSON API
- Local auth (username/password) with session cookie

It is structured to allow swapping implementations later:
- storage/ (local -> S3/MinIO)
- search/ (simple -> Postgres FTS -> Meilisearch/OpenSearch)
- jobs/ (inline -> redis worker)
- auth/ (local -> OIDC later)

## Quick start (Docker Compose) — Level 2
1. Copy env:
   - `cp .env.example .env`
   - change `SECRET_KEY`

2. Start:
   - `docker compose up --build`

3. Run migrations (first time):
   - `docker compose exec app alembic upgrade head`

4. Create an initial user:
   - `docker compose exec app python -m homelab_app.cli create-user --username admin --password admin123`

5. Open:
   - UI: http://localhost:8000
   - API docs: http://localhost:8000/docs

## Local dev (venv)
- `python3 -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- set env (`export $(cat .env | xargs)` or use direnv)
- `alembic upgrade head`
- `uvicorn homelab_app.main:app --reload`
