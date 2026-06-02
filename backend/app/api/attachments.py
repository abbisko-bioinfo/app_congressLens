import mimetypes
import uuid
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.attachment import Attachment
from app.models.presentation import Presentation
from app.services.minio import client as minio_client, ensure_bucket
from app.schemas.presentation import AttachmentRead

router = APIRouter(prefix="/presentations", tags=["attachments"])

PREVIEWABLE_TYPES = {"application/pdf", "image/png", "image/jpeg", "image/gif", "image/webp"}
CONVERSION_TYPES = {
    "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
}


@router.get("/{id}/attachments", response_model=list[AttachmentRead])
async def list_attachments(id: str, db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(Attachment).where(Attachment.presentation_id == uuid.UUID(id)).order_by(Attachment.uploaded_at))
    return result.all()


@router.post("/{id}/attachments", response_model=AttachmentRead, status_code=201)
async def upload_attachment(
    id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    pres = await db.get(Presentation, uuid.UUID(id))
    if not pres:
        raise HTTPException(404, "Presentation not found")

    ensure_bucket(minio_client)

    content_type = file.content_type or mimetypes.guess_type(file.filename or "")[0] or "application/octet-stream"
    object_key = f"presentations/{id}/{uuid.uuid4()}/{file.filename}"

    file_size = 0
    data = await file.read()
    file_size = len(data)

    minio_client.put_object(
        settings.minio_bucket,
        object_key,
        data,
        file_size,
        content_type=content_type,
    )

    preview_status = "ready" if content_type in PREVIEWABLE_TYPES else (
        "pending" if content_type in CONVERSION_TYPES else "not_supported"
    )

    obj = Attachment(
        presentation_id=uuid.UUID(id),
        original_filename=file.filename or "unknown",
        original_object_key=object_key,
        bucket_name=settings.minio_bucket,
        content_type=content_type,
        file_size=file_size,
        preview_status=preview_status,
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/attachments/{id}/preview")
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


@router.get("/attachments/{id}/download")
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


@router.delete("/attachments/{id}", status_code=204)
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