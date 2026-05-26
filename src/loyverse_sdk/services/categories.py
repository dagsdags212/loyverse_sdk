"""Categories service with business logic validation on top of CategoriesEndpoint."""

from loyverse_sdk.exceptions import ValidationError
from loyverse_sdk.models import Category
from loyverse_sdk.services.base import BaseService


class CategoriesService(BaseService):
    """
    Service for Category operations with business logic validation.

    Wraps CategoriesEndpoint with validation for category names.
    """

    def _validate_category_data(self, data: dict) -> None:
        """
        Validate category data before create/update operations.

        Raises:
            ValidationError: If category name is empty or missing
        """
        if not data:
            raise ValidationError(
                message="Category data cannot be empty",
                model_name="Category",
            )

        name = data.get("name")
        if not name or not str(name).strip():
            raise ValidationError(
                message="Category name cannot be empty or whitespace-only",
                model_name="Category",
            )

    async def create_category(self, category_data: dict) -> Category:
        """
        Create a new category after validating input data.

        Args:
            category_data: Category creation payload dict

        Returns:
            Category: The created category

        Raises:
            ValidationError: If category name is empty
        """
        self._validate_category_data(category_data)
        return await self._client.categories.create(category_data)

    async def update_category(self, id: str, category_data: dict) -> Category:
        """
        Update an existing category after validating input data.

        Args:
            id: The category ID to update
            category_data: Category update payload dict

        Returns:
            Category: The updated category

        Raises:
            ValidationError: If category name is empty
        """
        self._validate_category_data(category_data)
        return await self._client.categories.update(id, category_data)

    async def retrieve_category(self, id: str) -> Category:
        """
        Retrieve a category by ID.

        Args:
            id: Category UUID string

        Returns:
            Category: The retrieved category

        Raises:
            NotFoundError: If category not found
        """
        return await self._client.categories.retrieve(id)
