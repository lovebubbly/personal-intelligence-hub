from fastapi import APIRouter, Depends

from intel_hub.api.deps import get_repository_dep
from intel_hub.api.schemas import DomainResponse
from intel_hub.domains.registry import get_domain_registry

router = APIRouter(prefix="/domains", tags=["domains"])


@router.get("", response_model=list[DomainResponse])
def list_domains(repo=Depends(get_repository_dep)):
    registry = get_domain_registry()
    domains = repo.list_domains()
    responses = []
    for domain in domains:
        cfg = registry.get(domain.id)
        responses.append(
            DomainResponse(
                id=domain.id,
                display_name=domain.display_name,
                is_active=domain.is_active,
                topics=cfg.topics,
                action_signals={
                    name: {"icon": signal.icon, "description": signal.description}
                    for name, signal in cfg.action_signals.items()
                },
            )
        )
    return responses
