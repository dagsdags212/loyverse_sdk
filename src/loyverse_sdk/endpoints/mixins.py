from datetime import datetime
from typing import AsyncGenerator, Type, TypeVar, Generic
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError
from loyverse_sdk.utils import standardize_datetime_str
from loyverse_sdk.core.console import console
from loyverse_sdk.exceptions import ValidationError, PaginationError


T = TypeVar("T")


class ListMixin:
    """Mixin for retrieving a single page of records"""

    path: str

    async def list(
        self,
        limit: int = 50,
        cursor: str | None = None,
        model: Type[BaseModel] | None = None,
        **kwargs,
    ) -> dict:
        params = {"limit": limit, **kwargs}
        if cursor:
            params["cursor"] = cursor

        data = await self._get(self.path, params=params)
        if model:
            try:
                return model.model_validate(data)
            except PydanticValidationError as e:
                console.log(f"[red]Validation failed for {model.__name__}[/red]")
                raise ValidationError(
                    message=str(e),
                    validation_errors=e.errors(),
                    model_name=model.__name__
                )

        return data


class RetrieveMixin:
    """Mixin for retrieving a single record using an id"""

    path: str

    async def retrieve(self, id: str, model: Type[BaseModel] | None = None):
        data = await self._get(f"{self.path}/{id}")
        if model:
            try:
                return model.model_validate(data)
            except PydanticValidationError as e:
                console.log(f"[red]Validation failed for {model.__name__}[/red]")
                raise ValidationError(
                    message=str(e),
                    validation_errors=e.errors(),
                    model_name=model.__name__
                )

        return data


class CreateMixin:
    """Mixin for creating a new record from the client"""

    path: str

    async def create(
        self, payload: dict | Type[BaseModel], model: Type[BaseModel] | None = None
    ):
        json = payload.model_dump() if isinstance(payload, BaseModel) else payload
        data = await self._post(f"{self.path}", json=json)
        if model:
            return model.model_validate(data)

        return data


class UpdateMixin:
    """Mixin for updating a record from the client"""

    path: str

    async def update(
        self, id: str, payload: dict, model: Type[BaseModel] | None = None
    ):
        payload["id"] = id
        data = await self._post(f"{self.path}", json=payload)
        if model:
            return model.model_validate(data)
        return data


class DeleteMixin:
    """Mixin for deleting a record from the client"""

    path: str

    async def delete(self, id: str) -> list[str]:
        return await self._delete(f"{self.path}/{id}")


class PaginationMixin(Generic[T]):
    """Mixin for retrieving records across multiple pages"""

    path: str

    async def list_paginated(
        self,
        limit: int = 250,
        created_at_min: datetime | None = None,
        created_at_max: datetime | None = None,
        updated_at_min: datetime | None = None,
        updated_at_max: datetime | None = None,
        cursor: str | None = None,
    ) -> dict:
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if created_at_min:
            params["created_at_min"] = standardize_datetime_str(created_at_min)
        if created_at_max:
            params["created_at_max"] = standardize_datetime_str(created_at_max)
        if updated_at_min:
            params["updated_at_min"] = standardize_datetime_str(updated_at_min)
        if updated_at_max:
            params["updated_at_max"] = standardize_datetime_str(updated_at_max)

        return await self._get(self.path, params=params)

    async def iter_all(
        self,
        limit: int = 250,
        created_at_min: datetime | None = None,
        created_at_max: datetime | None = None,
        updated_at_min: datetime | None = None,
        updated_at_max: datetime | None = None,
    ) -> AsyncGenerator[T, None]:
        """
        Async generator to iterate over all items across all pages.

        Yields individual items from paginated API responses, automatically
        handling cursor-based pagination until all pages are consumed.

        Raises:
            PaginationError: If pagination metadata is missing or invalid
        """
        cursor = None
        seen_cursors = set()

        while True:
            resp = await self.list_paginated(
                cursor=cursor,
                limit=limit,
                created_at_min=created_at_min,
                created_at_max=created_at_max,
                updated_at_min=updated_at_min,
                updated_at_max=updated_at_max,
            )

            # Validate response structure
            if not isinstance(resp, dict):
                raise PaginationError(
                    f"Expected dict response for pagination, got {type(resp).__name__}"
                )

            records = resp.get(self.path)
            if records is None:
                raise PaginationError(
                    f"Response missing expected key '{self.path}' for records"
                )

            if not isinstance(records, list):
                raise PaginationError(
                    f"Expected list of records, got {type(records).__name__}"
                )

            # Yield each record
            for item in records:
                yield item

            # Get next cursor
            cursor = resp.get("cursor")

            # Check for pagination loop (cursor we've seen before)
            if cursor and cursor in seen_cursors:
                raise PaginationError(
                    f"Pagination loop detected - cursor '{cursor}' seen multiple times"
                )

            if cursor:
                seen_cursors.add(cursor)
            else:
                # No more pages
                break


class CrudMixin(CreateMixin, RetrieveMixin, UpdateMixin, DeleteMixin):
    """Composed mixin for performing CRUD operation from the client"""

    ...
