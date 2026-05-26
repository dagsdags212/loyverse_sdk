"""POS Devices service with business logic validation on top of PosDevicesEndpoints."""

from loyverse_sdk.models import PosDevice
from loyverse_sdk.services.base import BaseService


class DevicesService(BaseService):
    """
    Service for POS Device operations with business logic validation.

    Wraps PosDevicesEndpoints with basic device validation.
    """

    def _validate_device_data(self, data: dict) -> None:
        """
        Validate device data before create/update operations.

        Args:
            data: Device payload dict

        Raises:
            ValidationError: If required fields are missing
        """
        if not data:
            from loyverse_sdk.exceptions import ValidationError

            raise ValidationError(
                message="Device data cannot be empty",
                model_name="PosDevice",
            )

    async def retrieve_device(self, id: str) -> PosDevice:
        """
        Retrieve a POS device by ID.

        Args:
            id: Device UUID string

        Returns:
            PosDevice: The retrieved device

        Raises:
            NotFoundError: If device not found
        """
        return await self._client.devices.retrieve(id)

    async def list_devices(self, **kwargs):
        """
        List all POS devices with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of PosDevice objects
        """
        return await self._client.devices.list(**kwargs)

    async def create_device(self, device_data: dict) -> PosDevice:
        """
        Create a new POS device after validating input data.

        Args:
            device_data: Device creation payload dict

        Returns:
            PosDevice: The created device

        Raises:
            ValidationError: If device data is invalid
        """
        self._validate_device_data(device_data)
        return await self._client.devices.create(device_data)

    async def update_device(self, id: str, device_data: dict) -> PosDevice:
        """
        Update an existing POS device after validating input data.

        Args:
            id: The device ID to update
            device_data: Device update payload dict

        Returns:
            PosDevice: The updated device

        Raises:
            ValidationError: If device data is invalid
        """
        self._validate_device_data(device_data)
        return await self._client.devices.update(id, device_data)
