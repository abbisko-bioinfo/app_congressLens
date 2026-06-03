import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.watchlist_item import WatchlistItem
from app.schemas.watchlist import WatchlistItemCreate, WatchlistItemRead

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


@router.get("", response_model=list[WatchlistItemRead])
async def list_watchlist(
    user_id: str | None = None,
    target_type: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(WatchlistItem).order_by(WatchlistItem.created_at.desc())
    if user_id:
        stmt = stmt.where(WatchlistItem.user_id == user_id)
    if target_type:
        stmt = stmt.where(WatchlistItem.target_type == target_type)
    result = await db.scalars(stmt)
    return result.all()


@router.post("", response_model=WatchlistItemRead, status_code=201)
async def add_watchlist_item(data: WatchlistItemCreate, db: AsyncSession = Depends(get_db)):
    obj = WatchlistItem(**data.model_dump())
    if data.target_id:
        obj.target_id = uuid.UUID(data.target_id)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{id}", status_code=204)
async def remove_watchlist_item(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(WatchlistItem, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Watchlist item not found")
    await db.delete(obj)
    await db.commit()