from decimal import Decimal

from sqlalchemy import select

from intel_hub.db.models import KOL, Domain

CRYPTO_KOLS = [
    ("colouredcoins", "Murat", "analyst", Decimal("0.92")),
    ("Pentosh1", "Pentoshi", "analyst", Decimal("0.91")),
    ("CryptoKaleo", "Kaleo", "trader", Decimal("0.89")),
    ("blknoiz06", "blcknoiz", "analyst", Decimal("0.86")),
    ("Ansem", "Ansem", "trader", Decimal("0.86")),
    ("Cryptoyieldinfo", "Cryptoyieldinfo", "analyst", Decimal("0.82")),
    ("Maboroshi_Yuki", "Maboroshi", "trader", Decimal("0.82")),
    ("inversebrah", "inversebrah", "trader", Decimal("0.80")),
    ("CryptoBullet1", "CryptoBullet", "analyst", Decimal("0.80")),
    ("WuBlockchain", "Wu Blockchain", "journalist", Decimal("0.90")),
    ("zachxbt", "zachxbt", "investigator", Decimal("0.95")),
    ("DefiIgnas", "DefiIgnas", "analyst", Decimal("0.84")),
]


def seed_crypto_data(db) -> None:
    domain = db.get(Domain, "crypto")
    if domain is None:
        domain = Domain(
            id="crypto",
            display_name="🪙 Crypto",
            description="Crypto intelligence domain",
            is_active=True,
            config={
                "topics": ["BTC", "ETH", "SOL", "SUI"],
                "categories": [
                    "price_action",
                    "regulation",
                    "partnership",
                    "technical",
                    "macro",
                    "airdrop",
                    "hack",
                    "other",
                ],
            },
        )
        db.add(domain)

    existing = {k.twitter_username for k in db.scalars(select(KOL).where(KOL.domain_id == "crypto"))}
    for username, display_name, category, credibility in CRYPTO_KOLS:
        if username in existing:
            continue
        db.add(
            KOL(
                domain_id="crypto",
                twitter_username=username,
                display_name=display_name,
                category=category,
                credibility_score=credibility,
            )
        )

    db.commit()
