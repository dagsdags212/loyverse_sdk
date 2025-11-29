from datetime import datetime
from typing import Optional
import httpx
from pydantic import BaseModel
from loyverse_api.core.config import config
from loyverse_api.core.console import console


class Endpoint(BaseModel):
    endpoint: str
    base_url: str
    api_key: Optional[str] = None
    headers: dict = {}
    params: dict = {"limit": config.limit}
    data: dict = {}

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if self.api_key is None:
            raise Exception(
                "API key not found, provide it as an named parameter or in a .env file"
            )

        self.headers["Authorization"] = f"Bearer {self.api_key}"

    @property
    def url(self) -> str:
        return f"{self.base_url}/{self.endpoint}"

    def set_limit(self, limit: int, debug: bool = False) -> None:
        assert limit > 0, "limit should be a positive integer"
        if debug:
            console.log(f"limit set to {limit}")
        self.params["limit"] = limit


class LoyverseEndpoint(Endpoint):
    base_url: str = "https://api.loyverse.com/v1.0"
    api_key: str = config.loyverse_api_key

    def _get(self, cursor: str | None = None) -> tuple[dict, str | None] | None:
        if self.api_key is None:
            raise ValueError("API key not provided")

        if cursor:
            self.params["cursor"] = cursor

        try:
            resp = httpx.get(self.url, params=self.params, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()

            return data.get(self.endpoint, []), data.get("cursor")

        except httpx.HTTPStatusError as exc:
            console.print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}"
            )
            return

    def fetch_by_id(self, id: str) -> dict | None:
        """Retrieve a single record from an ID"""
        try:
            url = f"{self.url}/{id}"
            resp = httpx.get(url, params={}, headers=self.headers)
            resp.raise_for_status()

            return resp.json()

        except httpx.HTTPStatusError as exc:
            console.print(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}"
            )
            return

    # TODO: support printing to stdout, redirect output to file
    def fetch_all(self, limit: int = None, debug: bool = False) -> list[dict[str, any]]:
        """Recursively call a loyverse endpoint to retrieve all records"""
        limit = self.params.get("limit", 50)
        page = 1
        records = []

        data, cursor = self._get()
        records.extend([record for record in data])

        if debug:
            console.log(
                f"Retrieving records from '/{self.endpoint}' endpoint ({page} - {len(records)})"
            )

        while cursor:
            page += 1
            data, cursor = self._get(cursor=cursor)
            records.extend([record for record in data])

            if debug:
                print(
                    f"Retrieving records from '/{self.endpoint}' endpoint ({(page - 1) * limit + 1} - {len(records)})"
                )

        if debug:
            console.log(f"Successfully retrieved {len(records)} records")

        return records

    def fetch_most_recent(
        self, n: int = 50, debug: bool = False
    ) -> list[dict[str, any]]:
        """Retrieve the n most recent records"""
        limit = 250 if n >= 250 else n
        self.params["limit"] = limit
        page = 1
        records = []

        data, cursor = self._get()
        records.extend([record for record in data])

        if len(records) > n:
            return records[:n]

        if debug:
            console.log(
                f"Retrieving records from '/{self.endpoint}' endpoint ({page} - {len(records)})"
            )

        while cursor:
            page += 1
            data, cursor = self._get(cursor=cursor)
            records.extend([record for record in data])

            if len(records) > n:
                return records[:n]

            if debug:
                console.log(
                    f"Retrieving records from '/{self.endpoint}' endpoint ({(page - 1) * limit + 1} - {len(records)})"
                )

        if debug:
            console.log(f"Successfully retrieved {len(records)} records")

        return records

    def fetch_after_dt(self, dt: datetime, debug: bool = False):
        """Retrieve all records created AFTER the specified datetime"""
        assert isinstance(dt, datetime), "dt must be a datetime object"
        self.params["created_at_min"] = dt.isoformat() + ".000Z"
        records = self.fetch_all(debug=debug)
        return records

    def fetch_before_dt(self, dt: datetime, debug: bool = False):
        """Retrieve all records created BEFORE the specified datetime"""
        assert isinstance(dt, datetime), "dt must be a datetime object"
        self.params["created_at_max"] = dt.isoformat() + ".000Z"
        records = self.fetch_all(debug=debug)
        return records

    def fetch_between_dt(self, start: datetime, end: datetime, debug: bool = False):
        """Retrieve all records created BEFORE the specified datetime"""
        assert isinstance(start, datetime), "start must be a datetime object"
        assert isinstance(end, datetime), "start must be a datetime object"
        self.params["created_at_min"] = start.isoformat() + ".000Z"
        self.params["created_at_max"] = end.isoformat() + ".000Z"
        records = self.fetch_all(debug=debug)
        return records


class LoyverseEndpoints:
    """Entry point for accessing all Loyverse endpoints"""

    # CATEGORIES = LoyverseEndpoint(endpoint="categories")
    CUSTOMERS = LoyverseEndpoint(endpoint="customers")
    DISCOUNTS = LoyverseEndpoint(endpoint="discounts")
    EMPLOYEES = LoyverseEndpoint(endpoint="employees")
    INVENTORY = LoyverseEndpoint(endpoint="inventory")
    ITEMS = LoyverseEndpoint(endpoint="items")
    PAYMENT_TYPES = LoyverseEndpoint(endpoint="payment_types")
    POS_DEVICES = LoyverseEndpoint(endpoint="pos_devices")
    RECEIPTS = LoyverseEndpoint(endpoint="receipts")
    STORES = LoyverseEndpoint(endpoint="stores")
    # SHIFTS = LoyverseEndpoint(endpoint="shifts")
    # SUPPLIERS = LoyverseEndpoint(endpoint="suppliers")
    # TAXES = LoyverseEndpoint(endpoint="taxes")
    # WEBHOOKS = LoyverseEndpoint(endpoint="webhooks")
    # VARIANTS = LoyverseEndpoint(endpoint="variants")
