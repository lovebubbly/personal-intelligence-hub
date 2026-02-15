import asyncio

import socketio
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from intel_hub.api.routes.digest import router as digest_router
from intel_hub.api.routes.domains import router as domains_router
from intel_hub.api.routes.events import router as events_router
from intel_hub.api.routes.feed import router as feed_router
from intel_hub.api.routes.kols import router as kols_router
from intel_hub.api.routes.topics import router as topics_router
from intel_hub.api.websocket import sio
from intel_hub.config import get_settings
from intel_hub.logging import configure_logging
from intel_hub.services.broadcaster import StreamBroadcaster

settings = get_settings()
configure_logging()

app = FastAPI(title=settings.app_name)

app.include_router(domains_router, prefix="/api/v1")
app.include_router(feed_router, prefix="/api/v1")
app.include_router(topics_router, prefix="/api/v1")
app.include_router(digest_router, prefix="/api/v1")
app.include_router(kols_router, prefix="/api/v1")
app.include_router(events_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event() -> None:
    settings.validate_required()
    app.state.broadcaster = StreamBroadcaster()
    app.state.broadcaster_task = asyncio.create_task(app.state.broadcaster.run())


@app.on_event("shutdown")
async def shutdown_event() -> None:
    if hasattr(app.state, "broadcaster"):
        await app.state.broadcaster.stop()
    if hasattr(app.state, "broadcaster_task"):
        app.state.broadcaster_task.cancel()


@app.get("/health/live")
def health_live() -> dict:
    return {"status": "ok"}


@app.get("/health/ready")
def health_ready() -> dict:
    return {"status": "ready"}


@app.get("/metrics")
def metrics() -> PlainTextResponse:
    return PlainTextResponse(generate_latest().decode("utf-8"), media_type=CONTENT_TYPE_LATEST)


socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
