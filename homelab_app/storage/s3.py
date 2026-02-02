# Placeholder adapter for future MinIO/S3 support.
# Implement when you add attachments.
from typing import BinaryIO
from .base import Storage

class S3Storage(Storage):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError("S3Storage not implemented yet")

    def save(self, *, key: str, content: BinaryIO) -> str:
        raise NotImplementedError

    def open(self, *, key: str) -> BinaryIO:
        raise NotImplementedError

    def delete(self, *, key: str) -> None:
        raise NotImplementedError
