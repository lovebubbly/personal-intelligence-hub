# Personal Intelligence Hub (MVP)

AI 기반 멀티도메인 인텔리전스 대시보드 MVP.

## 구성

- Backend: FastAPI + SQLAlchemy + Redis Streams + APScheduler
- Frontend: Next.js 14 + Tailwind + Socket.IO + Framer Motion
- DB: PostgreSQL (local: docker-compose)

## 빠른 시작

```bash
docker compose up -d
cp .env.example .env
```

### Backend

```bash
cd backend
uv sync
uv run alembic upgrade head
uv run python -m intel_hub.db.seed
uv run uvicorn intel_hub.api.main:socket_app --reload --host 0.0.0.0 --port 8000
```

별도 터미널:

```bash
cd backend
uv run python -m intel_hub.worker
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

## Playwright 회귀

```bash
cd frontend
pnpm test:e2e:ux
pnpm test:e2e:notice
pnpm test:e2e:mobile
```
