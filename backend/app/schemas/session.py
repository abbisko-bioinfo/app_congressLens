from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionBase(BaseModel):
    conference_id: str
    source_session_id: str | None = None
    title: str
    session_type: str | None = None
    track: str | None = None
    subtrack: str | None = None
    room: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    timezone: str | None = None
    description: str | None = None
    is_on_demand: bool = False


class SessionCreate(SessionBase):
    pass


class SessionUpdate(BaseModel):
    source_session_id: str | None = None
    title: str | None = None
    session_type: str | None = None
    track: str | None = None
    subtrack: str | None = None
    room: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    timezone: str | None = None
    description: str | None = None
    is_on_demand: bool | None = None


class SessionRead(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class SessionList(BaseModel):
    items: list[SessionRead]
    total: int