from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PresentationBase(BaseModel):
    conference_id: str
    session_id: str | None = None
    source_presentation_id: str | None = None
    source_content_id: str | None = None
    title: str
    abstract_text: str | None = None
    abstract_html: str | None = None
    presentation_number: str | None = None
    abstract_number: str | None = None
    poster_board_number: str | None = None
    presentation_type: str | None = None
    activity: str | None = None
    status: str | None = None
    position_in_session: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    timezone: str | None = None
    presenter_name: str | None = None
    first_author_name: str | None = None
    author_block_html: str | None = None
    institution_block: str | None = None
    disclosure_block_html: str | None = None
    funding_sources: list[str] | None = None
    additional_funding_source: str | None = None
    doi: str | None = None
    journal_citation: str | None = None
    clinical_trial_registry_number: str | None = None
    source_url: str | None = None
    disclosure_url: str | None = None
    has_abstract: bool = False
    has_slides: bool = False
    has_posters: bool = False
    has_videos: bool = False
    summary_status: str = "none"


class PresentationCreate(PresentationBase):
    pass


class PresentationUpdate(BaseModel):
    title: str | None = None
    abstract_text: str | None = None
    abstract_html: str | None = None
    presentation_number: str | None = None
    abstract_number: str | None = None
    poster_board_number: str | None = None
    presentation_type: str | None = None
    activity: str | None = None
    status: str | None = None
    position_in_session: int | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    timezone: str | None = None
    presenter_name: str | None = None
    first_author_name: str | None = None
    author_block_html: str | None = None
    institution_block: str | None = None
    disclosure_block_html: str | None = None
    funding_sources: list[str] | None = None
    additional_funding_source: str | None = None
    doi: str | None = None
    journal_citation: str | None = None
    clinical_trial_registry_number: str | None = None
    source_url: str | None = None
    disclosure_url: str | None = None
    has_abstract: bool | None = None
    has_slides: bool | None = None
    has_posters: bool | None = None
    has_videos: bool | None = None
    summary_status: str | None = None


class AuthorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    display_name: str
    normalized_name: str | None = None
    role: str | None = None
    author_order: int | None = None
    organization: str | None = None
    city: str | None = None
    country: str | None = None
    is_first_author: bool
    is_presenter: bool


class AttachmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    original_filename: str
    content_type: str | None = None
    file_size: int | None = None
    preview_status: str
    uploaded_at: datetime


class PresentationRead(PresentationBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
    authors: list[AuthorRead] = []
    attachments: list[AttachmentRead] = []


class PresentationList(BaseModel):
    items: list[PresentationRead]
    total: int