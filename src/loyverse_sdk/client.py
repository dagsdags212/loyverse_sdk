from typing import Mapping
import httpx
from loyverse_sdk.auth import Auth
from loyverse_sdk.core.config import config
from loyverse_sdk.exceptions import (
    APIError,
    BadRequestError,
    AuthenticationError,
    ForbiddenError,
    NotFoundError,
    RateLimitError,
    ServerError,
    NetworkError,
)
from loyverse_sdk.endpoints.base import BaseEndpoint
from loyverse_sdk.endpoints import (
    CategoriesEndpoint,
    CustomersEndpoint,
    DiscountsEndpoint,
    EmployeesEndpoint,
    ItemsEndpoint,
    MerchantEndpoint,
    ModifiersEndpoint,
    PosDevicesEndpoints,
    ReceiptsEndpoint,
    StoresEndpoint,
    SuppliersEndpoint,
    TaxesEndpoint,
    WebhooksEndpoint,
    VariantsEndpoint,
)


class LoyverseClient:
    """Base class for sending HTTP requests to the Loyverse REST API"""

    def __init__(
        self,
        api_token: str | None = None,
        base_url: str = config.BASE_URL,
        timeout: float = 15.0,
    ):
        self.auth = Auth(api_token)

        # Shared asynchronous client
        self._client = httpx.AsyncClient(
            base_url=base_url, headers=self.auth.headers, timeout=timeout,
        )

        self.categories = CategoriesEndpoint(self)
        self.customers = CustomersEndpoint(self)
        self.discounts = DiscountsEndpoint(self)
        self.devices = PosDevicesEndpoints(self)
        self.employees = EmployeesEndpoint(self)
        self.items = ItemsEndpoint(self)
        self.merchant = MerchantEndpoint(self)
        self.modifiers = ModifiersEndpoint(self)
        self.receipts = ReceiptsEndpoint(self)
        self.stores = StoresEndpoint(self)
        self.suppliers = SuppliersEndpoint(self)
        self.taxes = TaxesEndpoint(self)
        self.webhooks = WebhooksEndpoint(self)
        self.variants = VariantsEndpoint(self)

    @property
    def endpoints(self) -> Mapping[str, BaseEndpoint]:
        """Returns a mapping of API endpoints to their objects"""
        return {
            "categories": self.categories,
            "customers": self.customers,
            "discounts": self.discounts,
            "devices": self.devices,
            "employees": self.employees,
            "items": self.items,
            "merchant": self.merchant,
            "modifiers": self.modifiers,
            "receipts": self.receipts,
            "stores": self.stores,
            "suppliers": self.suppliers,
            "taxes": self.taxes,
            "webhooks": self.webhooks,
            "variants": self.variants,
        }

    async def request(self, method: str, path: str, **kwargs) -> dict:
        """
        Send an HTTP request from the client to the endpoint.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            path: API endpoint path
            **kwargs: Additional arguments passed to httpx (params, json, headers, etc.)

        Returns:
            Response data as dict or text

        Raises:
            BadRequestError: For HTTP 400 errors
            AuthenticationError: For HTTP 401 errors
            ForbiddenError: For HTTP 403 errors
            NotFoundError: For HTTP 404 errors
            RateLimitError: For HTTP 429 errors
            ServerError: For HTTP 5xx errors
            APIError: For other HTTP error status codes
            NetworkError: For network/connection issues
        """
        try:
            resp = await self._client.request(method, path, **kwargs)
        except httpx.TimeoutException as e:
            raise NetworkError(
                f"Request to '{path}' timed out",
                original_error=e
            )
        except httpx.ConnectError as e:
            raise NetworkError(
                f"Failed to connect to API at '{path}'",
                original_error=e
            )
        except httpx.HTTPError as e:
            raise NetworkError(
                f"Network error occurred while requesting '{path}'",
                original_error=e
            )

        # Handle error responses
        if resp.status_code >= 400:
            try:
                payload = resp.json()
            except Exception:
                payload = resp.text

            # Map status codes to specific exception types
            if resp.status_code == 400:
                raise BadRequestError(payload, endpoint=path)
            elif resp.status_code == 401:
                raise AuthenticationError(payload, endpoint=path)
            elif resp.status_code == 403:
                raise ForbiddenError(payload, endpoint=path)
            elif resp.status_code == 404:
                raise NotFoundError(payload, endpoint=path)
            elif resp.status_code == 429:
                # Try to extract Retry-After header
                retry_after = resp.headers.get("Retry-After")
                retry_after_seconds = int(retry_after) if retry_after and retry_after.isdigit() else None
                raise RateLimitError(payload, endpoint=path, retry_after=retry_after_seconds)
            elif resp.status_code >= 500:
                raise ServerError(resp.status_code, payload, endpoint=path)
            else:
                # Generic API error for other status codes
                raise APIError(resp.status_code, payload, endpoint=path)

        # Parse successful response
        try:
            return resp.json()
        except Exception:
            return resp.text

    async def close(self):
        """Close the client instance"""
        await self._client.aclose()
