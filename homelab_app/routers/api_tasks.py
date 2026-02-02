from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import get_db
from ..auth.session import get_current_user
from ..models.task import Task
from ..schemas import TaskCreate, TaskUpdate, TaskOut
from ..services.tags import get_or_create_tags

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("", response_model=list[TaskOut])
def list_tasks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    tasks = db.execute(
        select(Task).where(Task.user_id == user.id, Task.is_archived == False).order_by(Task.updated_at.desc())
    ).scalars().all()
    return tasks

@router.post("", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = Task(
        user_id=user.id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        due_date=payload.due_date,
    )
    task.tags = get_or_create_tags(db, payload.tags)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "tags":
            task.tags = get_or_create_tags(db, value or [])
        else:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    task = db.get(Task, task_id)
    if not task or task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(task)
    db.commit()
    return {"ok": True}
