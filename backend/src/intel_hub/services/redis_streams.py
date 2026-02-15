import json
from datetime import UTC, datetime

from redis import Redis

from intel_hub.config import get_settings


class RedisStreams:
    def __init__(self, redis_client: Redis | None = None):
        self.settings = get_settings()
        self.redis = redis_client or Redis.from_url(self.settings.redis_url, decode_responses=True)

    def publish_raw_item(self, raw_item_id: str, domain_id: str) -> str:
        payload = {
            "raw_item_id": raw_item_id,
            "domain_id": domain_id,
            "ts": datetime.now(UTC).isoformat(),
        }
        return self.redis.xadd(self.settings.redis_stream_raw, payload)

    def publish_analyzed_item(self, analyzed_item_id: str, raw_item_id: str, domain_id: str) -> str:
        payload = {
            "analyzed_item_id": analyzed_item_id,
            "raw_item_id": raw_item_id,
            "domain_id": domain_id,
            "ts": datetime.now(UTC).isoformat(),
        }
        return self.redis.xadd(self.settings.redis_stream_analyzed, payload)

    def publish_failed_job(self, job_name: str, payload: dict) -> str:
        body = {
            "job": job_name,
            "payload": json.dumps(payload, ensure_ascii=False),
            "ts": datetime.now(UTC).isoformat(),
        }
        return self.redis.xadd(self.settings.redis_stream_failed_jobs, body)

    def read_stream(self, stream_name: str, last_id: str = "0-0", count: int = 100):
        return self.redis.xread({stream_name: last_id}, count=count, block=1000)
