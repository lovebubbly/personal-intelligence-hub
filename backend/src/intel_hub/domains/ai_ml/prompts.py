AI_ML_NOISE_FILTER_PROMPT = """
You are an AI/ML intelligence filter. Classify this content as SIGNAL or NOISE.
SIGNAL = New model release, significant paper, useful tool/framework, important benchmark,
industry shift, practical technique.
NOISE = Hype without substance, rehashed news, vague predictions, self-promotion,
engagement farming, minor updates.

Content: {content}
Author: {author} (Credibility: {credibility_score})
Source: {source_type}

Output JSON with:
- is_signal: boolean
- noise_reason: string | null
- importance_score: integer (1-10)
- related_topics: string[] (e.g. ["LLM", "Agent"])
- category: one of model_release|paper|tool|framework|regulation|benchmark|dataset|open_source|other
- context_summary: Korean one sentence summary.
""".strip()

AI_ML_ANALYZER_PROMPT = """
이 AI/ML 콘텐츠를 심층 분석하라:
원문: {content}
작성자: {author} | 소스: {source_type}
관련 토픽: {related_topics}

분석:
1. 기술적 중요성 (혁신도, 기존 방법 대비 개선)
2. 실용적 적용 가능성 (바로 써먹을 수 있는지, 어떤 프로젝트에)
3. 센티먼트 스코어 (-100 ~ +100, 커뮤니티 반응 기반)
4. 액션 시그널: apply / learn / paradigm_shift / neutral
5. 관련 맥락: 경쟁 모델/도구와 비교, 트렌드 방향

Output JSON:
{ "sentiment_score": 0, "action_signal": "", "analysis": "2-3문장 한국어" }
""".strip()
