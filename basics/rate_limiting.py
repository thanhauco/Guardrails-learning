"""
Rate Limiting Guardrails
=======================

Simple in‑memory rate limiter to protect LLM calls from abuse.
"""

import time
from collections import defaultdict
from typing import Callable, Any

class RateLimiter:
    """Token‑bucket style rate limiter.
    
    * ``max_calls`` – maximum number of calls allowed in ``period`` seconds.
    * ``period`` – time window in seconds.
    """
    def __init__(self, max_calls: int = 10, period: int = 60):
        self.max_calls = max_calls
        self.period = period
        self.calls: defaultdict[str, list[float]] = defaultdict(list)

    def _prune(self, key: str, now: float) -> None:
        # Remove timestamps older than the period
        self.calls[key] = [t for t in self.calls[key] if now - t < self.period]

    def allow(self, key: str = "default") -> bool:
        now = time.time()
        self._prune(key, now)
        return len(self.calls[key]) < self.max_calls

    def record(self, key: str = "default") -> None:
        now = time.time()
        self._prune(key, now)
        self.calls[key].append(now)

    def limit(self, func: Callable) -> Callable:
        """Decorator that enforces the rate limit before calling ``func``.
        """
        def wrapper(*args, **kwargs):
            if not self.allow():
                raise RuntimeError("Rate limit exceeded")
            self.record()
            return func(*args, **kwargs)
        return wrapper

# Example usage
if __name__ == "__main__":
    limiter = RateLimiter(max_calls=5, period=10)
    @limiter.limit
    def dummy_call(x):
        return x * 2
    for i in range(7):
        try:
            print(dummy_call(i))
        except RuntimeError as e:
            print(e)
