import io
import json
import sys
from collections.abc import Callable

import typer

from loyverse_sdk import LoyverseClient
from loyverse_sdk.cli._async import console, err_console, run_async
from loyverse_sdk.cli._dates import normalize_date
from loyverse_sdk.cli._display import build_table, flatten_for_export, items_key
from loyverse_sdk.cli._metadata import (
    get_listable_resources,
    get_response_model,
)


def _parse_extra_args(args: list[str]) -> dict[str, str]:
    """Parse --key value pairs from unknown CLI arguments."""
    result: dict[str, str] = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith("--") and not arg.startswith("---"):
            key = arg[2:].replace("-", "_")
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                result[key] = args[i + 1]
                i += 2
            else:
                result[key] = "true"
                i += 1
        else:
            i += 1
    return result


async def _fetch_all_pages(
    endpoint,
    params: dict[str, object],
    total_limit: int,
    on_progress: Callable[[int, int], None] | None = None,
) -> dict[str, object]:
    all_items: list[dict] = []
    cursor: str | None = None
    key = items_key(endpoint)
    page_num = 0

    while len(all_items) < total_limit:
        page_num += 1
        call_params = dict(params)
        call_params["limit"] = min(250, total_limit - len(all_items))
        if cursor:
            call_params["cursor"] = cursor

        data = await endpoint._get(endpoint.path, params=call_params)
        page = data.get(key, [])
        if not isinstance(page, list):
            break
        all_items.extend(page)
        if on_progress:
            on_progress(len(all_items), page_num)
        cursor = data.get("cursor")
        if not cursor or not page:
            break

    if len(all_items) > total_limit:
        all_items = all_items[:total_limit]

    return {key: all_items, "cursor": cursor}


def list_resources(
    ctx: typer.Context,
    resource: str,
    limit: int = 250,
    cursor: str | None = None,
    created_at_min: str | None = None,
    created_at_max: str | None = None,
    updated_at_min: str | None = None,
    updated_at_max: str | None = None,
    fmt: str = typer.Option(
        "json",
        "--format",
        "-f",
        help="Output format: json, table, csv, parquet",
    ),
) -> None:
    """List records from a Loyverse API resource.

    Resource-specific query parameters can be passed as extra flags
    (e.g. --email foo@bar.com, --store-id abc123).  Unknown flags
    are forwarded directly to the API.

    \b
    Examples:
        loyverse list customers --limit 10
        loyverse list receipts --created-at-min 2024-01-01T00:00:00Z
        loyverse list items --format table
        loyverse list customers --format csv > customers.csv
        loyverse list customers --email foo@bar.com
    """
    listable = get_listable_resources()
    if resource not in listable:
        valid = "', '".join(sorted(listable))
        console.print(f"[red]Unknown resource '{resource}'.[/red] Valid: '{valid}'")
        raise typer.Exit(1)

    fmt = fmt.lower()
    if fmt not in ("json", "table", "csv", "parquet"):
        console.print(f"[red]Invalid --format '{fmt}'[/red]")
        raise typer.Exit(1)

    extra_params = _parse_extra_args(ctx.args)

    params: dict[str, object] = {}
    if created_at_min:
        params["created_at_min"] = normalize_date(created_at_min)
    if created_at_max:
        params["created_at_max"] = normalize_date(created_at_max, end_of_day=True)
    if updated_at_min:
        params["updated_at_min"] = normalize_date(updated_at_min)
    if updated_at_max:
        params["updated_at_max"] = normalize_date(updated_at_max, end_of_day=True)
    params.update(extra_params)

    async def _run(client: LoyverseClient) -> None:
        endpoint = getattr(client, resource)
        status_console = err_console if fmt in ("csv", "parquet") else console

        with status_console.status(
            f"[bold]Fetching {resource}…[/bold]", spinner="dots"
        ) as status:
            if limit <= 250:
                call_params = dict(params)
                call_params["limit"] = limit
                if cursor:
                    call_params["cursor"] = cursor
                raw = await endpoint._get(endpoint.path, params=call_params)
            else:

                def _progress(count: int, page: int) -> None:
                    status.update(
                        f"[bold]Fetching {resource}…[/bold] "
                        f"page {page}, {count} records"
                    )

                raw = await _fetch_all_pages(
                    endpoint, params, limit, on_progress=_progress
                )

        response_model = get_response_model(resource)
        validated = response_model.model_validate(raw)
        items = validated.items

        if fmt == "json":
            console.print(json.dumps(raw, indent=2, default=str))
        elif fmt == "table":
            if not items:
                console.print(f"[dim]No {resource} found.[/dim]")
            else:
                console.print(build_table(items))
            next_cursor = raw.get("cursor")
            if next_cursor:
                console.print(
                    f"[dim]Next cursor: {next_cursor}  "
                    f"(use --cursor to fetch the next page)[/dim]"
                )
        elif fmt == "csv":
            if items:
                import polars as pl

                df = pl.DataFrame(flatten_for_export(items))
                buf = io.StringIO()
                df.write_csv(buf)
                sys.stdout.write(buf.getvalue())
            err_console.print(
                f"[dim]{len(items)} record{'s' if len(items) != 1 else ''}[/dim]"
            )
        elif fmt == "parquet":
            if items:
                if sys.stdout.isatty():
                    err_console.print(
                        "[yellow]Warning: writing binary Parquet to terminal. "
                        "Use '> file.parquet' to redirect.[/yellow]"
                    )

                import polars as pl

                df = pl.DataFrame(flatten_for_export(items))
                buf = io.BytesIO()
                df.write_parquet(buf)
                data = buf.getvalue()
                sys.stdout.flush()
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            err_console.print(
                f"[dim]{len(items)} record{'s' if len(items) != 1 else ''}[/dim]"
            )

    run_async(_run)
