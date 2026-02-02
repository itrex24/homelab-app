from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..auth.session import get_current_user
from ..models.note import Note
from ..schemas import NoteCreate, NoteUpdate, NoteOut
from ..services.tags import get_or_create_tags

router = APIRouter(prefix="/api/notes", tags=["notes"])

@router.get("", response_model=list[NoteOut])
def list_notes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.execute(select(Note).where(Note.user_id == user.id).order_by(Note.updated_at.desc())).scalars().all()
    return notes

@router.post("", response_model=NoteOut)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = Note(user_id=user.id, title=payload.title, body=payload.body)
    note.tags = get_or_create_tags(db, payload.tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return note

@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")

    if payload.title is not None:
        note.title = payload.title
    if payload.body is not None:
        note.body = payload.body
    if payload.tags is not None:
        note.tags = get_or_create_tags(db, payload.tags)

    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(note)
    db.commit()
    return {"ok": True}
