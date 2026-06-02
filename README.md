# CongressLens

Oncology conference presentation management system for AACR, ASCO, and ESMO.

## Quick Start

```bash
docker compose up -d
docker compose exec backend alembic upgrade head
```

Access:
- Frontend: http://localhost:5174
- Backend API: http://localhost:8001/docs (Swagger UI)
- MinIO Console: http://localhost:9011

## Development

### Backend

```bash
cd backend
uv venv && source .venv/bin/activate
uv pip install -e .
DATABASE_URL=postgresql+psycopg://congresslens:congresslens-password@localhost:5435/congresslens \
  uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Database Migrations

```bash
cd backend
DATABASE_URL=postgresql+psycopg://congresslens:congresslens-password@localhost:5435/congresslens \
  alembic upgrade head
```

### Import Presentations

```bash
curl -X POST "http://localhost:8001/api/import/conferences/{id}/presentations?source=asco&folder_path=/data/asco-2026"
curl -X POST "http://localhost:8001/api/import/conferences/{id}/presentations?source=aacr&folder_path=/data/aacr-2026"
```

### Tests

```bash
cd backend
PYTHONPATH=. DATABASE_URL=postgresql+psycopg://congresslens:congresslens-password@localhost:5435/congresslens_test pytest tests/ -v
```

## Tech Stack

- Backend: FastAPI + SQLAlchemy 2.0 async + Pydantic v2 + Alembic
- Frontend: React + TypeScript + Vite + TanStack Query + Tailwind CSS
- Database: PostgreSQL 16
- Object Storage: MinIO
- Queue: Redis + Celery
- Deployment: Docker Compose