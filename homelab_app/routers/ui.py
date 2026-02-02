from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from starlette import status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..auth.session import get_current_user
from ..models.note import Note
from ..models.task import Task, TaskStatus
from ..services.tags import parse_tag_csv, get_or_create_tags

router = APIRouter(tags=["ui"])

@router.get("/")
def home(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.execute(select(Note).where(Note.user_id == user.id).order_by(Note.updated_at.desc()).limit(20)).scalars().all()
    tasks = db.execute(select(Task).where(Task.user_id == user.id, Task.is_archived == False).order_by(Task.updated_at.desc()).limit(20)).scalars().all()
    return request.app.state.templates.TemplateResponse("home.html", {"request": request, "user": user, "notes": notes, "tasks": tasks})

# Notes UI
@router.get("/notes/new")
def notes_new(request: Request, user=Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse("note_edit.html", {"request": request, "user": user, "note": None, "tags_csv": ""})

@router.get("/notes/{note_id}")
def notes_edit(note_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.get(Note, note_id)
    if not note or note.user_id != user.id:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    tags_csv = ", ".join(t.name for t in note.tags)
    return request.app.state.templates.TemplateResponse("note_edit.html", {"request": request, "user": user, "note": note, "tags_csv": tags_csv})

@router.post("/notes/save")
def notes_save(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    note_id: str = Form(""),
    title: str = Form(...),
    body: str = Form(""),
    tags: str = Form(""),
):
    tag_names = parse_tag_csv(tags)
    if note_id:
        note = db.get(Note, int(note_id))
        if not note or note.user_id != user.id:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        note.title = title
        note.body = body
        note.tags = get_or_create_tags(db, tag_names)
    else:
        note = Note(user_id=user.id, title=title, body=body)
        note.tags = get_or_create_tags(db, tag_names)
        db.add(note)

    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/notes/{note_id}/delete")
def notes_delete(note_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.get(Note, note_id)
    if note and note.user_id == user.id:
        db.delete(note)
        db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

# Tasks UI
@router.get("/tasks/new")
def tasks_new(request: Request, user=Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse("task_edit.html", {"request": request, "user": user, "task": None, "tags_csv": "", "statuses": list(TaskStatus)})

@router.get("/tasks/{task_id}")
def tasks_edit(task_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task or task.user_id != user.id:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    tags_csv = ", ".join(t.name for t in task.tags)
    return request.app.state.templates.TemplateResponse("task_edit.html", {"request": request, "user": user, "task": task, "tags_csv": tags_csv, "statuses": list(TaskStatus)})

@router.post("/tasks/save")
def tasks_save(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    task_id: str = Form(""),
    title: str = Form(...),
    description: str = Form(""),
    status_value: str = Form("todo"),
    due_date: str = Form(""),
    tags: str = Form(""),
):
    from datetime import date

    tag_names = parse_tag_csv(tags)
    due = None
    if due_date.strip():
        due = date.fromisoformat(due_date.strip())

    if task_id:
        task = db.get(Task, int(task_id))
        if not task or task.user_id != user.id:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
        task.title = title
        task.description = description
        task.status = TaskStatus(status_value)
        task.due_date = due
        task.tags = get_or_create_tags(db, tag_names)
    else:
        task = Task(user_id=user.id, title=title, description=description, status=TaskStatus(status_value), due_date=due)
        task.tags = get_or_create_tags(db, tag_names)
        db.add(task)

    db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/tasks/{task_id}/delete")
def tasks_delete(task_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if task and task.user_id == user.id:
        db.delete(task)
        db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/tasks/{task_id}/archive")
def tasks_archive(task_id: int, request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if task and task.user_id == user.id:
        task.is_archived = True
        db.commit()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
