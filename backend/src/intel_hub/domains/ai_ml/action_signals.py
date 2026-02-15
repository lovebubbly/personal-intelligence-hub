from intel_hub.domains.base import ActionSignalDefinition

AI_ML_ACTION_SIGNALS = {
    "apply": ActionSignalDefinition(
        name="apply",
        icon="🟢",
        description="바로 적용 가능",
    ),
    "learn": ActionSignalDefinition(
        name="learn",
        icon="🟡",
        description="학습 필요",
    ),
    "paradigm_shift": ActionSignalDefinition(
        name="paradigm_shift",
        icon="🔴",
        description="전략 재검토 필요",
    ),
    "neutral": ActionSignalDefinition(
        name="neutral",
        icon="⚪",
        description="정보성",
    ),
}
