from decimal import Decimal

from sqlalchemy import select

from intel_hub.db.models import KOL, Domain

AI_ML_KOLS = [
    ("TestingCatalog", "TestingCatalog", "research", Decimal("0.93")),
    ("_akhaliq", "akhaliq", "curator", Decimal("0.91")),
    ("DrJimFan", "Jim Fan", "research", Decimal("0.90")),
    ("kaboroMatt", "Matt Kaboro", "engineer", Decimal("0.88")),
    ("swyx", "swyx", "analyst", Decimal("0.89")),
    ("AndrewYNg", "Andrew Ng", "educator", Decimal("0.95")),
    ("ylecun", "Yann LeCun", "research", Decimal("0.94")),
    ("hardmaru", "hardmaru", "research", Decimal("0.86")),
    ("huggingface", "Hugging Face", "organization", Decimal("0.93")),
    ("OpenAI", "OpenAI", "organization", Decimal("0.96")),
    ("AnthropicAI", "Anthropic", "organization", Decimal("0.95")),
]


def seed_ai_ml_data(db) -> None:
    domain = db.get(Domain, "ai_ml")
    if domain is None:
        domain = Domain(
            id="ai_ml",
            display_name="🤖 AI/ML",
            description="AI/ML intelligence domain",
            is_active=True,
            config={
                "topics": ["LLM", "Agent", "Vision", "Multimodal", "Safety", "Infra"],
                "categories": [
                    "model_release",
                    "paper",
                    "tool",
                    "framework",
                    "regulation",
                    "benchmark",
                    "dataset",
                    "open_source",
                    "other",
                ],
            },
        )
        db.add(domain)

    existing = {k.twitter_username for k in db.scalars(select(KOL).where(KOL.domain_id == "ai_ml"))}
    for username, display_name, category, credibility in AI_ML_KOLS:
        if username in existing:
            continue
        db.add(
            KOL(
                domain_id="ai_ml",
                twitter_username=username,
                display_name=display_name,
                category=category,
                credibility_score=credibility,
            )
        )

    db.commit()
