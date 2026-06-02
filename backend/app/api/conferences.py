import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.conference import Conference
from app.schemas.conference import ConferenceCreate, ConferenceList, ConferenceRead, ConferenceUpdate

router = APIRouter(prefix="/conferences", tags=["conferences"])


@router.get("", response_model=ConferenceList)
async def list_conferences(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    total = await db.scalar(select(func.count()).select_from(Conference))
    result = await db.scalars(select(Conference).offset(skip).limit(limit).order_by(Conference.year.desc(), Conference.acronym))
    return ConferenceList(items=result.all(), total=total or 0)


@router.post("", response_model=ConferenceRead, status_code=201)
async def create_conference(data: ConferenceCreate, db: AsyncSession = Depends(get_db)):
    obj = Conference(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{id}", response_model=ConferenceRead)
async def get_conference(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Conference, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Conference not found")
    return obj


@router.patch("/{id}", response_model=ConferenceRead)
async def update_conference(id: str, data: ConferenceUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Conference, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Conference not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj