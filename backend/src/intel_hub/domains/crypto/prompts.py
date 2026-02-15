CRYPTO_NOISE_FILTER_PROMPT = """
You are a crypto intelligence filter. Classify this content as SIGNAL or NOISE.
SIGNAL = Actionable alpha, market-moving info, genuine analysis, important crypto updates.
NOISE = Shilling, paid promotion, vague sentiment ("bullish vibes"), memes, engagement farming.

Content: {content}
Author: {author} (Credibility: {credibility_score})
Source: {source_type}

Output JSON with:
- is_signal: boolean
- noise_reason: string | null
- importance_score: integer (1-10)
- related_topics: string[]
- category: one of price_action|regulation|partnership|technical|macro|airdrop|hack|other
- context_summary: Korean one sentence summary.
""".strip()

CRYPTO_ANALYZER_PROMPT = """
이 크립토 콘텐츠를 심층 분석하라:
원문: {content}
작성자: {author} | 소스: {source_type}
관련 코인: {related_topics}

분석:
1. 시장 영향 (단기/중기)
2. 센티먼트 스코어 (-100 ~ +100, 근거)
3. 액션 시그널: opportunity / watch / risk / neutral
4. 관련 맥락: 이전 유사 이벤트와 연결

Output JSON:
{ "sentiment_score": 0, "action_signal": "", "analysis": "2-3문장 한국어" }
""".strip()
