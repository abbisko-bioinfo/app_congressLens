import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionList, SessionRead, SessionUpdate

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=SessionList)
async def list_sessions(
    conference_id: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Session).order_by(Session.start_time, Session.title)
    if conference_id:
        stmt = stmt.where(Session.conference_id == uuid.UUID(conference_id))
    total = await db.scalar(select(func.count()).select_from(stmt.subquery()))
    result = await db.scalars(stmt.offset(skip).limit(limit))
    return SessionList(items=result.all(), total=total or 0)


@router.post("", response_model=SessionRead, status_code=201)
async def create_session(data: SessionCreate, db: AsyncSession = Depends(get_db)):
    obj = Session(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{id}", response_model=SessionRead)
async def get_session(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Session, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Session not found")
    return obj


@router.patch("/{id}", response_model=SessionRead)
async def update_session(id: str, data: SessionUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Session, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Session not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj