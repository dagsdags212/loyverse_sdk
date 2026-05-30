import json

import typer

from loyverse_sdk import LoyverseClient
from loyverse_sdk.cli._async import console, err_console, run_async
from loyverse_sdk.cli._metadata import get_updatable_resources


def _parse_extra_args(args: list[str]) -> dict[str, str]:
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


def update_resource(
    ctx: typer.Context,
    resource: str,
    id: str,
    yes: bool = False,
) -> None:
    """Update an existing resource record.

    Pass the fields to change as --flag value pairs.

    \b
    Examples:
        loyverse update categories <ID> --name "New Name"
        loyverse update customers <ID> --email new@acme.com
        loyverse update items <ID> --item-name "New Item Name"
        loyverse update receipts <ID> --note "Updated note"
    """
    updatable = get_updatable_resources()
    if resource not in updatable:
        valid = "', '".join(sorted(updatable))
        console.print(f"[red]Cannot update '{resource}'.[/red] Updatable: '{valid}'")
        raise typer.Exit(1)

    fields = _parse_extra_args(ctx.args)
    if not fields:
        console.print("[red]No update fields provided.[/red]")
        raise typer.Exit(1)

    if not yes:
        console.print(
            f"\n[bold]Update [cyan]{resource}[/cyan] [yellow]{id}[/yellow]:[/bold]"
        )
        for k, v in fields.items():
            console.print(f"  {k}: [green]{v}[/green]")
        confirmed = typer.confirm("\nProceed with update?")
        if not confirmed:
            console.print("[dim]Cancelled.[/dim]")
            raise typer.Exit(0)

    async def _run(client: LoyverseClient) -> None:
        endpoint = getattr(client, resource)

        with err_console.status(f"[bold]Updating {resource}…[/bold]", spinner="dots"):
            result = await endpoint.update(id=id, payload=dict(fields))

        console.print(
            json.dumps(
                result.model_dump() if hasattr(result, "model_dump") else result,
                indent=2,
                default=str,
            )
        )

    run_async(_run)
