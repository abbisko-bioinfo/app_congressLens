from fastapi import APIRouter

from app.api.health import router as health_router
from app.api.conferences import router as conferences_router
from app.api.sessions import router as sessions_router
from app.api.presentations import router as presentations_router
from app.api.interactions import router as interactions_router
from app.api.watchlist import router as watchlist_router
from app.api.importer import router as importer_router
from app.api.presentation_attachments import router as presentation_attachments_router
from app.api.attachments import router as attachments_router
from app.api.calendar import router as calendar_router
from app.api.ai import router as ai_router
from app.auth.routes import router as auth_router

api_router = APIRouter(prefix="/api")
api_router.include_router(health_router, tags=["health"])
api_router.include_router(conferences_router)
api_router.include_router(sessions_router)
api_router.include_router(presentations_router)
api_router.include_router(interactions_router)
api_router.include_router(watchlist_router)
api_router.include_router(importer_router)
api_router.include_router(presentation_attachments_router)
api_router.include_router(attachments_router)
api_router.include_router(calendar_router)
api_router.include_router(ai_router)
api_router.include_router(auth_router)