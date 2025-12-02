from typing import Type, TypeVar, Any, Callable
from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


def returns_model(model: Type[T]):
    """Decorator to parse response into a pydantic model."""

    def _decorator(fn: Callable[..., Any]):
        async def _inner(*args, **kwargs):
            data = await fn(*args, **kwargs)
            if isinstance(data, model):
                return data
            return (
                model.model_validate(data)
                if hasattr(model, "model_validate")
                else model(**data)
            )

        return _inner

    return _decorator


class BaseEndpoint:
    path: str
    client: "LoyverseClient"

    def __init__(self, client: "LoyverseClient") -> None:
        self.client = client

    async def _get(self, path: str, **kwargs):
        """Send a GET request from the client"""
        return await self.client.request("GET", path, **kwargs)

    async def _post(self, path: str, **kwargs):
        return await self.client.request("POST", path, **kwargs)

    async def _patch(self, path: str, **kwargs):
        return await self.client.request("PATCH", path, **kwargs)

    async def _put(self, path: str, **kwargs):
        return await self.client.request("PUT", path, **kwargs)

    async def _delete(self, path: str, **kwargs):
        return await self.client.request("DELETE", path, **kwargs)
