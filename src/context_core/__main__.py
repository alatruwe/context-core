import typer
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# Create the Typer app
app = typer.Typer()

VALID_CONTEXT_TYPES = [
    "facts", "decisions", "goals",
    "instructions", "actions", "summaries",
    "archives", "personas", "timeline"
]


# ──────────────────────────────────────────────────────────────
# CLI COMMAND: hello
# Say hello to confirm the CLI works
# ──────────────────────────────────────────────────────────────
@app.command()
def hello():
    """Say hello!"""
    typer.echo("👋 Hello from Context Utility!")


def safe_prompt(prompt_text: str) -> str:
    value = typer.prompt(prompt_text)
    if value.strip().lower() == "exit":
        typer.echo("👋 Exiting walkthrough. No changes made.")
        raise typer.Exit()
    return value


# ──────────────────────────────────────────────────────────────
# CLI COMMAND: init-project
# Initializes a new project with folder structure and metadata
# ──────────────────────────────────────────────────────────────
@app.command("init-project")
def init_project(project_name: str):
    """
    Initialize a new context project with folders and metadata.
    """
    base_path = Path("projects_data") / project_name

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
    base_path = Path("projects_data") / project_name

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
    if type not in VALID_CONTEXT_TYPES:
        typer.echo(f"❌ '{type}' is not a valid context type.")
        typer.echo("📂 Valid types:")
        for t in VALID_CONTEXT_TYPES:
            typer.echo(f"  - {t}")
        raise typer.Exit(code=1)

    base_path = Path("projects_data") / project / type
    file_path = base_path / f"{name}.md"

    if not base_path.exists():
        typer.echo(f"❌ The folder '{base_path}' does not exist. Did you run `init`?")
        raise typer.Exit(code=1)

    if file_path.exists():
        typer.echo(f"⚠️ File '{file_path}' already exists.")
        raise typer.Exit(code=1)

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
    file_path = Path("projects_data") / project / type / f"{name}.md"

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
    file_path = Path("projects_data") / project / type / f"{name}.md"

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
    file_path = Path("projects_data") / project / type / f"{name}.md"

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
    project_path = Path("projects_data") / project

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

@app.command("walkthrough")
def walkthrough():
    """
    Show a step-by-step example of setting up a project, then optionally walk the user through it interactively.
    """
    typer.echo("👋 Welcome to Context Utility!\n")
    typer.echo("Let’s walk through how to set up your first project and context file.\n")

    typer.echo("🔧 Step 1: Initialize your project")
    typer.echo("  $ context init my-first-project")
    typer.echo("  ✅ Project 'my-first-project' initialized with standard folders.\n")

    typer.echo("🗂️ Step 2: Create your first context file")
    typer.echo("  $ context create-context my-first-project facts first-notes")
    typer.echo("  ✅ Created file: projects_data/my-first-project/facts/first-notes.md\n")

    typer.echo("✏️ Step 3: Edit the file (optional)")
    typer.echo("  $ context edit-context my-first-project facts first-notes")
    typer.echo("  (opens in your default editor like nano or VS Code)\n")

    typer.echo("📋 Step 4: View your context files")
    typer.echo("  $ context list-contexts my-first-project")
    typer.echo("  📂 facts/")
    typer.echo("    - first-notes.md\n")

    typer.echo("🚀 That’s it! You’re now ready to work with structured context.\n")

    confirm = typer.confirm("Would you like to create your first project now?", default=True)
    if confirm:
        typer.echo("\nLaunching interactive setup...\n")
        # Reuse the real setup logic from the earlier interactive walkthrough
        _run_walkthrough_interactive()
    else:
        typer.echo("👋 No problem. You can run this again anytime with `context walkthrough`.")

def _run_walkthrough_interactive():
    while True:
        project = safe_prompt("📁 Project name (use dashes or underscores, no spaces)")
        if " " in project:
            typer.echo("❌ Project names cannot contain spaces.")
            typer.echo("👉 Use dashes or underscores instead, like `my-project` or `client_data`.\n")
        else:
            break

    base_path = Path("projects_data") / project

    if base_path.exists():
        typer.echo(f"⚠️ Project '{project}' already exists. Skipping init.")
    else:
        subfolders = [
            "facts", "decisions", "goals",
            "instructions", "actions", "summaries",
            "archives", "personas", "timeline"
        ]
        for folder in subfolders:
            (base_path / folder).mkdir(parents=True, exist_ok=True)
        meta = {
            "project": project,
            "created": datetime.now().isoformat(),
            "context_types": subfolders
        }
        with open(base_path / "meta.json", "w") as f:
            json.dump(meta, f, indent=2)
        typer.echo(f"✅ Project '{project}' initialized.\n")

    typer.echo("📂 Available context types:")
    for t in VALID_CONTEXT_TYPES:
        typer.echo(f"  - {t}")

    context_type = safe_prompt("\n📂 Choose a context type")
    while context_type not in VALID_CONTEXT_TYPES:
        typer.echo(f"❌ '{context_type}' is not a valid type.")
        context_type = safe_prompt("📂 Try again (e.g. facts, goals)")

    file_name = safe_prompt("📝 Context file name (without .md)")

    file_path = base_path / context_type / f"{file_name}.md"
    if file_path.exists():
        typer.echo(f"⚠️ File '{file_path}' already exists. Skipping create.")
    else:
        title = file_name.replace("-", " ").title()
        content = f"# {title}\n\nCreated on {datetime.now().isoformat()}\n"
        file_path.write_text(content)
        typer.echo(f"✅ Created file: {file_path}")

    open_now = typer.confirm("✏️ Do you want to open it now?", default=True)
    if open_now:
        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(file_path)])

    typer.echo("\n🚀 You’re ready! Use:")
    typer.echo(f"  context list-contexts {project}")


# ──────────────────────────────────────────────────────────────
# Main entry point for running with `python -m context_core`
# ──────────────────────────────────────────────────────────────
def main():
    app()

if __name__ == "__main__":
    main()
