from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse
from starlette import status
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import settings
from .observability.logging import setup_logging
from .routers import auth as auth_router
from .routers import api_notes, api_tasks, ui as ui_router


class RedirectUnauthedMiddleware:
    """
    Requires SessionMiddleware to already have populated scope['session'].
    Therefore SessionMiddleware must be OUTERMOST (added last).
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        path = scope.get("path", "")

        # Allow static + API + docs without auth
        if (
            path.startswith("/static")
            or path.startswith("/api")
            or path.startswith("/docs")
            or path.startswith("/openapi")
            or path in ("/login",)
        ):
            return await self.app(scope, receive, send)

        session = scope.get("session")  # set by SessionMiddleware
        if not session or session.get("user_id") is None:
            resp = RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
            return await resp(scope, receive, send)

        return await self.app(scope, receive, send)


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title=settings.APP_NAME)

    # Templates
    templates_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )

    class _Templates:
        def __init__(self, env):
            self.env = env

        def TemplateResponse(self, name: str, context: dict, status_code: int = 200):
            template = self.env.get_template(name)
            from starlette.responses import HTMLResponse
            return HTMLResponse(template.render(**context), status_code=status_code)

    app.state.templates = _Templates(env)

    # Static
    static_dir = Path(__file__).parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Routers
    app.include_router(auth_router.router)
    app.include_router(api_notes.router)
    app.include_router(api_tasks.router)
    app.include_router(ui_router.router)

    # Middleware order matters:
    # - RedirectUnauthedMiddleware must be INNER
    # - SessionMiddleware must be OUTER (added last)
    app.add_middleware(RedirectUnauthedMiddleware)
    app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY, https_only=False)

    @app.get("/health")
    def health():
        return {"ok": True, "env": settings.APP_ENV}

    return app


app = create_app()
