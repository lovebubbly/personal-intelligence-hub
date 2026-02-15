"""initial schema

Revision ID: 0001_init
Revises:
Create Date: 2026-02-15
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "domains",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "kols",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain_id", sa.String(), nullable=False),
        sa.Column("twitter_username", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=True),
        sa.Column("follower_count", sa.Integer(), nullable=True),
        sa.Column("credibility_score", sa.Numeric(3, 2), nullable=False, server_default="0.50"),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("domain_id", "twitter_username", name="uq_kol_domain_username"),
    )

    op.create_table(
        "raw_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain_id", sa.String(), nullable=False),
        sa.Column("source_type", sa.String(), nullable=False),
        sa.Column("source_id", sa.String(), nullable=True),
        sa.Column("author", sa.String(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("url", sa.Text(), nullable=True),
        sa.Column("media_urls", sa.JSON(), nullable=True),
        sa.Column("raw_metadata", sa.JSON(), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("domain_id", "source_type", "source_id", name="uq_raw_domain_source"),
    )
    op.create_index("ix_raw_items_domain_collected", "raw_items", ["domain_id", "collected_at"], unique=False)

    op.create_table(
        "analyzed_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("raw_item_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain_id", sa.String(), nullable=False),
        sa.Column("is_signal", sa.Boolean(), nullable=False),
        sa.Column("noise_reason", sa.Text(), nullable=True),
        sa.Column("importance_score", sa.Integer(), nullable=True),
        sa.Column("sentiment_score", sa.Integer(), nullable=True),
        sa.Column("action_signal", sa.String(), nullable=False),
        sa.Column("context_summary", sa.Text(), nullable=True),
        sa.Column("related_topics", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("llm_model", sa.String(), nullable=True),
        sa.Column("analyzed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.CheckConstraint("importance_score BETWEEN 1 AND 10", name="chk_importance_score"),
        sa.CheckConstraint("sentiment_score BETWEEN -100 AND 100", name="chk_sentiment_score"),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"]),
        sa.ForeignKeyConstraint(["raw_item_id"], ["raw_items.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("raw_item_id", name="uq_analyzed_raw_item_id"),
    )
    op.create_index("ix_analyzed_domain_analyzed", "analyzed_items", ["domain_id", "analyzed_at"], unique=False)
    op.create_index(
        "ix_analyzed_importance_analyzed",
        "analyzed_items",
        ["importance_score", "analyzed_at"],
        unique=False,
    )

    op.create_table(
        "daily_digests",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("domain_id", sa.String(), nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("digest_date", sa.Date(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("detailed_analysis", sa.Text(), nullable=True),
        sa.Column("sentiment_avg", sa.Integer(), nullable=True),
        sa.Column("signal_count", sa.Integer(), nullable=True),
        sa.Column("top_events", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["domain_id"], ["domains.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("domain_id", "topic", "digest_date", name="uq_daily_digest_domain_topic_date"),
    )
    op.create_index("ix_daily_digests_domain_date", "daily_digests", ["domain_id", "digest_date"], unique=False)

    op.create_table(
        "cross_domain_links",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("source_item_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("target_item_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("link_type", sa.String(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("confidence", sa.Numeric(3, 2), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.ForeignKeyConstraint(["source_item_id"], ["analyzed_items.id"]),
        sa.ForeignKeyConstraint(["target_item_id"], ["analyzed_items.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "telegram_subscribers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("alert_level", sa.String(), nullable=False, server_default="high"),
        sa.Column("domain_filter", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("topic_filter", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.CheckConstraint("alert_level IN ('all', 'high', 'critical')", name="chk_alert_level"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("chat_id"),
    )

    op.create_table(
        "model_usage_daily",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("usage_date", sa.Date(), nullable=False),
        sa.Column("model", sa.String(), nullable=False),
        sa.Column("calls", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tokens_in", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("tokens_out", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cost_estimate", sa.Numeric(10, 4), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("usage_date", "model", name="uq_model_usage_daily"),
    )


def downgrade() -> None:
    op.drop_table("model_usage_daily")
    op.drop_table("telegram_subscribers")
    op.drop_table("cross_domain_links")
    op.drop_index("ix_daily_digests_domain_date", table_name="daily_digests")
    op.drop_table("daily_digests")
    op.drop_index("ix_analyzed_importance_analyzed", table_name="analyzed_items")
    op.drop_index("ix_analyzed_domain_analyzed", table_name="analyzed_items")
    op.drop_table("analyzed_items")
    op.drop_index("ix_raw_items_domain_collected", table_name="raw_items")
    op.drop_table("raw_items")
    op.drop_table("kols")
    op.drop_table("domains")
