import uuid

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.attachment import Attachment
from app.workers.celery_app import app as celery_app

PPTX_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
DOCX_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
XLSX_CONTENT_TYPES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


@celery_app.task(name="convert_attachment_preview")
def convert_attachment_preview(attachment_id: str) -> dict:
    with SessionLocal() as db:
        obj = db.get(Attachment, uuid.UUID(attachment_id))
        if not obj:
            return {"attachment_id": attachment_id, "status": "failed", "message": "Attachment not found"}

        content_type = obj.content_type or ""

        if content_type in XLSX_CONTENT_TYPES:
            obj.preview_status = "not_supported"
            obj.conversion_error = "XLSX preview conversion not supported in MVP"
            db.commit()
            return {"attachment_id": attachment_id, "status": "not_supported", "message": "XLSX not supported in MVP"}

        if content_type in PPTX_CONTENT_TYPES or content_type in DOCX_CONTENT_TYPES:
            obj.preview_status = "processing"
            db.commit()
            # MVP placeholder: no actual conversion tooling available
            obj.preview_status = "not_supported"
            obj.conversion_error = f"{content_type} preview conversion not available in MVP"
            db.commit()
            return {"attachment_id": attachment_id, "status": "not_supported", "message": f"{content_type} conversion not available in MVP"}

        return {"attachment_id": attachment_id, "status": "not_supported", "message": "Unsupported content type for preview conversion"}


@celery_app.task(name="generate_presentation_summary")
def generate_presentation_summary(presentation_id: str) -> dict:
    return {"presentation_id": presentation_id, "status": "pending", "message": "AI summary not implemented in MVP"}


@celery_app.task(name="extract_presentation_entities")
def extract_presentation_entities(presentation_id: str) -> dict:
    return {"presentation_id": presentation_id, "status": "pending", "message": "Entity extraction not implemented in MVP"}


@celery_app.task(name="generate_conference_summary")
def generate_conference_summary(conference_id: str) -> dict:
    return {"conference_id": conference_id, "status": "pending", "message": "Conference summary not implemented in MVP"}