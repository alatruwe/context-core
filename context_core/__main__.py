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
@app.command("init-project")
def init_project(project_name: str):
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
# CLI COMMAND: create
# Create a new context file in a given project and type folder
# ──────────────────────────────────────────────────────────────
@app.command("create-context")
def create_context(project: str, type: str, name: str):
    """
    Create a new context file in a project (e.g. facts/my-topic.md).
    """
    base_path = Path("context_data") / project / type
    file_path = base_path / f"{name}.md"

    if not base_path.exists():
        typer.echo(f"❌ The folder '{base_path}' does not exist. Did you run `init`?")
        raise typer.Exit(code=1)

    if file_path.exists():
        typer.echo(f"⚠️ File '{file_path}' already exists.")
        raise typer.Exit(code=1)

    # Create the file with a simple template
    title = name.replace("-", " ").title()
    content = f"# {title}\n\nCreated on {datetime.now().isoformat()}\n"
    file_path.write_text(content)

    typer.echo(f"✅ Created file: {file_path}")

# ──────────────────────────────────────────────────────────────
# CLI COMMAND: delete
# Delete a context file from a project
# ──────────────────────────────────────────────────────────────
@app.command("delete-context")
def delete_context(project: str, type: str, name: str, force: bool = typer.Option(False, "--force", help="Skip confirmation")):
    """
    Delete a context file from a project (e.g. facts/my-topic.md).
    """
    file_path = Path("context_data") / project / type / f"{name}.md"

    if not file_path.exists():
        typer.echo(f"❌ File '{file_path}' does not exist.")
        raise typer.Exit(code=1)

    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete '{file_path}'?")
        if not confirm:
            typer.echo("❎ Cancelled.")
            raise typer.Exit(code=1)

    file_path.unlink()
    typer.echo(f"🗑️ Deleted file: {file_path}")


# ──────────────────────────────────────────────────────────────
# Main entry point for running with `python -m context_core`
# ──────────────────────────────────────────────────────────────
def main():
    app()

if __name__ == "__main__":
    main()
