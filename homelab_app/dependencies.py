from fastapi import Depends
from sqlalchemy.orm import Session
from .db import get_db
from .config import settings
from .storage.local import LocalFilesystemStorage
from .storage.base import Storage
from .jobs.inline import InlineJobs
from .jobs.base import Jobs
from .search.simple import SimpleLikeSearch
from .search.base import Search

def get_storage() -> Storage:
    # Only local is wired for now
    return LocalFilesystemStorage(settings.LOCAL_STORAGE_PATH)

def get_jobs() -> Jobs:
    return InlineJobs()

def get_search(db: Session = Depends(get_db)) -> Search:
    return SimpleLikeSearch(db)
