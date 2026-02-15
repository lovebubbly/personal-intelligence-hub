from collections.abc import Generator

from sqlalchemy.orm import Session

from intel_hub.db.repository import HubRepository
from intel_hub.db.session import get_db_session


def get_repository(db: Session) -> HubRepository:
    return HubRepository(db)


def get_repository_dep() -> Generator[HubRepository, None, None]:
    for db in get_db_session():
        yield HubRepository(db)
