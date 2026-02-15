from datetime import UTC, datetime, timedelta

import structlog

from intel_hub.collectors.arxiv import ArxivCollector
from intel_hub.collectors.base import RawItemDTO
from intel_hub.collectors.github import GitHubCollector
from intel_hub.collectors.onchain import OnchainCollector
from intel_hub.collectors.rss import RSSCollector
from intel_hub.collectors.twitter import TwitterCollector
from intel_hub.db.repository import HubRepository
from intel_hub.domains.registry import get_domain_registry
from intel_hub.services.redis_streams import RedisStreams

logger = structlog.get_logger(__name__)


class CollectorService:
    def __init__(self, repo: HubRepository, streams: RedisStreams):
        self.repo = repo
        self.streams = streams
        self.registry = get_domain_registry()
        self.collector_map = {
            "TwitterCollector": TwitterCollector(),
            "RSSCollector": RSSCollector(),
            "OnchainCollector": OnchainCollector(),
            "ArxivCollector": ArxivCollector(),
            "GitHubCollector": GitHubCollector(),
        }

    def run_collectors(
        self,
        domain_id: str,
        collector_names: list[str] | None = None,
        since: datetime | None = None,
    ) -> dict:
        since_dt = since or datetime.now(UTC) - timedelta(minutes=5)
        inserted_count = 0
        domain_config = self.registry.get(domain_id)
        enabled_names = collector_names if collector_names is not None else domain_config.collectors
        collectors = [self.collector_map[name] for name in enabled_names if name in self.collector_map]

        for collector in collectors:
            try:
                items = collector.collect(domain_id, since_dt)
            except Exception as exc:
                logger.warning(
                    "collector_run_failed",
                    collector=collector.__class__.__name__,
                    domain=domain_id,
                    error=str(exc),
                )
                continue

            for item in items:
                try:
                    raw_id = self.repo.upsert_raw_item(self._to_db_payload(item))
                    self.streams.publish_raw_item(str(raw_id), domain_id)
                    inserted_count += 1
                except Exception as exc:
                    logger.warning(
                        "collector_item_upsert_failed",
                        collector=collector.__class__.__name__,
                        domain=domain_id,
                        source_id=item.source_id,
                        error=str(exc),
                    )

        return {"domain": domain_id, "inserted": inserted_count}

    @staticmethod
    def _to_db_payload(item: RawItemDTO) -> dict:
        return {
            "domain_id": item.domain_id,
            "source_type": item.source_type,
            "source_id": item.source_id,
            "author": item.author,
            "content": item.content,
            "url": item.url,
            "media_urls": item.media_urls,
            "raw_metadata": item.raw_metadata,
            "collected_at": item.collected_at,
        }
