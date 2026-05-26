"""
Service layer for Customers with business validation.
"""

from loyverse_sdk.services.base import BaseService
from loyverse_sdk.models import Customer
from loyverse_sdk.exceptions import ValidationError, NotFoundError


class CustomersService(BaseService):
    """
    Service layer for customer operations with email validation.

    Wraps CustomersEndpoint and adds business validation logic.
    """

    def _validate_email(self, email: str | None) -> str | None:
        """Validate email format. Allows None (optional field)."""
        if email is None:
            return None

        if isinstance(email, str):
            email = email.strip()
            if email == "":
                raise ValidationError(
                    message="Email cannot be empty or whitespace", model_name="Customer"
                )

            # Must contain exactly one @
            at_count = email.count("@")
            if at_count != 1:
                raise ValidationError(
                    message=f"Invalid email format: must contain exactly one '@' (found {at_count})",
                    model_name="Customer",
                )

            # Domain must contain at least one dot after @
            local, domain = email.split("@")
            if "." not in domain:
                raise ValidationError(
                    message=f"Invalid email domain: must contain at least one '.' after '@'",
                    model_name="Customer",
                )

            return email

        raise ValidationError(
            message=f"Email must be a string or None, got {type(email).__name__}",
            model_name="Customer",
        )

    def _validate_customer_data(self, data: dict) -> dict:
        """Validate required fields in customer data."""
        if not data:
            raise ValidationError(
                message="Customer data cannot be empty", model_name="Customer"
            )

        # Check required 'name' field
        if "name" not in data or not data.get("name"):
            raise ValidationError(
                message="Customer 'name' field is required", model_name="Customer"
            )

        return data

    async def create_customer(self, customer_data: dict) -> Customer:
        """
        Create a new customer with email validation.

        Args:
            customer_data: Dictionary with customer fields (name, email, etc.)

        Returns:
            Created Customer instance

        Raises:
            ValidationError: If email format is invalid or required fields missing
            NotFoundError: If the API returns 404
            BadRequestError: If the API returns 400
        """
        # Validate email if provided
        if "email" in customer_data:
            customer_data = customer_data.copy()
            customer_data["email"] = self._validate_email(customer_data["email"])

        # Validate required fields
        self._validate_customer_data(customer_data)

        return await self._client.customers.create(customer_data)

    async def retrieve_customer(self, id: str) -> Customer:
        """
        Retrieve a customer by ID.

        Args:
            id: Customer UUID string

        Returns:
            Customer instance

        Raises:
            NotFoundError: If customer not found
        """
        return await self._client.customers.retrieve(id)

    async def retrieve_by_email(self, email: str) -> Customer:
        """
        Retrieve a customer by email address.

        Iterates through all customers to find one matching the email.
        Note: The Loyverse API does not have a native get-by-email endpoint,
        so this performs a linear search.

        Args:
            email: Email address to search for

        Returns:
            Customer instance if found

        Raises:
            ValidationError: If email format is invalid
            NotFoundError: If no customer found with the given email
        """
        # Validate email format first
        email = self._validate_email(email)
        if not email:
            raise ValidationError(
                message="Email is required for retrieve_by_email", model_name="Customer"
            )

        async for customer in self._client.customers.iter_all(limit=250):
            if customer.email == email:
                return customer

        raise NotFoundError(
            payload={"message": f"No customer found with email: {email}"},
            resource_id=f"email:{email}",
        )

    async def update_customer(self, id: str, customer_data: dict) -> Customer:
        """
        Update an existing customer with email validation.

        Args:
            id: Customer UUID string
            customer_data: Dictionary with fields to update

        Returns:
            Updated Customer instance

        Raises:
            ValidationError: If email format is invalid
            NotFoundError: If customer not found
            BadRequestError: If the API returns 400
        """
        # Validate email if provided
        if "email" in customer_data:
            customer_data = customer_data.copy()
            customer_data["email"] = self._validate_email(customer_data["email"])

        return await self._client.customers.update(id, customer_data)
