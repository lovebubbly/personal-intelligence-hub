import uuid
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal

from sqlalchemy import and_, desc, func, or_, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from intel_hub.db.models import (
    KOL,
    AnalyzedItem,
    CrossDomainLink,
    DailyDigest,
    Domain,
    ModelUsageDaily,
    RawItem,
    TelegramSubscriber,
)


@dataclass
class FeedCursor:
    collected_at: datetime | None


class HubRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_domains(self) -> list[Domain]:
        return list(self.db.scalars(select(Domain).where(Domain.is_active.is_(True))))

    def list_kols(self, domain_id: str) -> list[KOL]:
        stmt = select(KOL).where(and_(KOL.domain_id == domain_id, KOL.is_active.is_(True)))
        return list(self.db.scalars(stmt))

    def list_kols_all(self) -> list[KOL]:
        stmt = select(KOL).where(KOL.is_active.is_(True)).order_by(KOL.domain_id, KOL.credibility_score.desc())
        return list(self.db.scalars(stmt))

    def upsert_raw_item(self, payload: dict) -> uuid.UUID:
        stmt = pg_insert(RawItem).values(**payload)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_raw_domain_source",
            set_={
                "author": stmt.excluded.author,
                "content": stmt.excluded.content,
                "url": stmt.excluded.url,
                "media_urls": stmt.excluded.media_urls,
                "raw_metadata": stmt.excluded.raw_metadata,
                "collected_at": stmt.excluded.collected_at,
            },
        ).returning(RawItem.id)
        raw_item_id = self.db.execute(stmt).scalar_one()
        self.db.commit()
        return raw_item_id

    def get_raw_item(self, raw_item_id: uuid.UUID) -> RawItem | None:
        return self.db.get(RawItem, raw_item_id)

    def upsert_analyzed_item(self, payload: dict) -> uuid.UUID:
        stmt = pg_insert(AnalyzedItem).values(**payload)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_analyzed_raw_item_id",
            set_={
                "is_signal": stmt.excluded.is_signal,
                "noise_reason": stmt.excluded.noise_reason,
                "importance_score": stmt.excluded.importance_score,
                "sentiment_score": stmt.excluded.sentiment_score,
                "action_signal": stmt.excluded.action_signal,
                "context_summary": stmt.excluded.context_summary,
                "related_topics": stmt.excluded.related_topics,
                "category": stmt.excluded.category,
                "llm_model": stmt.excluded.llm_model,
                "analyzed_at": stmt.excluded.analyzed_at,
            },
        ).returning(AnalyzedItem.id)
        analyzed_id = self.db.execute(stmt).scalar_one()
        self.db.commit()
        return analyzed_id

    def list_feed(
        self,
        domain: str,
        limit: int,
        min_importance: int,
        cursor: datetime | None,
    ) -> list[dict]:
        stmt = (
            select(
                RawItem.id,
                RawItem.domain_id,
                RawItem.source_type,
                RawItem.author,
                RawItem.content,
                RawItem.url,
                RawItem.collected_at,
                AnalyzedItem.is_signal,
                AnalyzedItem.importance_score,
                AnalyzedItem.sentiment_score,
                AnalyzedItem.action_signal,
                AnalyzedItem.context_summary,
                AnalyzedItem.related_topics,
                AnalyzedItem.category,
            )
            .join(AnalyzedItem, AnalyzedItem.raw_item_id == RawItem.id)
            .where(AnalyzedItem.importance_score >= min_importance)
        )
        if domain != "all":
            stmt = stmt.where(RawItem.domain_id == domain)
        if cursor is not None:
            stmt = stmt.where(RawItem.collected_at < cursor)

        stmt = stmt.order_by(desc(AnalyzedItem.importance_score), desc(RawItem.collected_at)).limit(limit)
        rows = self.db.execute(stmt).mappings().all()
        return [dict(row) for row in rows]

    def get_feed_item_by_analyzed_id(self, analyzed_item_id: str) -> dict | None:
        stmt = (
            select(
                RawItem.id,
                RawItem.domain_id,
                RawItem.source_type,
                RawItem.author,
                RawItem.content,
                RawItem.url,
                RawItem.collected_at,
                AnalyzedItem.is_signal,
                AnalyzedItem.importance_score,
                AnalyzedItem.sentiment_score,
                AnalyzedItem.action_signal,
                AnalyzedItem.context_summary,
                AnalyzedItem.related_topics,
                AnalyzedItem.category,
            )
            .join(AnalyzedItem, AnalyzedItem.raw_item_id == RawItem.id)
            .where(AnalyzedItem.id == analyzed_item_id)
        )
        row = self.db.execute(stmt).mappings().first()
        return dict(row) if row else None

    def topic_stats(self, domain_id: str) -> list[dict]:
        since = datetime.now(UTC) - timedelta(hours=24)

        topic_expr = func.unnest(AnalyzedItem.related_topics).label("topic")
        subq = (
            select(
                topic_expr,
                AnalyzedItem.id.label("analyzed_id"),
                AnalyzedItem.sentiment_score,
                AnalyzedItem.importance_score,
            )
            .where(
                and_(
                    AnalyzedItem.domain_id == domain_id,
                    AnalyzedItem.is_signal.is_(True),
                    AnalyzedItem.analyzed_at >= since,
                )
            )
            .subquery()
        )

        stmt = (
            select(
                subq.c.topic,
                func.count(subq.c.analyzed_id).label("signal_count_24h"),
                func.avg(subq.c.sentiment_score).label("sentiment_avg"),
            )
            .group_by(subq.c.topic)
            .order_by(desc("signal_count_24h"))
        )

        rows = self.db.execute(stmt).mappings().all()
        response: list[dict] = []
        for row in rows:
            top_items_stmt = (
                select(
                    RawItem.content,
                    RawItem.url,
                    AnalyzedItem.importance_score,
                    AnalyzedItem.action_signal,
                )
                .join(AnalyzedItem, AnalyzedItem.raw_item_id == RawItem.id)
                .where(
                    and_(
                        AnalyzedItem.domain_id == domain_id,
                        func.array_position(AnalyzedItem.related_topics, row["topic"]).is_not(None),
                    )
                )
                .order_by(desc(AnalyzedItem.importance_score), desc(RawItem.collected_at))
                .limit(3)
            )
            top_items = [dict(item) for item in self.db.execute(top_items_stmt).mappings().all()]
            response.append(
                {
                    "topic": row["topic"],
                    "signal_count_24h": int(row["signal_count_24h"]),
                    "sentiment_avg": int(row["sentiment_avg"] or 0),
                    "top_items": top_items,
                }
            )
        return response

    def list_digests(self, domain_id: str, digest_date: date) -> list[DailyDigest]:
        stmt = select(DailyDigest).where(
            and_(DailyDigest.domain_id == domain_id, DailyDigest.digest_date == digest_date)
        )
        return list(self.db.scalars(stmt))

    def upsert_digest(self, payload: dict) -> uuid.UUID:
        stmt = pg_insert(DailyDigest).values(**payload)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_daily_digest_domain_topic_date",
            set_={
                "summary": stmt.excluded.summary,
                "detailed_analysis": stmt.excluded.detailed_analysis,
                "sentiment_avg": stmt.excluded.sentiment_avg,
                "signal_count": stmt.excluded.signal_count,
                "top_events": stmt.excluded.top_events,
            },
        ).returning(DailyDigest.id)
        digest_id = self.db.execute(stmt).scalar_one()
        self.db.commit()
        return digest_id

    def upsert_subscriber(self, payload: dict) -> uuid.UUID:
        stmt = pg_insert(TelegramSubscriber).values(**payload)
        stmt = stmt.on_conflict_do_update(
            index_elements=[TelegramSubscriber.chat_id],
            set_={
                "username": stmt.excluded.username,
                "alert_level": stmt.excluded.alert_level,
                "domain_filter": stmt.excluded.domain_filter,
                "topic_filter": stmt.excluded.topic_filter,
                "is_active": stmt.excluded.is_active,
            },
        ).returning(TelegramSubscriber.id)
        subscriber_id = self.db.execute(stmt).scalar_one()
        self.db.commit()
        return subscriber_id

    def update_subscriber_filters(
        self,
        chat_id: int,
        alert_level: str | None = None,
        domain_filter: list[str] | None = None,
        topic_filter: list[str] | None = None,
    ) -> None:
        subscriber = self.db.scalar(select(TelegramSubscriber).where(TelegramSubscriber.chat_id == chat_id))
        if subscriber is None:
            return
        if alert_level is not None:
            subscriber.alert_level = alert_level
        if domain_filter is not None:
            subscriber.domain_filter = domain_filter
        if topic_filter is not None:
            subscriber.topic_filter = topic_filter
        self.db.commit()

    def list_subscribers(self) -> list[TelegramSubscriber]:
        stmt = select(TelegramSubscriber).where(TelegramSubscriber.is_active.is_(True))
        return list(self.db.scalars(stmt))

    def record_model_usage(
        self,
        usage_date: date,
        model: str,
        tokens_in: int,
        tokens_out: int,
        cost_estimate: Decimal,
    ) -> None:
        stmt = pg_insert(ModelUsageDaily).values(
            usage_date=usage_date,
            model=model,
            calls=1,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_estimate=cost_estimate,
        )
        stmt = stmt.on_conflict_do_update(
            constraint="uq_model_usage_daily",
            set_={
                "calls": ModelUsageDaily.calls + 1,
                "tokens_in": ModelUsageDaily.tokens_in + tokens_in,
                "tokens_out": ModelUsageDaily.tokens_out + tokens_out,
                "cost_estimate": ModelUsageDaily.cost_estimate + cost_estimate,
            },
        )
        self.db.execute(stmt)
        self.db.commit()

    def analyzed_items_for_digest(self, domain_id: str, start_dt: datetime, end_dt: datetime) -> list[dict]:
        stmt = (
            select(
                AnalyzedItem.related_topics,
                AnalyzedItem.sentiment_score,
                AnalyzedItem.action_signal,
                AnalyzedItem.importance_score,
                AnalyzedItem.context_summary,
                RawItem.content,
                RawItem.url,
                RawItem.author,
            )
            .join(RawItem, RawItem.id == AnalyzedItem.raw_item_id)
            .where(
                and_(
                    AnalyzedItem.domain_id == domain_id,
                    AnalyzedItem.analyzed_at >= start_dt,
                    AnalyzedItem.analyzed_at <= end_dt,
                    AnalyzedItem.is_signal.is_(True),
                )
            )
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]

    def top_analyzed_items(self, min_importance: int = 7, limit: int = 20) -> list[dict]:
        stmt = (
            select(
                AnalyzedItem.id.label("analyzed_item_id"),
                RawItem.domain_id,
                RawItem.source_type,
                RawItem.author,
                RawItem.content,
                RawItem.url,
                RawItem.collected_at,
                AnalyzedItem.importance_score,
                AnalyzedItem.action_signal,
                AnalyzedItem.related_topics,
                AnalyzedItem.context_summary,
                AnalyzedItem.category,
            )
            .join(AnalyzedItem, AnalyzedItem.raw_item_id == RawItem.id)
            .where(AnalyzedItem.importance_score >= min_importance)
            .order_by(desc(AnalyzedItem.importance_score), desc(RawItem.collected_at))
            .limit(limit)
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]

    def recent_signal_items(self, since: datetime) -> list[dict]:
        stmt = (
            select(
                AnalyzedItem.id.label("analyzed_item_id"),
                AnalyzedItem.domain_id,
                AnalyzedItem.related_topics,
                AnalyzedItem.importance_score,
                AnalyzedItem.action_signal,
                AnalyzedItem.context_summary,
                RawItem.content,
                RawItem.url,
                RawItem.author,
            )
            .join(RawItem, RawItem.id == AnalyzedItem.raw_item_id)
            .where(
                and_(
                    AnalyzedItem.is_signal.is_(True),
                    AnalyzedItem.analyzed_at >= since,
                )
            )
            .order_by(desc(AnalyzedItem.importance_score), desc(AnalyzedItem.analyzed_at))
            .limit(250)
        )
        return [dict(row) for row in self.db.execute(stmt).mappings().all()]

    def has_cross_domain_link(self, source_item_id: uuid.UUID, target_item_id: uuid.UUID) -> bool:
        stmt = select(CrossDomainLink.id).where(
            or_(
                and_(
                    CrossDomainLink.source_item_id == source_item_id,
                    CrossDomainLink.target_item_id == target_item_id,
                ),
                and_(
                    CrossDomainLink.source_item_id == target_item_id,
                    CrossDomainLink.target_item_id == source_item_id,
                ),
            )
        )
        return self.db.scalar(stmt) is not None

    def create_cross_domain_link(
        self,
        source_item_id: uuid.UUID,
        target_item_id: uuid.UUID,
        link_type: str,
        explanation: str,
        confidence: Decimal,
    ) -> uuid.UUID:
        link = CrossDomainLink(
            source_item_id=source_item_id,
            target_item_id=target_item_id,
            link_type=link_type,
            explanation=explanation,
            confidence=confidence,
        )
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link.id
