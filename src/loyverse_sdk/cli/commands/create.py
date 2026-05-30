import json

import typer

from loyverse_sdk import LoyverseClient
from loyverse_sdk.cli._async import console, err_console, run_async
from loyverse_sdk.cli._metadata import (
    get_creatable_resources,
    get_required_fields,
    make_create_epilog,
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


def create_resource(
    ctx: typer.Context,
    resource: str,
) -> None:
    """Create a new resource record via the Loyverse API.

    Pass fields as --flag value pairs.  Required fields depend on the
    resource type and are validated client-side before the API call.

    \b
    Examples:
        loyverse create categories --name "Drinks" --color GREEN
        loyverse create customers --name "Jane" --email jane@acme.com
        loyverse create discounts --type FIXED_AMOUNT --name "10 off" --amount 10
        loyverse create items --item-name "Latte"
        loyverse create pos_devices --name "Front" --store-id <UUID>
        loyverse create receipts --store-id <UUID>
        loyverse create suppliers --name "Acme Inc"
        loyverse create taxes --type INCLUDED --name "VAT" --rate 12
        loyverse create webhooks --url "https://…" --type items.update
        loyverse create variants --item-id <UUID> --sku "LATTE-M"
    """
    creatable = get_creatable_resources()
    if resource not in creatable:
        valid = "', '".join(sorted(creatable))
        console.print(f"[red]Cannot create '{resource}'.[/red] Creatable: '{valid}'")
        raise typer.Exit(1)

    payload = _parse_extra_args(ctx.args)

    missing = [f for f in get_required_fields(resource) if f not in payload]
    if missing:
        console.print(
            f"[red]Missing required fields for '{resource}': "
            f"{', '.join('--' + m for m in missing)}[/red]"
        )
        raise typer.Exit(1)

    async def _run(client: LoyverseClient) -> None:
        endpoint = getattr(client, resource)

        with err_console.status(f"[bold]Creating {resource}…[/bold]", spinner="dots"):
            raw = await endpoint.create(payload=payload)

        console.print(json.dumps(raw, indent=2, default=str))

    run_async(_run)


create_resource.__doc__ = create_resource.__doc__ + "\n\n\b\n" + make_create_epilog()
