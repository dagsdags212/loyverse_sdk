from loyverse_api.endpoints.base import BaseEndpoint
from loyverse_api.endpoints.mixins import (
    ListMixin,
    RetrieveMixin,
    PaginationMixin,
)
from loyverse_api.models import Employee, EmployeeListResponse


class EmployeesEndpoint(BaseEndpoint, ListMixin, RetrieveMixin, PaginationMixin):
    path = "employees"

    async def list(self, *, limit: int = 100, cursor: str | None = None):
        return await super().list(
            limit=limit, cursor=cursor, model=EmployeeListResponse
        )

    async def iter_all(self):
        async for item in super().iter_all():
            yield Employee.model_validate(item)

    async def retrieve(self, id: str):
        return await super().retrieve(id, model=Employee)
