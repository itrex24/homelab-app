from abc import ABC, abstractmethod
from collections.abc import Callable

class Jobs(ABC):
    @abstractmethod
    def enqueue(self, fn: Callable, *args, **kwargs) -> None:
        raise NotImplementedError
