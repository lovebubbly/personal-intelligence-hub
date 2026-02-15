from datetime import date, datetime

from pydantic import BaseModel


class DomainResponse(BaseModel):
    id: str
    display_name: str
    is_active: bool
    topics: list[str]
    action_signals: dict


class FeedItemResponse(BaseModel):
    id: str
    domain_id: str
    source_type: str
    author: str | None
    content: str
    url: str | None
    collected_at: datetime
    is_signal: bool
    importance_score: int | None
    sentiment_score: int | None
    action_signal: str
    context_summary: str | None
    related_topics: list[str] | None
    category: str | None


class TopicIntelligenceResponse(BaseModel):
    topic: str
    signal_count_24h: int
    sentiment_avg: int
    top_items: list[dict]


class DigestTopicResponse(BaseModel):
    topic: str
    summary: str
    detailed_analysis: str | None
    sentiment_avg: int | None
    signal_count: int | None
    top_events: dict | list | None


class DigestResponse(BaseModel):
    domain_id: str
    digest_date: date
    topics: list[DigestTopicResponse]


class KOLResponse(BaseModel):
    domain_id: str
    twitter_username: str
    display_name: str | None
    credibility_score: float
    follower_count: int | None
    is_active: bool


class EventResponse(BaseModel):
    id: str
    domain_id: str
    title: str
    date: datetime
    kind: str
