from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select
from starlette import status
from ..db import get_db
from ..models.user import User
from ..auth.passwords import verify_password
from ..auth.session import SESSION_USER_KEY

router = APIRouter(tags=["auth"])

@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
    if not user or not verify_password(password, user.password_hash) or not user.is_active:
        return request.app.state.templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"}, status_code=400)

    request.session[SESSION_USER_KEY] = user.id
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/logout")
def logout(request: Request):
    request.session.pop(SESSION_USER_KEY, None)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
