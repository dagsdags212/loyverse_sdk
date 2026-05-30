from rich.table import Table

from loyverse_sdk.cli._async import console
from loyverse_sdk.cli._metadata import get_endpoint_classes
from loyverse_sdk.endpoints.mixins import (
    CreateMixin,
    DeleteMixin,
    ListMixin,
    RetrieveMixin,
    UpdateMixin,
)


def _operations(cls: type) -> list[str]:
    ops: list[str] = []
    if issubclass(cls, ListMixin):
        ops.append("list")
    if issubclass(cls, RetrieveMixin):
        ops.append("get")
    if issubclass(cls, CreateMixin):
        ops.append("create")
    if issubclass(cls, UpdateMixin):
        ops.append("update")
    if issubclass(cls, DeleteMixin):
        ops.append("delete")
    return ops


def endpoints() -> None:
    """List all available API endpoints and their supported operations."""
    endpoint_classes = get_endpoint_classes()

    table = Table(title="Loyverse API Endpoints")
    table.add_column("Resource", style="cyan")
    table.add_column("Path", style="green")
    table.add_column("Operations", style="yellow")

    for name, cls in endpoint_classes.items():
        ops = _operations(cls)
        table.add_row(name, f"/{cls.path}", ", ".join(ops))

    console.print(table)
