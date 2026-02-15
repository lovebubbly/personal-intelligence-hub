import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    JSON,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from intel_hub.db.base import Base


class Domain(Base):
    __tablename__ = "domains"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    config: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class KOL(Base):
    __tablename__ = "kols"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(ForeignKey("domains.id"), nullable=False)
    twitter_username: Mapped[str] = mapped_column(String, nullable=False)
    display_name: Mapped[str | None] = mapped_column(String)
    follower_count: Mapped[int | None] = mapped_column(Integer)
    credibility_score: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=Decimal("0.50"))
    category: Mapped[str | None] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("domain_id", "twitter_username", name="uq_kol_domain_username"),)


class RawItem(Base):
    __tablename__ = "raw_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(ForeignKey("domains.id"), nullable=False)
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[str | None] = mapped_column(String)
    author: Mapped[str | None] = mapped_column(String)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str | None] = mapped_column(Text)
    media_urls: Mapped[dict | None] = mapped_column(JSON)
    raw_metadata: Mapped[dict | None] = mapped_column(JSON)
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("domain_id", "source_type", "source_id", name="uq_raw_domain_source"),
        Index("ix_raw_items_domain_collected", "domain_id", "collected_at"),
    )


class AnalyzedItem(Base):
    __tablename__ = "analyzed_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    raw_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("raw_items.id"), nullable=False)
    domain_id: Mapped[str] = mapped_column(ForeignKey("domains.id"), nullable=False)
    is_signal: Mapped[bool] = mapped_column(Boolean, nullable=False)
    noise_reason: Mapped[str | None] = mapped_column(Text)
    importance_score: Mapped[int | None] = mapped_column(Integer)
    sentiment_score: Mapped[int | None] = mapped_column(Integer)
    action_signal: Mapped[str] = mapped_column(String, nullable=False)
    context_summary: Mapped[str | None] = mapped_column(Text)
    related_topics: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    category: Mapped[str | None] = mapped_column(String)
    llm_model: Mapped[str | None] = mapped_column(String)
    analyzed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("importance_score BETWEEN 1 AND 10", name="chk_importance_score"),
        CheckConstraint("sentiment_score BETWEEN -100 AND 100", name="chk_sentiment_score"),
        UniqueConstraint("raw_item_id", name="uq_analyzed_raw_item_id"),
        Index("ix_analyzed_domain_analyzed", "domain_id", "analyzed_at"),
        Index("ix_analyzed_importance_analyzed", "importance_score", "analyzed_at"),
    )


class DailyDigest(Base):
    __tablename__ = "daily_digests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    domain_id: Mapped[str] = mapped_column(ForeignKey("domains.id"), nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    digest_date: Mapped[date] = mapped_column(Date, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    detailed_analysis: Mapped[str | None] = mapped_column(Text)
    sentiment_avg: Mapped[int | None] = mapped_column(Integer)
    signal_count: Mapped[int | None] = mapped_column(Integer)
    top_events: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("domain_id", "topic", "digest_date", name="uq_daily_digest_domain_topic_date"),
        Index("ix_daily_digests_domain_date", "domain_id", "digest_date"),
    )


class CrossDomainLink(Base):
    __tablename__ = "cross_domain_links"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyzed_items.id"), nullable=False)
    target_item_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("analyzed_items.id"), nullable=False)
    link_type: Mapped[str | None] = mapped_column(String)
    explanation: Mapped[str | None] = mapped_column(Text)
    confidence: Mapped[Decimal | None] = mapped_column(Numeric(3, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TelegramSubscriber(Base):
    __tablename__ = "telegram_subscribers"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String)
    alert_level: Mapped[str] = mapped_column(String, default="high", nullable=False)
    domain_filter: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    topic_filter: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("alert_level IN ('all', 'high', 'critical')", name="chk_alert_level"),
    )


class ModelUsageDaily(Base):
    __tablename__ = "model_usage_daily"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usage_date: Mapped[date] = mapped_column(Date, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    calls: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_in: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tokens_out: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_estimate: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False, default=Decimal("0"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("usage_date", "model", name="uq_model_usage_daily"),)
