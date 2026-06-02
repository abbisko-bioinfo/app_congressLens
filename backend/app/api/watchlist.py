import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.watchlist_item import WatchlistItem
from app.models.session import Session
from app.models.presentation import Presentation
from app.models.conference import Conference
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


@router.get("/calendar/events")
async def calendar_events(
    user_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(WatchlistItem)
    if user_id:
        stmt = stmt.where(WatchlistItem.user_id == user_id)
    items = await db.scalars(stmt)
    events = []
    for item in items.all():
        event_data = {"watchlist_id": str(item.id), "target_type": item.target_type, "target_id": str(item.target_id)}
        if item.target_type == "conference":
            conf = await db.get(Conference, item.target_id)
            if conf:
                event_data.update({"title": conf.name, "start": str(conf.start_date), "end": str(conf.end_date)})
        elif item.target_type == "session":
            sess = await db.get(Session, item.target_id)
            if sess:
                event_data.update({"title": sess.title, "start": str(sess.start_time), "end": str(sess.end_time)})
        elif item.target_type == "presentation":
            pres = await db.get(Presentation, item.target_id)
            if pres:
                event_data.update({"title": pres.title, "start": str(pres.start_time), "end": str(pres.end_time)})
        events.append(event_data)
    return {"events": events}