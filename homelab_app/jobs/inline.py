from collections.abc import Callable
from .base import Jobs

class InlineJobs(Jobs):
    def enqueue(self, fn: Callable, *args, **kwargs) -> None:
        fn(*args, **kwargs)
