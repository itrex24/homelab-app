from typing import Iterable, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..models.tag import Tag

def normalize_tag_name(name: str) -> str:
    return name.strip().lower()

def parse_tag_csv(s: str) -> List[str]:
    if not s:
        return []
    parts = [p.strip() for p in s.split(",")]
    return [p for p in (normalize_tag_name(p) for p in parts) if p]

def get_or_create_tags(db: Session, tag_names: Iterable[str]) -> list[Tag]:
    names = sorted(set(normalize_tag_name(n) for n in tag_names if n and n.strip()))
    if not names:
        return []

    existing = db.execute(select(Tag).where(Tag.name.in_(names))).scalars().all()
    existing_map = {t.name: t for t in existing}

    out: list[Tag] = []
    for n in names:
        t = existing_map.get(n)
        if not t:
            t = Tag(name=n)
            db.add(t)
            db.flush()
        out.append(t)
    return out
