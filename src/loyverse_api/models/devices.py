from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class PosDevice(BaseModel):
    id: UUID
    name: str
    store_id: UUID
    activated: bool = True
    deleted_at: datetime | None = None
