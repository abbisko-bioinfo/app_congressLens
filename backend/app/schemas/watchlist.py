import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WatchlistItemCreate(BaseModel):
    user_id: str | None = None
    target_type: str
    target_id: uuid.UUID
    note: str | None = None


class WatchlistItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: str | None = None
    target_type: str
    target_id: uuid.UUID
    note: str | None = None
    created_at: datetime