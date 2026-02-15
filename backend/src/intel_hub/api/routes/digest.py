from datetime import date

from fastapi import APIRouter, Depends, Query

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import DigestResponse, DigestTopicResponse

router = APIRouter(prefix="/digest", tags=["digest"])


@router.get("", response_model=DigestResponse)
def get_digest(
    domain: str = Query("crypto", pattern="^(crypto|ai_ml)$"),
    digest_date: date | None = Query(default=None),
    repo=Depends(get_repository_dep),
):
    if digest_date is None:
        digest_date = date.today()
    digests = repo.list_digests(domain, digest_date)
    topics = [
        DigestTopicResponse(
            topic=d.topic,
            summary=d.summary,
            detailed_analysis=d.detailed_analysis,
            sentiment_avg=d.sentiment_avg,
            signal_count=d.signal_count,
            top_events=d.top_events,
        )
        for d in digests
    ]
    return DigestResponse(domain_id=domain, digest_date=digest_date, topics=topics)
