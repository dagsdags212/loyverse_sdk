from pathlib import Path

import typer

from loyverse_sdk.cli._async import console


def init() -> None:
    """Set up your Loyverse API token in a .env file."""
    env_path = Path(".env")
    existing_vars: dict[str, str] = {}
    content = ""

    if env_path.exists():
        content = env_path.read_text()
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                existing_vars[key.strip()] = value.strip().strip('"').strip("'")

        if "LOYVERSE_API_TOKEN" in existing_vars:
            console.print("[yellow]LOYVERSE_API_TOKEN is already set.[/yellow]")
            overwrite = typer.confirm("Do you want to overwrite it?")
            if not overwrite:
                console.print("[dim]Keeping existing token.[/dim]")
                return

    token = typer.prompt(
        "Enter your Loyverse API token",
        hide_input=True,
    )
    token = token.strip()
    if not token:
        console.print("[red]Token cannot be empty.[/red]")
        raise typer.Exit(1)

    if "LOYVERSE_API_TOKEN" in existing_vars:
        lines = content.splitlines()
        with open(env_path, "w") as f:
            updated = False
            for line in lines:
                if line.strip().startswith("LOYVERSE_API_TOKEN="):
                    f.write(f"LOYVERSE_API_TOKEN={token}\n")
                    updated = True
                else:
                    f.write(f"{line}\n")
            if not updated:
                f.write(f"LOYVERSE_API_TOKEN={token}\n")
    else:
        with open(env_path, "a") as f:
            if env_path.exists() and env_path.stat().st_size > 0:
                f.write("\n")
            f.write(f"LOYVERSE_API_TOKEN={token}\n")

    console.print("[green]✓  API token saved to .env[/green]")
