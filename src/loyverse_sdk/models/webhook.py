from datetime import datetime
from enum import StrEnum
from uuid import UUID
from pydantic import BaseModel, Field
from loyverse_sdk.models.common import Pagination


class WebhookType(StrEnum):
    INVENTORY_LEVELS_UPDATE = "inventory_levels.update"
    ITEMS_UPDATE = "items.update"
    CUSTOMERS_UPDATE = "customers.update"
    RECEIPTS_UPDATE = "receipts.update"
    SHIFTS_CREATE = "shifts.create"


class WebhookStatus(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class Webhook(BaseModel):
    id: UUID
    merchant_id: UUID
    url: str
    type: WebhookType
    status: WebhookStatus = WebhookStatus.ENABLED
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class WebhookListResponse(Pagination):
    items: list[Webhook] = Field(alias="webhooks")
