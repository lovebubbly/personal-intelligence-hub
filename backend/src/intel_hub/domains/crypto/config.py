from intel_hub.domains.base import BaseDomainConfig
from intel_hub.domains.crypto.action_signals import CRYPTO_ACTION_SIGNALS
from intel_hub.domains.crypto.kol_list import CRYPTO_KOL_LIST
from intel_hub.domains.crypto.prompts import CRYPTO_ANALYZER_PROMPT, CRYPTO_NOISE_FILTER_PROMPT

CRYPTO_DOMAIN_CONFIG = BaseDomainConfig(
    id="crypto",
    display_name="🪙 Crypto",
    description="Crypto market intelligence",
    kol_list=CRYPTO_KOL_LIST,
    rss_sources=[
        "https://www.coindesk.com/arc/outboundfeeds/rss/",
        "https://www.theblock.co/rss.xml",
        "https://decrypt.co/feed",
        "https://cointelegraph.com/rss",
    ],
    collectors=["TwitterCollector", "RSSCollector", "OnchainCollector"],
    noise_filter_prompt=CRYPTO_NOISE_FILTER_PROMPT,
    analyzer_prompt=CRYPTO_ANALYZER_PROMPT,
    action_signals=CRYPTO_ACTION_SIGNALS,
    categories=[
        "price_action",
        "regulation",
        "partnership",
        "technical",
        "macro",
        "airdrop",
        "hack",
        "other",
    ],
    topics=["BTC", "ETH", "SOL", "SUI", "ALT"],
)
