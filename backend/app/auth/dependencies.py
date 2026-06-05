"""FastAPI dependencies for authentication."""

import logging

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.core.config import settings
from app.core.database import get_db

logger = logging.getLogger(__name__)

SESSION_COOKIE_NAME = "session"


async def get_current_user(
    session: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """Returns the current User from session cookie, or None for anonymous."""
    if not session:
        return None

    try:
        from itsdangerous import URLSafeTimedSerializer

        serializer = URLSafeTimedSerializer(settings.secret_key)
        user_id = serializer.loads(session, max_age=86400 * 7)  # 7 days
    except Exception:
        return None

    user = await db.scalar(select(User).where(User.id == user_id, User.is_active.is_(True)))
    return user


async def get_admin_user(
    current_user: User | None = Depends(get_current_user),
) -> User:
    """Requires authenticated admin user. Raises 403 if not admin."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user


async def get_authenticated_user(
    current_user: User | None = Depends(get_current_user),
) -> User:
    """Requires any authenticated user. Raises 401 if anonymous."""
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return current_user
