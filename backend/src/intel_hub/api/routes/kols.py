from fastapi import APIRouter, Depends, Query

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import KOLResponse

router = APIRouter(prefix="/kols", tags=["kols"])


@router.get("", response_model=list[KOLResponse])
def get_kols(domain: str = Query("all", pattern="^(all|crypto|ai_ml)$"), repo=Depends(get_repository_dep)):
    rows = repo.list_kols_all() if domain == "all" else repo.list_kols(domain)
    return [
        KOLResponse(
            domain_id=k.domain_id,
            twitter_username=k.twitter_username,
            display_name=k.display_name,
            credibility_score=float(k.credibility_score),
            follower_count=k.follower_count,
            is_active=k.is_active,
        )
        for k in rows
    ]
