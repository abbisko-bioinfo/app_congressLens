from app.workers.celery_app import app as celery_app


@celery_app.task(name="convert_attachment_preview")
def convert_attachment_preview(attachment_id: str) -> dict:
    return {"attachment_id": attachment_id, "status": "not_supported", "message": "Conversion not implemented in MVP"}


@celery_app.task(name="generate_presentation_summary")
def generate_presentation_summary(presentation_id: str) -> dict:
    return {"presentation_id": presentation_id, "status": "pending", "message": "AI summary not implemented in MVP"}


@celery_app.task(name="extract_presentation_entities")
def extract_presentation_entities(presentation_id: str) -> dict:
    return {"presentation_id": presentation_id, "status": "pending", "message": "Entity extraction not implemented in MVP"}


@celery_app.task(name="generate_conference_summary")
def generate_conference_summary(conference_id: str) -> dict:
    return {"conference_id": conference_id, "status": "pending", "message": "Conference summary not implemented in MVP"}