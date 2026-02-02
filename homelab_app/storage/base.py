from abc import ABC, abstractmethod
from typing import BinaryIO

class Storage(ABC):
    @abstractmethod
    def save(self, *, key: str, content: BinaryIO) -> str:
        """Save content under a key. Returns the key (or resolved path)."""
        raise NotImplementedError

    @abstractmethod
    def open(self, *, key: str) -> BinaryIO:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *, key: str) -> None:
        raise NotImplementedError
