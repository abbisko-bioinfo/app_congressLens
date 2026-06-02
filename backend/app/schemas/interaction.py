from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    author: str | None = None
    body: str


class CommentUpdate(BaseModel):
    author: str | None = None
    body: str | None = None


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    presentation_id: str
    author: str | None = None
    body: str
    created_at: datetime
    updated_at: datetime


class AnnotationCreate(BaseModel):
    attachment_id: str | None = None
    selected_text: str | None = None
    note: str
    color: str | None = None
    page_number: int | None = None
    anchor_data: dict | None = None
    created_by: str | None = None


class AnnotationUpdate(BaseModel):
    note: str | None = None
    color: str | None = None
    selected_text: str | None = None
    anchor_data: dict | None = None


class AnnotationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    presentation_id: str
    attachment_id: str | None = None
    selected_text: str | None = None
    note: str
    color: str | None = None
    page_number: int | None = None
    anchor_data: dict | None = None
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime