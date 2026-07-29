from fastapi import APIRouter

from app.comments.router import router as comments_router
from app.tickets.router import router as tickets_router
from app.users.router import router as users_router

api_router = APIRouter(prefix="/api")

api_router.include_router(users_router)
api_router.include_router(tickets_router)
api_router.include_router(comments_router)
