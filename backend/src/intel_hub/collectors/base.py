from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass(slots=True)
class RawItemDTO:
    domain_id: str
    source_type: str
    source_id: str
    author: str | None
    content: str
    url: str | None
    media_urls: dict | None = None
    raw_metadata: dict = field(default_factory=dict)
    collected_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class BaseCollector(ABC):
    source_type: str

    @abstractmethod
    def collect(self, domain_id: str, since: datetime | None = None) -> list[RawItemDTO]:
        raise NotImplementedError

    @abstractmethod
    def normalize(self, payload: dict, domain_id: str) -> RawItemDTO:
        raise NotImplementedError
