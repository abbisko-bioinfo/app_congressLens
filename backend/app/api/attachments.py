import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.attachment import Attachment
from app.services.minio import client as minio_client

router = APIRouter(prefix="/attachments", tags=["attachments"])


@router.get("/{id}/preview")
async def preview_attachment(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Attachment, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Attachment not found")
    if obj.preview_status != "ready":
        raise HTTPException(400, f"Preview not available (status: {obj.preview_status})")

    url = minio_client.presigned_get_object(
        obj.bucket_name,
        obj.original_object_key,
        expires=timedelta(hours=1),
    )
    public_host = settings.minio_public_endpoint
    if public_host:
        internal = settings.minio_endpoint
        url = url.replace(internal, public_host)
    return {"url": url}


@router.get("/{id}/download")
async def download_attachment(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Attachment, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Attachment not found")

    url = minio_client.presigned_get_object(
        obj.bucket_name,
        obj.original_object_key,
        expires=timedelta(hours=1),
    )
    public_host = settings.minio_public_endpoint
    if public_host:
        url = url.replace(settings.minio_endpoint, public_host)
    return {"url": url, "filename": obj.original_filename, "content_type": obj.content_type}


@router.delete("/{id}", status_code=204)
async def delete_attachment(id: str, db: AsyncSession = Depends(get_db)):
    obj = await db.get(Attachment, uuid.UUID(id))
    if not obj:
        raise HTTPException(404, "Attachment not found")
    try:
        minio_client.remove_object(obj.bucket_name, obj.original_object_key)
    except Exception:
        pass
    await db.delete(obj)
    await db.commit()