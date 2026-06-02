from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WatchlistItemCreate(BaseModel):
    user_id: str | None = None
    target_type: str
    target_id: str
    note: str | None = None


class WatchlistItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str | None = None
    target_type: str
    target_id: str
    note: str | None = None
    created_at: datetime