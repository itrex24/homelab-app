from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional
from .models.task import TaskStatus

class TagOut(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = ""
    tags: List[str] = []

class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    body: Optional[str] = None
    tags: Optional[List[str]] = None

class NoteOut(BaseModel):
    id: int
    title: str
    body: str
    tags: List[TagOut] = []
    class Config:
        from_attributes = True

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = ""
    status: TaskStatus = TaskStatus.todo
    due_date: Optional[date] = None
    tags: List[str] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[date] = None
    tags: Optional[List[str]] = None
    is_archived: Optional[bool] = None

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    due_date: Optional[date] = None
    is_archived: bool
    tags: List[TagOut] = []
    class Config:
        from_attributes = True
