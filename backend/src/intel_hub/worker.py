import time

import structlog

from intel_hub.config import get_settings
from intel_hub.db.repository import HubRepository
from intel_hub.db.session import SessionLocal
from intel_hub.logging import configure_logging
from intel_hub.scheduler import WorkerScheduler
from intel_hub.services.processing_service import ProcessingService
from intel_hub.services.redis_streams import RedisStreams

logger = structlog.get_logger(__name__)


def run_worker() -> None:
    configure_logging()
    settings = get_settings()
    settings.validate_required()

    scheduler = WorkerScheduler()
    scheduler.start()
    logger.info("worker_started")

    if settings.telegram_bot_token:
        # Bot polling can run in a separate process in production. For MVP it is optional.
        logger.info("telegram_bot_configured")

    with SessionLocal() as db:
        repo = HubRepository(db)
        streams = RedisStreams()
        processing = ProcessingService(repo, streams)

        try:
            while True:
                processing.process_raw_stream_once()
                processing.process_analyzed_stream_once()
                db.expire_all()
                time.sleep(2)
        except KeyboardInterrupt:
            logger.info("worker_shutdown")
        finally:
            scheduler.stop()


if __name__ == "__main__":
    run_worker()
