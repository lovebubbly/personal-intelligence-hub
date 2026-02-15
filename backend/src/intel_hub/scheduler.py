from datetime import UTC, datetime, timedelta
from zoneinfo import ZoneInfo

import structlog
from apscheduler.schedulers.background import BackgroundScheduler

from intel_hub.config import get_settings
from intel_hub.db.repository import HubRepository
from intel_hub.db.session import SessionLocal
from intel_hub.domains.registry import get_domain_registry
from intel_hub.pipeline.cross_domain import CrossDomainLinkPipeline
from intel_hub.pipeline.daily_digest import DailyDigestPipeline
from intel_hub.services.collector_service import CollectorService
from intel_hub.services.redis_streams import RedisStreams

logger = structlog.get_logger(__name__)


class WorkerScheduler:
    def __init__(self):
        self.settings = get_settings()
        self.registry = get_domain_registry()
        self.scheduler = BackgroundScheduler(timezone=ZoneInfo(self.settings.app_timezone))

    def start(self) -> None:
        self.scheduler.add_job(self.run_realtime_collectors, "interval", minutes=5, id="collectors_realtime")
        self.scheduler.add_job(self.run_ai_ml_github_collectors, "interval", hours=6, id="collectors_ai_ml_github")
        self.scheduler.add_job(
            self.run_ai_ml_arxiv_collectors,
            "cron",
            hour=self.settings.daily_digest_hour_kst,
            minute=0,
            id="collectors_ai_ml_arxiv",
        )
        self.scheduler.add_job(self.run_cross_domain, "interval", minutes=30, id="cross_domain")
        self.scheduler.add_job(
            self.run_digest,
            "cron",
            hour=self.settings.daily_digest_hour_kst,
            minute=0,
            id="daily_digest",
        )
        self.scheduler.start()

    def stop(self) -> None:
        self.scheduler.shutdown(wait=False)

    def run_realtime_collectors(self) -> None:
        with SessionLocal() as db:
            repo = HubRepository(db)
            streams = RedisStreams()
            collector_service = CollectorService(repo, streams)
            realtime_collectors_by_domain = {
                "crypto": ["TwitterCollector", "RSSCollector", "OnchainCollector"],
                "ai_ml": ["TwitterCollector", "RSSCollector"],
            }
            for domain in self.registry.list_active():
                collector_names = realtime_collectors_by_domain.get(domain.id, ["TwitterCollector", "RSSCollector"])
                result = collector_service.run_collectors(
                    domain.id,
                    collector_names=collector_names,
                    since=datetime.now(UTC) - timedelta(minutes=5),
                )
                logger.info("collectors_completed", **result)

    def run_ai_ml_github_collectors(self) -> None:
        with SessionLocal() as db:
            repo = HubRepository(db)
            streams = RedisStreams()
            collector_service = CollectorService(repo, streams)
            result = collector_service.run_collectors(
                "ai_ml",
                collector_names=["GitHubCollector"],
                since=datetime.now(UTC) - timedelta(hours=6),
            )
            logger.info("collectors_completed", cadence="6h", **result)

    def run_ai_ml_arxiv_collectors(self) -> None:
        with SessionLocal() as db:
            repo = HubRepository(db)
            streams = RedisStreams()
            collector_service = CollectorService(repo, streams)
            result = collector_service.run_collectors(
                "ai_ml",
                collector_names=["ArxivCollector"],
                since=datetime.now(UTC) - timedelta(days=1),
            )
            logger.info("collectors_completed", cadence="daily", **result)

    def run_digest(self) -> None:
        with SessionLocal() as db:
            repo = HubRepository(db)
            pipeline = DailyDigestPipeline(repo)
            for domain in self.registry.list_active():
                results = pipeline.run(domain.id)
                logger.info(
                    "daily_digest_completed",
                    domain=domain.id,
                    count=len(results),
                    executed_at=datetime.utcnow().isoformat(),
                )

    def run_cross_domain(self) -> None:
        with SessionLocal() as db:
            repo = HubRepository(db)
            pipeline = CrossDomainLinkPipeline(repo)
            count = pipeline.run(recent_minutes=30)
            logger.info("cross_domain_completed", count=count)
