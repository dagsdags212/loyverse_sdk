import typer

from loyverse_sdk.cli.commands.create import create_resource
from loyverse_sdk.cli.commands.delete import delete_resource
from loyverse_sdk.cli.commands.endpoints import endpoints
from loyverse_sdk.cli.commands.export_ import export_resources
from loyverse_sdk.cli.commands.get import get_resource
from loyverse_sdk.cli.commands.init import init
from loyverse_sdk.cli.commands.list import list_resources
from loyverse_sdk.cli.commands.update import update_resource
from loyverse_sdk.cli._metadata import make_create_epilog

app = typer.Typer(
    name="loyverse",
    help="Loyverse SDK CLI — interact with the Loyverse API",
    no_args_is_help=True,
)

app.command()(init)

app.command(
    name="list",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)(list_resources)

app.command(
    name="create",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)(create_resource)

app.command(
    name="update",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)(update_resource)

app.command(name="delete")(delete_resource)

app.command(name="get")(get_resource)

app.command(name="endpoints")(endpoints)

app.command(name="export")(export_resources)
