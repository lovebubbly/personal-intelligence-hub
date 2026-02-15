import socketio
import structlog

from intel_hub.config import get_settings

logger = structlog.get_logger(__name__)
settings = get_settings()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event(namespace=settings.socket_namespace)
async def connect(sid, environ):
    logger.info("socket_connected", sid=sid)


@sio.on("subscribe", namespace=settings.socket_namespace)
async def subscribe(sid, data):
    domains = data.get("domains", ["all"])
    for domain in domains:
        room = f"domain:{domain}"
        await sio.enter_room(sid, room, namespace=settings.socket_namespace)
    logger.info("socket_subscribed", sid=sid, domains=domains)


@sio.event(namespace=settings.socket_namespace)
async def disconnect(sid):
    logger.info("socket_disconnected", sid=sid)
