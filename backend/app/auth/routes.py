"""Auth routes: login, logout, session check."""

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import SESSION_COOKIE_NAME, get_current_user
from app.auth.ldap import authenticate_ldap
from app.auth.models import User
from app.core.config import settings
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    password: str


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    display_name: str
    email: str | None = None
    is_admin: bool = False


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user: UserResponse | None = None


@router.post("/login")
async def login(
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> SessionResponse:
    """Authenticate via LDAP and set session cookie."""
    ldap_result = await authenticate_ldap(body.username, body.password)

    if ldap_result is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Find or create local user record
    user = await db.scalar(
        select(User).where(User.ldap_uid == ldap_result["ldap_uid"], User.is_active.is_(True))
    )

    if user is None:
        # Create new user from LDAP data
        is_admin = ldap_result["ldap_uid"] in settings.admin_users_list
        user = User(
            ldap_uid=ldap_result["ldap_uid"],
            display_name=ldap_result["display_name"],
            email=ldap_result.get("email"),
            is_admin=is_admin,
        )
        db.add(user)
        await db.flush()
    else:
        # Update display name / email from LDAP
        user.display_name = ldap_result["display_name"]
        if ldap_result.get("email"):
            user.email = ldap_result["email"]
        await db.flush()

    # Set session cookie
    from itsdangerous import URLSafeTimedSerializer

    serializer = URLSafeTimedSerializer(settings.secret_key)
    token = serializer.dumps(user.id)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        max_age=86400 * 7,  # 7 days
        httponly=True,
        samesite="lax",
        secure=False,  # Set True in production with HTTPS
    )

    return SessionResponse(
        user=UserResponse(
            id=user.id,
            display_name=user.display_name,
            email=user.email,
            is_admin=user.is_admin,
        )
    )


@router.post("/logout")
async def logout(response: Response) -> dict:
    """Clear session cookie."""
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"status": "ok"}


@router.get("/session")
async def session_check(
    current_user: User | None = Depends(get_current_user),
) -> SessionResponse:
    """Return current user info from session cookie."""
    if current_user is None:
        return SessionResponse(user=None)
    return SessionResponse(
        user=UserResponse(
            id=current_user.id,
            display_name=current_user.display_name,
            email=current_user.email,
            is_admin=current_user.is_admin,
        )
    )
