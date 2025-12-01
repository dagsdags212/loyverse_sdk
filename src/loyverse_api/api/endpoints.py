from typing import Hashable, Any
from datetime import datetime
import httpx
from pydantic._internal._model_construction import ModelMetaclass
from pydantic import ValidationError
from loyverse_api.core.config import config
from loyverse_api.core.console import console
from loyverse_api.api._endpoint import BaseEndpoint


class LoyverseEndpoint(BaseEndpoint):
    base_url: str = "https://api.loyverse.com/v1.0"
    api_key: str = config.loyverse_api_key

    def __init__(self, model: ModelMetaclass | None = None, **kwargs):
        super().__init__(**kwargs)
        self._model = model

    # Only update this for logic in model instantiation
    def _validate_json(
        self, data: dict[Hashable, Any]
    ) -> ModelMetaclass | dict[Hashable, Any]:
        """Validate JSON data and instantiate into a pydantic model.
        If an invalid pydantic model is passed, return the raw data"""
        if self._model is None:
            return data

        if not isinstance(self._model, ModelMetaclass):
            raise TypeError("not a valid pydantic model")

        try:
            m = self._model.model_validate(data)
            return m
        except ValidationError:
            if self.debug:
                console.log(
                    f"data (with {len(data)} keys) does not matche model schema"
                )
            return data

    def fetch_by_id(self, id: str) -> dict | None:
        """Retrieve a single record from an ID"""
        try:
            url = f"{self.url}/{id}"
            if self.debug:
                console.log(f"Sending a GET request to '{url}'")
            resp = httpx.get(url, params={}, headers=self.headers)
            resp.raise_for_status()
            data = resp.json()
            return self._validate_json(data)

        except httpx.HTTPStatusError as exc:
            console.log(
                f"Error response {exc.response.status_code} while requesting {exc.request.url!r}"
            )
            return

    # TODO: support printing to stdout, redirect output to file
    def fetch_all(
        self,
        limit: int = None,
    ) -> list[dict[str, any]]:
        """Recursively call a loyverse endpoint to retrieve all records"""
        limit = self.params.get("limit", 50)
        page = 1
        records: list[dict] | list[ModelMetaclass] = []

        data, cursor = self.get()
        records.extend([self._validate_json(record) for record in data])

        if self.debug:
            console.log(
                f"Retrieving records from '/{self.endpoint}' endpoint ({page} - {len(records)})"
            )

        while cursor:
            page += 1
            data, cursor = self.get(cursor=cursor)
            records.extend([self._validate_json(record) for record in data])

            if self.debug:
                console.log(
                    f"Retrieving records from '/{self.endpoint}' endpoint ({(page - 1) * limit + 1} - {len(records)})"
                )

        if self.debug:
            console.log(f"Successfully retrieved {len(records)} records")

        return records

    def fetch_most_recent(self, n: int = 50) -> list[dict[str, any]]:
        """Retrieve the n most recent records"""
        limit = 250 if n >= 250 else n
        self.params["limit"] = limit
        page = 1
        records = []

        data, cursor = self.get()
        records.extend([self._validate_json(record) for record in data])

        if len(records) > n:
            return records[:n]

        if self.debug:
            console.log(
                f"Retrieving records from '/{self.endpoint}' endpoint ({page} - {len(records)})"
            )

        while cursor:
            page += 1
            data, cursor = self.get(cursor=cursor)
            records.extend([self._validate_json(record) for record in data])

            if len(records) > n:
                return records[:n]

            if self.debug:
                console.log(
                    f"Retrieving records from '/{self.endpoint}' endpoint ({(page - 1) * limit + 1} - {len(records)})"
                )

        if self.debug:
            console.log(f"Successfully retrieved {len(records)} records")

        return records

    def _validate_dt(self, dt: datetime) -> str:
        """Parses a datetme format and converts to ISO 8601 format"""
        assert isinstance(dt, datetime), "dt must be a datetime object"
        dt = dt.isoformat(sep="T", timespec="milliseconds") + "Z"
        return dt

    def fetch_after_dt(self, dt: datetime):
        """Retrieve all records created AFTER the specified datetime"""
        self.params["created_at_min"] = self._validate_dt(dt)
        self.params["created_at_max"] = None
        records = self.fetch_all()
        return records

    def fetch_before_dt(self, dt: datetime):
        """Retrieve all records created BEFORE the specified datetime"""
        self.params["created_at_min"] = None
        self.params["created_at_max"] = self._validate_dt(dt)
        records = self.fetch_all()
        return records

    def fetch_between_dt(
        self,
        start: datetime,
        end: datetime,
    ):
        """Retrieve all records created BEFORE the specified datetime"""
        assert end >= start, "end date must be greater than start date"

        self.params["created_at_min"] = self._validate_dt(start)
        self.params["created_at_max"] = self._validate_dt(end)
        records = self.fetch_all()
        return records
