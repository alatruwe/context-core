import typer
import os
import json
from datetime import datetime
from pathlib import Path

# Create the Typer app
app = typer.Typer()

# ──────────────────────────────────────────────────────────────
# CLI COMMAND: hello
# Say hello to confirm the CLI works
# ──────────────────────────────────────────────────────────────
@app.command()
def hello():
    """Say hello!"""
    typer.echo("👋 Hello from Context Utility!")


# ──────────────────────────────────────────────────────────────
# CLI COMMAND: init
# Initializes a new project with folder structure and metadata
# ──────────────────────────────────────────────────────────────
@app.command()
def init(project_name: str):
    """
    Initialize a new context project with folders and metadata.
    """
    base_path = Path("context_data") / project_name

    # Define the standard context subfolders
    subfolders = [
        "facts", "decisions", "goals",
        "instructions", "actions", "summaries",
        "archives", "personas", "timeline"
    ]

    # Prevent overwriting an existing project
    if base_path.exists():
        typer.echo(f"⚠️ Project '{project_name}' already exists.")
        raise typer.Exit(code=1)

    # Create the project folder and each subfolder
    for folder in subfolders:
        folder_path = base_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)

    # Create a metadata file for the project
    meta = {
        "project": project_name,
        "created": datetime.now().isoformat(),
        "context_types": subfolders
    }
    with open(base_path / "meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    typer.echo(f"✅ Initialized project at {base_path}")

# ──────────────────────────────────────────────────────────────
# CLI COMMAND: delete-project
# Delete a project and all its context folders and files.
# ──────────────────────────────────────────────────────────────
@app.command("delete-project")
def delete_project(project_name: str, force: bool = typer.Option(False, "--force", help="Skip confirmation")):
    """
    Delete a project and all its context folders and files.
    """
    base_path = Path("context_data") / project_name

    if not base_path.exists():
        typer.echo(f"❌ Project '{project_name}' does not exist.")
        raise typer.Exit(code=1)

    # Confirm deletion unless --force is used
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete the project '{project_name}' and all its data?")
        if not confirm:
            typer.echo("❎ Cancelled.")
            raise typer.Exit(code=1)

    # Recursively delete the project folder
    import shutil
    shutil.rmtree(base_path)
    typer.echo(f"🗑️ Deleted project '{project_name}' and all contents.")

# ──────────────────────────────────────────────────────────────
# Main entry point for running with `python -m context_core`
# ──────────────────────────────────────────────────────────────
def main():
    app()

if __name__ == "__main__":
    main()
