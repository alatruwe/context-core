import typer
import os
import json
import subprocess
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
# CLI COMMAND: init-project
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
# CLI COMMAND: create-context
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
# CLI COMMAND: delete-context
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
# CLI COMMAND: edit-context
# Edit a context file in your system editor
# ──────────────────────────────────────────────────────────────
@app.command("edit-context")
def edit_context(project: str, type: str, name: str):
    """
    Edit a context file in your default system editor (e.g. nano, code).
    """
    file_path = Path("context_data") / project / type / f"{name}.md"

    if not file_path.exists():
        typer.echo(f"❌ File '{file_path}' does not exist.")
        raise typer.Exit(code=1)

    editor = os.environ.get("EDITOR", "nano")
    subprocess.run([editor, str(file_path)])

# ──────────────────────────────────────────────────────────────
# CLI COMMAND: view-context
# Print the contents of a context file to the terminal
# ──────────────────────────────────────────────────────────────
@app.command("view-context")
def view_context(project: str, type: str, name: str, pager: bool = typer.Option(False, "--pager", help="Use a pager like 'less' to view the file")):
    """
    View the contents of a context file.
    """
    file_path = Path("context_data") / project / type / f"{name}.md"

    if not file_path.exists():
        typer.echo(f"❌ File '{file_path}' does not exist.")
        raise typer.Exit(code=1)

    content = file_path.read_text()

    if pager:
        pager_process = subprocess.Popen(["less"], stdin=subprocess.PIPE)
        pager_process.communicate(input=content.encode())
    else:
        typer.echo(content)

# ──────────────────────────────────────────────────────────────
# CLI COMMAND: list-contexts
# List context files in a project, optionally filtered by type
# ──────────────────────────────────────────────────────────────
@app.command("list-contexts")
def list_contexts(project: str, type: str = typer.Argument(None, help="Optional context type (e.g. facts, goals)")):
    """
    List context files in a project. If a type is provided, only list that folder.
    """
    project_path = Path("context_data") / project

    if not project_path.exists():
        typer.echo(f"❌ Project '{project}' does not exist.")
        raise typer.Exit(code=1)

    if type:
        type_path = project_path / type
        if not type_path.exists():
            typer.echo(f"❌ Context type '{type}' does not exist in project '{project}'.")
            raise typer.Exit(code=1)

        files = sorted(type_path.glob("*.md"))
        if not files:
            typer.echo(f"📂 No context files found in '{type}/'")
        else:
            typer.echo(f"📂 {type}/")
            for file in files:
                typer.echo(f"  - {file.name}")
    else:
        found = False
        for folder in sorted(project_path.iterdir()):
            if folder.is_dir():
                files = sorted(folder.glob("*.md"))
                if files:
                    found = True
                    typer.echo(f"📂 {folder.name}/")
                    for file in files:
                        typer.echo(f"  - {file.name}")
        if not found:
            typer.echo(f"📦 No context files found in project '{project}'.")


# ──────────────────────────────────────────────────────────────
# Main entry point for running with `python -m context_core`
# ──────────────────────────────────────────────────────────────
def main():
    app()

if __name__ == "__main__":
    main()
