from fastapi import APIRouter, Depends, Path

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import TopicIntelligenceResponse

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("/{domain_id}", response_model=list[TopicIntelligenceResponse])
def get_topics(
    domain_id: str = Path(pattern="^(crypto|ai_ml)$"),
    repo=Depends(get_repository_dep),
):
    return [TopicIntelligenceResponse(**row) for row in repo.topic_stats(domain_id)]
