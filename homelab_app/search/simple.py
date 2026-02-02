from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from .base import Search
from ..models.note import Note
from ..models.task import Task

class SimpleLikeSearch(Search):
    def __init__(self, db: Session):
        self.db = db

    def search_notes(self, *, user_id: int, q: str) -> Sequence[int]:
        q = q.strip()
        if not q:
            return []
        rows = self.db.execute(
            select(Note.id).where(
                Note.user_id == user_id,
                or_(Note.title.ilike(f"%{q}%"), Note.body.ilike(f"%{q}%"))
            ).order_by(Note.updated_at.desc())
        ).all()
        return [r[0] for r in rows]

    def search_tasks(self, *, user_id: int, q: str) -> Sequence[int]:
        q = q.strip()
        if not q:
            return []
        rows = self.db.execute(
            select(Task.id).where(
                Task.user_id == user_id,
                or_(Task.title.ilike(f"%{q}%"), Task.description.ilike(f"%{q}%"))
            ).order_by(Task.updated_at.desc())
        ).all()
        return [r[0] for r in rows]
