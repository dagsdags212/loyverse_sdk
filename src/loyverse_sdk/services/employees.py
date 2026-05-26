"""Employees service with business logic validation on top of EmployeesEndpoint."""

from loyverse_sdk.models import Employee
from loyverse_sdk.services.base import BaseService


class EmployeesService(BaseService):
    """
    Service for Employee operations with business logic validation.

    Wraps EmployeesEndpoint with basic employee validation.
    """

    def _validate_employee_data(self, data: dict) -> None:
        """
        Validate employee data before create/update operations.

        Args:
            data: Employee payload dict

        Raises:
            ValidationError: If required fields are missing
        """
        if not data:
            from loyverse_sdk.exceptions import ValidationError

            raise ValidationError(
                message="Employee data cannot be empty",
                model_name="Employee",
            )

    async def retrieve_employee(self, id: str) -> Employee:
        """
        Retrieve an employee by ID.

        Args:
            id: Employee UUID string

        Returns:
            Employee: The retrieved employee

        Raises:
            NotFoundError: If employee not found
        """
        return await self._client.employees.retrieve(id)

    async def list_employees(self, **kwargs):
        """
        List all employees with optional filtering.

        Args:
            **kwargs: Pagination options (limit, cursor)

        Returns:
            List of Employee objects
        """
        return await self._client.employees.list(**kwargs)

    async def iter_all_employees(self, **kwargs):
        """
        Iterate through all employees using cursor-based pagination.

        Args:
            **kwargs: Options passed to iter_all

        Yields:
            Employee objects
        """
        async for employee in self._client.employees.iter_all(**kwargs):
            yield employee
