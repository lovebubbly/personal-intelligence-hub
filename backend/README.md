# Intel Hub Backend

## Run

```bash
uv sync
uv run alembic upgrade head
uv run uvicorn intel_hub.api.main:socket_app --reload --host 0.0.0.0 --port 8000
```

Worker:

```bash
uv run python -m intel_hub.worker
```
