from datetime import datetime
from functools import wraps
from typing import Type, Callable, Any
from pydantic import BaseModel


def standardize_datetime_str(dt: datetime) -> str:
    """Coverts datetime object to ISO 8601 format"""
    assert isinstance(dt, datetime), "dt must be a datetime object"
    return dt.isoformat(timespec="milliseconds") + "Z"


def convert_response(data: Any, model: Type[BaseModel]):
    """Convert raw API responses into models, preserving pagination envelopes"""
    if isinstance(data, dict) and "items":
        ...


def use_model(model: Type[BaseModel] | None = None):
    """Attach model-conversion support to endpoint methods.

    Usage:
        @use_model(model=Model)
        async def fetch_data(...):
            return data
    """

    async def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            override = kwargs.pop("model", None)

            raw = await func(*args, **kwargs)

            if override is False:
                return raw

            if isinstance(override, type) and issubclass(override, BaseModel):
                return override.model_validate(raw)

            if override:
                if model:
                    return convert_response(raw, model)
                return raw

            if model:
                return convert_response(raw, model)

        return wrapper

    return decorator
