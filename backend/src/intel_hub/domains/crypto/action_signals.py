from intel_hub.domains.base import ActionSignalDefinition

CRYPTO_ACTION_SIGNALS = {
    "opportunity": ActionSignalDefinition(
        name="opportunity",
        icon="🟢",
        description="매수/참여 기회",
    ),
    "watch": ActionSignalDefinition(
        name="watch",
        icon="🟡",
        description="주시 필요",
    ),
    "risk": ActionSignalDefinition(
        name="risk",
        icon="🔴",
        description="리스크 경고",
    ),
    "neutral": ActionSignalDefinition(
        name="neutral",
        icon="⚪",
        description="정보성",
    ),
}
