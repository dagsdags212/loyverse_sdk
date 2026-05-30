from datetime import datetime

import pytz
import typer

from loyverse_sdk import LoyverseClient
from loyverse_sdk.cli._async import console, err_console, run_async
from loyverse_sdk.cli._dates import normalize_date
from loyverse_sdk.cli._metadata import get_listable_resources
from loyverse_sdk.exceptions import ExportError


def export_resources(
    db_path: str = typer.Option(
        ...,
        "--db-path",
        "-d",
        help="Path to the DuckDB database file",
    ),
    resource: str | None = typer.Option(
        None,
        "--resource",
        "-r",
        help="Export a single resource (omit for all resources)",
    ),
    created_at_min: str | None = typer.Option(
        None,
        "--created-at-min",
        help="Earliest created_at (ISO-8601, YYYY-MM-DD, today, yesterday)",
    ),
    created_at_max: str | None = typer.Option(
        None,
        "--created-at-max",
        help="Latest created_at (ISO-8601, YYYY-MM-DD, today, yesterday)",
    ),
    batch_size: int = typer.Option(
        1000,
        "--batch-size",
        "-b",
        help="Records to insert per transaction",
    ),
    no_indexes: bool = typer.Option(
        False,
        "--no-indexes",
        help="Skip index creation after export",
    ),
) -> None:
    """Export API data to a local DuckDB database for analytics.

    \b
    Examples:
        loyverse export --db-path loyverse.duckdb
        loyverse export --db-path loyverse.duckdb --resource receipts
        loyverse export --db-path loyverse.duckdb --created-at-min 2024-01-01
    """
    resources: list[str] | None = None
    if resource:
        listable = get_listable_resources()
        if resource not in listable:
            valid = "', '".join(sorted(listable))
            console.print(f"[red]Unknown resource '{resource}'.[/red] Valid: '{valid}'")
            raise typer.Exit(1)
        resources = [resource]

    def _progress(resource_name: str, current: int, total: int) -> None:
        err_console.print(f"[dim]{resource_name}: {current}/{total}[/dim]")

    def _parse_date(value: str) -> datetime:
        normalized = normalize_date(value)
        dt = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
        return dt.astimezone(pytz.utc).replace(tzinfo=None)

    kwargs: dict = {
        "db_path": db_path,
        "batch_size": batch_size,
        "create_indexes": not no_indexes,
        "progress_callback": _progress,
    }
    if created_at_min:
        kwargs["created_at_min"] = _parse_date(created_at_min)
    if created_at_max:
        kwargs["created_at_max"] = _parse_date(created_at_max)

    if resources:
        kwargs["resources"] = resources

    async def _run(client: LoyverseClient) -> None:
        try:
            counts = await client.export_to_duckdb(**kwargs)
        except ExportError as e:
            console.print(f"[red]Export failed: {e}[/red]")
            raise typer.Exit(1)

        total = sum(counts.values())
        console.print(f"[green]✓  Exported {total} records to {db_path}[/green]")
        for name, count in sorted(counts.items()):
            console.print(f"  {name}: {count}")

    run_async(_run)
