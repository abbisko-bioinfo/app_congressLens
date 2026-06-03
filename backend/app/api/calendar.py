import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.watchlist_item import WatchlistItem
from app.models.session import Session
from app.models.presentation import Presentation
from app.models.conference import Conference

router = APIRouter(prefix="/calendar", tags=["calendar"])


@router.get("/events")
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