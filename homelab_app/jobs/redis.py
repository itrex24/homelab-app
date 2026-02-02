# Placeholder adapter for future Redis worker (RQ/Celery).
from collections.abc import Callable
from .base import Jobs

class RedisJobs(Jobs):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("RedisJobs not implemented yet")

    def enqueue(self, fn: Callable, *args, **kwargs) -> None:
        raise NotImplementedError
