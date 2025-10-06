from typing import Callable, Tuple
from tenacity import retry, stop_after_attempt, wait_fixed

# Generic retry decorator for model calls
def with_retries(attempts: int = 2, wait_seconds: int = 1):
    def deco(fn: Callable):
        return retry(stop=stop_after_attempt(attempts), wait=wait_fixed(wait_seconds))(fn)
    return deco
