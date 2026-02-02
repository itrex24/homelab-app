import os
from typing import BinaryIO
from .base import Storage

class LocalFilesystemStorage(Storage):
    def __init__(self, base_path: str):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def _full_path(self, key: str) -> str:
        key = key.lstrip("/")
        return os.path.join(self.base_path, key)

    def save(self, *, key: str, content: BinaryIO) -> str:
        path = self._full_path(key)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(content.read())
        return key

    def open(self, *, key: str) -> BinaryIO:
        return open(self._full_path(key), "rb")

    def delete(self, *, key: str) -> None:
        path = self._full_path(key)
        if os.path.exists(path):
            os.remove(path)
