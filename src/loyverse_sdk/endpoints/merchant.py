from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints.mixins import (
    RetrieveMixin,
)
from loyverse_sdk.models import Merchant


class MerchantEndpoint(BaseEndpoint, RetrieveMixin):
    path = "merchant"

    async def retrieve(self):
        data = await self._get(self.path)
        return Merchant.model_validate(data)
