"""Base service class for all service classes in the services layer."""

from abc import ABC


class BaseService(ABC):
    """
    Base class for all service classes.

    Services wrap endpoint instances and add business logic validation,
    multi-step operations, and cross-field constraints on top of the
    raw CRUD operations provided by endpoints.

    Attributes:
        _client: Internal reference to the LoyverseClient instance

    Example:
        class ItemsService(BaseService):
            async def create_item(self, item_data: dict):
                self._validate_item_data(item_data)
                return await self._client.items.create(item_data)
    """

    def __init__(self, client: "LoyverseClient") -> None:
        """Initialize the service with a client reference."""
        self._client = client

    @property
    def client(self) -> "LoyverseClient":
        """Returns the LoyverseClient instance for subclass use."""
        return self._client
