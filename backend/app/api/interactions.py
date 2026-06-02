import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.comment import Comment
from app.models.annotation import Annotation
from app.models.presentation import Presentation
from app.schemas.interaction import (
    AnnotationCreate, AnnotationRead, AnnotationUpdate,
    CommentCreate, CommentRead, CommentUpdate,
)

router = APIRouter(tags=["interactions"])


# --- Comments ---

@router.get("/presentations/{id}/comments", response_model=list[CommentRead])
async def list_comments(id: str, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    result = await db.scalars(select(Comment).where(Comment.presentation_id == uuid.UUID(id)).order_by(Comment.created_at))
    return result.all()


@router.post("/presentations/{id}/comments", response_model=CommentRead, status_code=201)
async def create_comment(id: str, data: CommentCreate, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    obj = Comment(presentation_id=uuid.UUID(id), **data.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/comments/{id}", response_model=CommentRead)
async def update_comment(id: str, data: CommentUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Comment, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Comment not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/comments/{id}", status_code=204)
async def delete_comment(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Comment, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Comment not found")
    await db.delete(obj)
    await db.commit()


# --- Annotations ---

@router.get("/presentations/{id}/annotations", response_model=list[AnnotationRead])
async def list_annotations(id: str, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    result = await db.scalars(select(Annotation).where(Annotation.presentation_id == uuid.UUID(id)).order_by(Annotation.created_at))
    return result.all()


@router.post("/presentations/{id}/annotations", response_model=AnnotationRead, status_code=201)
async def create_annotation(id: str, data: AnnotationCreate, db: AsyncSession = Depends(get_db)):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")
    dump = data.model_dump()
    if dump.get("attachment_id"):
        dump["attachment_id"] = uuid.UUID(dump["attachment_id"])
    obj = Annotation(presentation_id=uuid.UUID(id), **dump)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.patch("/annotations/{id}", response_model=AnnotationRead)
async def update_annotation(id: str, data: AnnotationUpdate, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Annotation, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Annotation not found")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/annotations/{id}", status_code=204)
async def delete_annotation(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Annotation, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Annotation not found")
    await db.delete(obj)
    await db.commit()