from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.comments.models import Comment  # noqa: F401 — register SQLAlchemy mapper
from app.core.config import settings
from app.tickets.models import Ticket  # noqa: F401 — register SQLAlchemy mapper
from app.users.models import User  # noqa: F401 — register SQLAlchemy mapper


def create_app() -> FastAPI:
    app = FastAPI(title="Support Ticket Management API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


app = create_app()
