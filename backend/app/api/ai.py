import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.ai_summary import AISummary
from app.models.presentation import Presentation

router = APIRouter(tags=["ai"])


@router.get("/presentations/{id}/ai-summary")
async def get_ai_summary(id: str, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    summaries = await db.scalars(
        select(AISummary).where(AISummary.scope_type == "presentation", AISummary.scope_id == uuid.UUID(id))
    )
    items = summaries.all()
    if not items:
        return {"status": "none", "summaries": []}
    return {"status": items[0].status, "summaries": [{"id": str(s.id), "summary_type": s.summary_type, "content": s.content, "model_name": s.model_name, "status": s.status} for s in items]}


@router.post("/presentations/{id}/ai-summary/jobs", status_code=202)
async def create_ai_summary_job(id: str, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    summary = AISummary(
        scope_type="presentation",
        scope_id=uuid.UUID(id),
        summary_type="general",
        status="pending",
    )
    db.add(summary)
    await db.commit()
    await db.refresh(summary)
    return {"job_id": str(summary.id), "status": "pending"}