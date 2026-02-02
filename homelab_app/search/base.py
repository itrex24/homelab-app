from abc import ABC, abstractmethod
from typing import Sequence

class Search(ABC):
    @abstractmethod
    def search_notes(self, *, user_id: int, q: str) -> Sequence[int]:
        raise NotImplementedError

    @abstractmethod
    def search_tasks(self, *, user_id: int, q: str) -> Sequence[int]:
        raise NotImplementedError
