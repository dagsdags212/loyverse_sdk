"""Merchant service with business logic validation on top of MerchantEndpoint."""

from loyverse_sdk.models import Merchant
from loyverse_sdk.services.base import BaseService


class MerchantService(BaseService):
    """
    Service for Merchant operations with business logic validation.

    Wraps MerchantEndpoint with merchant data validation.
    """

    async def retrieve_merchant(self) -> Merchant:
        """
        Retrieve merchant information.

        Returns:
            Merchant: The merchant object

        Raises:
            NotFoundError: If merchant not found
        """
        return await self._client.merchant.retrieve()

    async def get_merchant_info(self) -> dict:
        """
        Get merchant information as a dict.

        Returns:
            dict: Merchant data
        """
        merchant = await self.retrieve_merchant()
        return merchant.model_dump()
