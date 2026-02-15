from collections.abc import Callable
from functools import wraps
from typing import Any

from tenacity import RetryError, retry, stop_after_attempt, wait_exponential


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, reset_seconds: int = 120) -> None:
        self.failure_threshold = failure_threshold
        self.reset_seconds = reset_seconds
        self.failures = 0
        self.last_failure_ts: float | None = None

    def allow(self, now_ts: float) -> bool:
        if self.last_failure_ts is None:
            return True
        if self.failures < self.failure_threshold:
            return True
        return now_ts - self.last_failure_ts >= self.reset_seconds

    def on_success(self) -> None:
        self.failures = 0
        self.last_failure_ts = None

    def on_failure(self, now_ts: float) -> None:
        self.failures += 1
        self.last_failure_ts = now_ts


def retry_external_call(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    @retry(wait=wait_exponential(multiplier=1, min=1, max=8), stop=stop_after_attempt(3), reraise=True)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return func(*args, **kwargs)

    return wrapper


def is_retry_exhausted(exc: Exception) -> bool:
    return isinstance(exc, RetryError)
