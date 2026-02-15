import uuid

import structlog

from intel_hub.config import get_settings
from intel_hub.db.repository import HubRepository
from intel_hub.pipeline.analyzer import AnalyzerPipeline
from intel_hub.pipeline.noise_filter import NoiseFilterPipeline
from intel_hub.services.alert_dispatcher import AlertDispatcher
from intel_hub.services.redis_streams import RedisStreams

logger = structlog.get_logger(__name__)


class ProcessingService:
    def __init__(self, repo: HubRepository, streams: RedisStreams):
        self.settings = get_settings()
        self.repo = repo
        self.streams = streams
        self.noise_filter = NoiseFilterPipeline(repo)
        self.analyzer = AnalyzerPipeline(repo)
        self.alert_dispatcher = AlertDispatcher()
        self.raw_last_id = "0-0"
        self.analyzed_last_id = "0-0"

    def process_raw_stream_once(self) -> int:
        consumed = 0
        entries = self.streams.read_stream(self.settings.redis_stream_raw, self.raw_last_id, count=100)
        for _, events in entries:
            for msg_id, payload in events:
                consumed += 1
                self.raw_last_id = msg_id
                try:
                    raw_item_id = uuid.UUID(payload["raw_item_id"])
                    result = self.noise_filter.run_for_raw_item(raw_item_id)
                    self.streams.publish_analyzed_item(
                        str(result["analyzed_id"]),
                        str(result["raw_item_id"]),
                        result["domain_id"],
                    )
                except Exception as exc:
                    logger.warning("noise_filter_failed", payload=payload, error=str(exc))
                    self.streams.publish_failed_job("noise_filter", payload)
        return consumed

    def process_analyzed_stream_once(self) -> int:
        consumed = 0
        entries = self.streams.read_stream(
            self.settings.redis_stream_analyzed,
            self.analyzed_last_id,
            count=100,
        )
        for _, events in entries:
            for msg_id, payload in events:
                consumed += 1
                self.analyzed_last_id = msg_id
                try:
                    analyzed_item_id = uuid.UUID(payload["analyzed_item_id"])
                    self.analyzer.run_for_analyzed_item(analyzed_item_id)
                    latest_items = self.repo.list_feed("all", limit=1, min_importance=1, cursor=None)
                    if latest_items:
                        subscribers = self.repo.list_subscribers()
                        self.alert_dispatcher.dispatch(latest_items[0], subscribers)
                except Exception as exc:
                    logger.warning("analyzer_failed", payload=payload, error=str(exc))
                    self.streams.publish_failed_job("analyzer", payload)
        return consumed
