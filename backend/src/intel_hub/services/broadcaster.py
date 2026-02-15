import asyncio
from datetime import UTC, datetime

import redis.asyncio as aioredis
import structlog

from intel_hub.api.websocket import sio
from intel_hub.config import get_settings
from intel_hub.db.repository import HubRepository
from intel_hub.db.session import SessionLocal

logger = structlog.get_logger(__name__)


class StreamBroadcaster:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.redis = aioredis.from_url(self.settings.redis_url, decode_responses=True)
        self.last_id = "$"
        self._running = True

    async def run(self) -> None:
        while self._running:
            try:
                stream_response = await self.redis.xread(
                    {self.settings.redis_stream_analyzed: self.last_id},
                    count=50,
                    block=1000,
                )
                if not stream_response:
                    await self._emit_heartbeat()
                    continue

                for _, events in stream_response:
                    for msg_id, payload in events:
                        self.last_id = msg_id
                        await self._emit_item(payload)
            except Exception as exc:
                logger.warning("broadcaster_error", error=str(exc))
                await asyncio.sleep(2)

    async def _emit_item(self, payload: dict) -> None:
        analyzed_item_id = payload.get("analyzed_item_id")
        if not analyzed_item_id:
            return
        with SessionLocal() as db:
            repo = HubRepository(db)
            item = repo.get_feed_item_by_analyzed_id(analyzed_item_id)
            if not item:
                return

        domain_id = item["domain_id"]
        await sio.emit("feed:item", item, room="domain:all", namespace=self.settings.socket_namespace)
        await sio.emit(
            "feed:item",
            item,
            room=f"domain:{domain_id}",
            namespace=self.settings.socket_namespace,
        )

    async def _emit_heartbeat(self) -> None:
        payload = {"ts": datetime.now(UTC).isoformat(), "lag_ms": 0}
        await sio.emit("feed:heartbeat", payload, room="domain:all", namespace=self.settings.socket_namespace)

    async def stop(self) -> None:
        self._running = False
        await self.redis.aclose()
