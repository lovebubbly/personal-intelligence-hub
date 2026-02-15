import uvicorn

from intel_hub.config import get_settings


def run_api() -> None:
    settings = get_settings()
    settings.validate_required()
    uvicorn.run(
        "intel_hub.api.main:socket_app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "local",
    )


if __name__ == "__main__":
    run_api()
