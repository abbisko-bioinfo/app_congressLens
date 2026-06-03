import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.presentation import Presentation
from app.models.presentation_author import PresentationAuthor
from app.models.watchlist_item import WatchlistItem
from app.schemas.presentation import PresentationCreate, PresentationList, PresentationRead, PresentationUpdate, AuthorRead

router = APIRouter(prefix="/presentations", tags=["presentations"])


@router.get("", response_model=PresentationList)
async def list_presentations(
    conference_id: str | None = None,
    session_id: str | None = None,
    query: str | None = None,
    presentation_type: str | None = None,
    has_attachment: bool | None = None,
    summary_status: str | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Presentation).order_by(Presentation.start_time, Presentation.title)
    if conference_id:
        stmt = stmt.where(Presentation.conference_id == uuid.UUID(conference_id))
    if session_id:
        stmt = stmt.where(Presentation.session_id == uuid.UUID(session_id))
    if query:
        stmt = stmt.where(
            or_(
                Presentation.title.ilike(f"%{query}%"),
                Presentation.abstract_text.ilike(f"%{query}%"),
                Presentation.presenter_name.ilike(f"%{query}%"),
                Presentation.first_author_name.ilike(f"%{query}%"),
            )
        )
    if presentation_type:
        stmt = stmt.where(Presentation.presentation_type == presentation_type)
    if summary_status:
        stmt = stmt.where(Presentation.summary_status == summary_status)
    total = await db.scalar(select(func.count()).select_from(stmt.subquery()))
    result = await db.scalars(stmt.offset(skip).limit(limit))
    return PresentationList(items=result.all(), total=total or 0)


@router.post("", response_model=PresentationRead, status_code=201)
async def create_presentation(data: PresentationCreate, db: AsyncSession = Depends(get_db)):
    obj = Presentation(**data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{id}", response_model=PresentationRead)
async def get_presentation(id: str, user_id: str | None = None, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Presentation, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Presentation not found")
    is_watched = False
    if user_id:
        watched = await db.scalar(
            select(WatchlistItem).where(
                WatchlistItem.user_id == user_id,
                WatchlistItem.target_type == "presentation",
                WatchlistItem.target_id == obj.id,
            )
        )
        is_watched = watched is not None
    response = PresentationRead.model_validate(obj)
    response.is_watched = is_watched
    return response


@router.patch("/{id}", response_model=PresentationRead)
async def update_presentation(id: str, data: PresentationUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Presentation, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Presentation not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{id}/authors", response_model=list[AuthorRead])
async def get_presentation_authors(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Presentation, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Presentation not found")
    result = await db.scalars(
        select(PresentationAuthor)
        .where(PresentationAuthor.presentation_id == uuid.UUID(id))
        .order_by(PresentationAuthor.author_order)
    )
    return result.all()