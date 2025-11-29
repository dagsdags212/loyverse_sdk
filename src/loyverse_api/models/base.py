from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, Field


class Base(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = Field(default=None, exclude=True)
