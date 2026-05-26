import json
from datetime import datetime
from typing import Callable, Mapping, Optional
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
    InventoryEndpoint,
    MerchantEndpoint,
    ModifiersEndpoint,
    PosDevicesEndpoints,
    ReceiptsEndpoint,
    ShiftsEndpoint,
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
            base_url=base_url,
            headers=self.auth.headers,
            timeout=timeout,
        )

        self.categories = CategoriesEndpoint(self)
        self.customers = CustomersEndpoint(self)
        self.discounts = DiscountsEndpoint(self)
        self.devices = PosDevicesEndpoints(self)
        self.employees = EmployeesEndpoint(self)
        self.inventory = InventoryEndpoint(self)
        self.items = ItemsEndpoint(self)
        self.merchant = MerchantEndpoint(self)
        self.modifiers = ModifiersEndpoint(self)
        self.receipts = ReceiptsEndpoint(self)
        self.shifts = ShiftsEndpoint(self)
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
            "inventory": self.inventory,
            "items": self.items,
            "merchant": self.merchant,
            "modifiers": self.modifiers,
            "receipts": self.receipts,
            "shifts": self.shifts,
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
            raise NetworkError(f"Request to '{path}' timed out", original_error=e)
        except httpx.ConnectError as e:
            raise NetworkError(
                f"Failed to connect to API at '{path}'", original_error=e
            )
        except httpx.HTTPError as e:
            raise NetworkError(
                f"Network error occurred while requesting '{path}'", original_error=e
            )

        # Handle error responses
        if resp.status_code >= 400:
            try:
                payload = resp.json()
            except json.JSONDecodeError:
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
                retry_after_seconds = (
                    int(retry_after) if retry_after and retry_after.isdigit() else None
                )
                raise RateLimitError(
                    payload, endpoint=path, retry_after=retry_after_seconds
                )
            elif resp.status_code >= 500:
                raise ServerError(resp.status_code, payload, endpoint=path)
            else:
                # Generic API error for other status codes
                raise APIError(resp.status_code, payload, endpoint=path)

        # Parse successful response
        try:
            return resp.json()
        except json.JSONDecodeError:
            return resp.text

    async def close(self):
        """Close the client instance"""
        await self._client.aclose()

    # ========================================================================
    # DUCKDB EXPORT METHODS
    # ========================================================================

    async def export_to_duckdb(
        self,
        db_path: str,
        resources: Optional[list[str]] = None,
        created_at_min: Optional[datetime] = None,
        created_at_max: Optional[datetime] = None,
        updated_at_min: Optional[datetime] = None,
        updated_at_max: Optional[datetime] = None,
        batch_size: int = 1000,
        progress_callback: Optional[Callable[[str, int, int], None]] = None,
        create_indexes: bool = True,
    ) -> dict[str, int]:
        """
        Export Loyverse data to DuckDB database.

        Streams data from all 14 API endpoints and exports to a local DuckDB
        database with proper relational schema and foreign keys.

        Args:
            db_path: Path to DuckDB database file (will be created if doesn't exist)
            resources: List of resource names to export (None = all resources)
                Valid: categories, customers, employees, items, receipts, etc.
            created_at_min: Filter records created after this datetime
            created_at_max: Filter records created before this datetime
            updated_at_min: Filter records updated after this datetime
            updated_at_max: Filter records updated before this datetime
            batch_size: Number of records to insert per transaction (default: 1000)
            progress_callback: Optional callback function(resource_name, current, total)
            create_indexes: Whether to create indexes after export (default: True)

        Returns:
            Dictionary mapping resource names to record counts exported

        Raises:
            ExportError: If export fails

        Example:
            # Full export
            client = LoyverseClient()
            counts = await client.export_to_duckdb("loyverse.duckdb")
            print(f"Exported: {counts}")
            # Output: {'categories': 15, 'customers': 1250, 'receipts': 45000, ...}

            # Date range export (specific period)
            from datetime import datetime
            counts = await client.export_to_duckdb(
                "loyverse.duckdb",
                created_at_min=datetime(2024, 1, 1),
                created_at_max=datetime(2024, 12, 31),
            )

            # Selective export with progress
            def progress(resource, current, total):
                print(f"{resource}: {current}/{total}")

            counts = await client.export_to_duckdb(
                "loyverse.duckdb",
                resources=["receipts", "customers", "items"],
                progress_callback=progress,
            )

            await client.close()
        """
        from loyverse_sdk.db.exporter import DuckDBExporter

        exporter = DuckDBExporter(self, db_path)
        try:
            return await exporter.export_all(
                resources=resources,
                created_at_min=created_at_min,
                created_at_max=created_at_max,
                updated_at_min=updated_at_min,
                updated_at_max=updated_at_max,
                batch_size=batch_size,
                progress_callback=progress_callback,
                create_indexes_after=create_indexes,
            )
        finally:
            exporter.close()

    async def export_resource_to_duckdb(
        self,
        resource_name: str,
        db_path: str,
        created_at_min: Optional[datetime] = None,
        created_at_max: Optional[datetime] = None,
        updated_at_min: Optional[datetime] = None,
        updated_at_max: Optional[datetime] = None,
        batch_size: int = 1000,
    ) -> int:
        """
        Export a single resource to DuckDB.

        Lower-level method for exporting individual resources with more control.
        Use export_to_duckdb() for most cases.

        Args:
            resource_name: Name of resource (e.g., "receipts", "items", "customers")
            db_path: Path to DuckDB database file
            created_at_min: Filter records created after this datetime
            created_at_max: Filter records created before this datetime
            updated_at_min: Filter records updated after this datetime
            updated_at_max: Filter records updated before this datetime
            batch_size: Number of records to insert per transaction

        Returns:
            Number of records exported

        Raises:
            ExportError: If export fails

        Example:
            client = LoyverseClient()

            # Export only receipts
            count = await client.export_resource_to_duckdb(
                "receipts",
                "loyverse.duckdb"
            )
            print(f"Exported {count} receipts")

            await client.close()
        """
        from loyverse_sdk.db.exporter import DuckDBExporter

        exporter = DuckDBExporter(self, db_path)
        try:
            return await exporter.export_resource(
                resource_name,
                created_at_min=created_at_min,
                created_at_max=created_at_max,
                updated_at_min=updated_at_min,
                updated_at_max=updated_at_max,
                batch_size=batch_size,
            )
        finally:
            exporter.close()

    def init_duckdb_schema(
        self,
        db_path: str,
        drop_existing: bool = False,
    ) -> None:
        """
        Initialize DuckDB database schema without exporting data.

        Creates all tables, foreign keys, and constraints but doesn't populate them.
        Useful for setting up the database structure before export or for manual
        data insertion.

        Args:
            db_path: Path to DuckDB database file
            drop_existing: If True, drops all tables before creating schema

        Example:
            client = LoyverseClient()

            # Initialize empty database
            client.init_duckdb_schema("loyverse.duckdb")

            # Reset database (drop all tables and recreate)
            client.init_duckdb_schema("loyverse.duckdb", drop_existing=True)
        """
        from loyverse_sdk.db.schema_builder import create_duckdb_schema

        create_duckdb_schema(db_path, drop_existing=drop_existing)
