from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class ConferenceBase(BaseModel):
    acronym: str
    name: str
    year: int
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    timezone: str | None = None
    website: str | None = None
    description: str | None = None


class ConferenceCreate(ConferenceBase):
    pass


class ConferenceUpdate(BaseModel):
    acronym: str | None = None
    name: str | None = None
    year: int | None = None
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    timezone: str | None = None
    website: str | None = None
    description: str | None = None


class ConferenceRead(ConferenceBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime


class ConferenceList(BaseModel):
    items: list[ConferenceRead]
    total: int