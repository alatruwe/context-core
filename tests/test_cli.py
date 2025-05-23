import os
import shutil
import subprocess
from pathlib import Path
from typer.testing import CliRunner
from unittest.mock import patch
from context_core.__main__ import app
from typer import Typer

runner = CliRunner()
DATA_DIR = Path("context_data")


def test_hello_command():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "👋 Hello from Context Utility!" in result.output

# INIT PROJECT TESTS
def test_init_creates_project_structure():
    project_name = "test-project"
    project_path = DATA_DIR / project_name

    # Clean before test
    if project_path.exists():
        shutil.rmtree(project_path)

    result = runner.invoke(app, ["init-project", project_name])
    assert result.exit_code == 0
    assert project_path.exists()
    assert (project_path / "facts").exists()
    assert (project_path / "meta.json").exists()
    assert "✅ Initialized project" in result.output

    # Clean up after
    shutil.rmtree(project_path)

def test_init_fails_if_project_exists():
    project_name = "test-existing"
    project_path = DATA_DIR / project_name

    # Clean up before test
    if project_path.exists():
        shutil.rmtree(project_path)

    # First run: create the project
    result1 = runner.invoke(app, ["init-project", project_name])
    assert result1.exit_code == 0
    assert project_path.exists()

    # Second run: try to re-create it
    result2 = runner.invoke(app, ["init-project", project_name])
    assert result2.exit_code != 0
    assert "already exists" in result2.output

    # Clean up
    shutil.rmtree(project_path)

def test_init_fails_without_project_name():
    result = runner.invoke(app, ["init-project"])
    assert result.exit_code != 0
    assert "Usage:" in result.output or "Missing argument" in result.output

# DELETE PROJECT TESTS
def test_delete_project_command():
    project_name = "test-delete"
    project_path = DATA_DIR / project_name

    # Setup: manually create a dummy project
    (project_path / "facts").mkdir(parents=True, exist_ok=True)
    (project_path / "meta.json").write_text("{}")

    assert project_path.exists()

    # Use --force to skip confirmation
    result = runner.invoke(app, ["delete-project", project_name, "--force"])
    assert result.exit_code == 0
    assert not project_path.exists()
    assert "🗑️ Deleted project" in result.output

def test_delete_project_fails_if_missing():
    project_name = "nonexistent-project"
    project_path = DATA_DIR / project_name

    # Ensure it really doesn't exist
    if project_path.exists():
        shutil.rmtree(project_path)

    result = runner.invoke(app, ["delete-project", project_name, "--force"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_delete_project_cancelled_on_prompt():
    project_name = "test-cancel"
    project_path = DATA_DIR / project_name

    # Setup dummy project
    (project_path / "facts").mkdir(parents=True, exist_ok=True)

    # Simulate user typing 'n' when prompted
    result = runner.invoke(app, ["delete-project", project_name], input="n\n")

    assert result.exit_code != 0
    assert "❎ Cancelled." in result.output
    assert project_path.exists()

    shutil.rmtree(project_path)

def test_delete_project_confirmed_prompt():
    project_name = "test-confirm"
    project_path = DATA_DIR / project_name

    (project_path / "facts").mkdir(parents=True, exist_ok=True)

    result = runner.invoke(app, ["delete-project", project_name], input="y\n")
    assert result.exit_code == 0
    assert not project_path.exists()
    assert "🗑️ Deleted project" in result.output

# CREATE FILE TESTS
def test_create_context_file():
    project_name = "test-create"
    project_path = DATA_DIR / project_name
    facts_path = project_path / "facts"
    file_path = facts_path / "my-topic.md"

    # Ensure clean start
    if project_path.exists():
        shutil.rmtree(project_path)

    runner.invoke(app, ["init-project", project_name])
    result = runner.invoke(app, ["create-context", project_name, "facts", "my-topic"])

    assert result.exit_code == 0
    assert file_path.exists()
    assert "✅ Created file" in result.output
    assert "# My Topic" in file_path.read_text()

    shutil.rmtree(project_path)

def test_create_context_file_already_exists():
    project = "test-duplicate"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "duplicate-topic"])

    result = runner.invoke(app, ["create-context", project, "facts", "duplicate-topic"])
    assert result.exit_code != 0
    assert "already exists" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_create_context_missing_folder():
    project = "nonexistent-project"
    result = runner.invoke(app, ["create-context", project, "facts", "missing-folder-test"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_create_context_invalid_characters():
    project = "test-invalid-chars"
    runner.invoke(app, ["init-project", project])

    result = runner.invoke(app, ["create-context", project, "facts", "bad@name!"])
    assert result.exit_code == 0  # Should still allow file creation
    file_path = DATA_DIR / project / "facts" / "bad@name!.md"
    assert file_path.exists()
    assert "# Bad@Name!" in file_path.read_text()

    shutil.rmtree(DATA_DIR / project)

def test_create_context_invalid_type():
    project = "test-invalid-type"
    runner.invoke(app, ["init-project", project])

    result = runner.invoke(app, ["create-context", project, "fake-type", "test-note"])
    assert result.exit_code != 0
    assert "is not a valid context type" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_create_context_template_format():
    project = "test-template"
    runner.invoke(app, ["init-project", project])

    result = runner.invoke(app, ["create-context", project, "facts", "test-format"])
    file_path = DATA_DIR / project / "facts" / "test-format.md"
    content = file_path.read_text()

    assert "# Test Format" in content
    assert "Created on" in content

    shutil.rmtree(DATA_DIR / project)


# DELETE FILE TESTS
def test_delete_context_file():
    project_name = "test-delete-context"
    project_path = DATA_DIR / project_name
    facts_path = project_path / "facts"
    file_path = facts_path / "delete-me.md"

    # Setup
    runner.invoke(app, ["init-project", project_name])
    runner.invoke(app, ["create-context", project_name, "facts", "delete-me"])
    assert file_path.exists()

    # Delete with --force
    result = runner.invoke(app, ["delete-context", project_name, "facts", "delete-me", "--force"])

    assert result.exit_code == 0
    assert not file_path.exists()
    assert "🗑️ Deleted file" in result.output

    shutil.rmtree(project_path)

def test_delete_context_file_does_not_exist():
    project = "test-delete-missing"
    runner.invoke(app, ["init-project", project])
    result = runner.invoke(app, ["delete-context", project, "facts", "not-there", "--force"])

    assert result.exit_code != 0
    assert "does not exist" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_delete_context_prompt_rejection():
    project = "test-prompt-reject"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "keep-me"])

    file_path = DATA_DIR / project / "facts" / "keep-me.md"
    result = runner.invoke(app, ["delete-context", project, "facts", "keep-me"], input="n\n")

    assert result.exit_code != 0
    assert "❎ Cancelled." in result.output
    assert file_path.exists()

    shutil.rmtree(DATA_DIR / project)

def test_delete_context_prompt_confirmation():
    project = "test-prompt-confirm"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "go-ahead"])

    file_path = DATA_DIR / project / "facts" / "go-ahead.md"
    result = runner.invoke(app, ["delete-context", project, "facts", "go-ahead"], input="y\n")

    assert result.exit_code == 0
    assert "🗑️ Deleted file" in result.output
    assert not file_path.exists()

    shutil.rmtree(DATA_DIR / project)

def test_delete_context_folder_remains_after_file_deletion():
    project = "test-folder-persists"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "one-file"])

    file_path = DATA_DIR / project / "facts" / "one-file.md"
    result = runner.invoke(app, ["delete-context", project, "facts", "one-file", "--force"])

    assert result.exit_code == 0
    assert not file_path.exists()
    assert (DATA_DIR / project / "facts").exists()

    shutil.rmtree(DATA_DIR / project)

# EDIT FILE TESTS
def test_edit_context_opens_editor():
    project = "test-edit"
    file_path = DATA_DIR / project / "facts" / "edit-me.md"

    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "edit-me"])
    assert file_path.exists()  # ensure file was created

    with patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["edit-context", project, "facts", "edit-me"])
        assert result.exit_code == 0, result.output
        mock_run.assert_called_once()
        assert str(file_path) in mock_run.call_args[0][0]

    shutil.rmtree(DATA_DIR / project)

def test_edit_context_fails_if_missing():
    project = "test-edit-missing"
    result = runner.invoke(app, ["edit-context", project, "facts", "nope"])

    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_edit_context_respects_editor_env():
    project = "test-edit-env"
    file_path = DATA_DIR / project / "facts" / "env-editor.md"


    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "env-editor"])
    assert file_path.exists()  # ensure file was created

    with patch.dict(os.environ, {"EDITOR": "mock-editor"}), patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["edit-context", project, "facts", "env-editor"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0][0] == "mock-editor"

    shutil.rmtree(DATA_DIR / project)

def test_edit_context_falls_back_to_nano():
    project = "test-edit-fallback"
    file_path = DATA_DIR / project / "facts" / "fallback-editor.md"

    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "fallback-editor"])
    assert file_path.exists()  # ensure file was created

    # Clear EDITOR env for this test
    with patch.dict(os.environ, {}, clear=True), patch("subprocess.run") as mock_run:
        result = runner.invoke(app, ["edit-context", project, "facts", "fallback-editor"])
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert mock_run.call_args[0][0][0] == "nano"

    shutil.rmtree(DATA_DIR / project)

# VIEW FILE TESTS
def test_view_context_prints_file_contents():
    project = "test-view"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "view-me"])
    file_path = DATA_DIR / project / "facts" / "view-me.md"
    file_path.write_text("Hello from view test!\n")

    result = runner.invoke(app, ["view-context", project, "facts", "view-me"])
    assert result.exit_code == 0
    assert "Hello from view test!" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_view_context_fails_on_missing_file():
    project = "test-view-missing"
    result = runner.invoke(app, ["view-context", project, "facts", "nope"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_view_context_uses_pager():
    project = "test-view-pager"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "paged"])
    file_path = DATA_DIR / project / "facts" / "paged.md"
    file_path.write_text("Content to be paged\n")

    with patch("subprocess.Popen") as mock_popen:
        mock_process = mock_popen.return_value
        mock_process.communicate.return_value = (None, None)

        result = runner.invoke(app, ["view-context", project, "facts", "paged", "--pager"])
        assert result.exit_code == 0
        mock_popen.assert_called_once_with(["less"], stdin=subprocess.PIPE)
        mock_process.communicate.assert_called_once()

    shutil.rmtree(DATA_DIR / project)

# LIST FILES TESTS
def test_list_contexts_by_type():
    project = "test-list-type"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "file-one"])
    runner.invoke(app, ["create-context", project, "facts", "file-two"])

    result = runner.invoke(app, ["list-contexts", project, "facts"])
    assert result.exit_code == 0
    assert "📂 facts/" in result.output
    assert "file-one.md" in result.output
    assert "file-two.md" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_list_contexts_whole_project():
    project = "test-list-all"
    runner.invoke(app, ["init-project", project])
    runner.invoke(app, ["create-context", project, "facts", "a"])
    runner.invoke(app, ["create-context", project, "goals", "b"])
    runner.invoke(app, ["create-context", project, "decisions", "c"])

    result = runner.invoke(app, ["list-contexts", project])
    assert result.exit_code == 0
    assert "📂 facts/" in result.output
    assert "a.md" in result.output
    assert "📂 goals/" in result.output
    assert "b.md" in result.output
    assert "📂 decisions/" in result.output
    assert "c.md" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_list_contexts_type_not_found():
    project = "test-list-missing-type"
    runner.invoke(app, ["init-project", project])

    result = runner.invoke(app, ["list-contexts", project, "fake-type"])
    assert result.exit_code != 0
    assert "does not exist" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_list_contexts_project_not_found():
    project = "not-a-project"
    result = runner.invoke(app, ["list-contexts", project])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_list_contexts_type_no_files():
    project = "test-empty-type"
    runner.invoke(app, ["init-project", project])  # creates empty folders

    result = runner.invoke(app, ["list-contexts", project, "facts"])
    assert result.exit_code == 0
    assert "No context files found in 'facts/'" in result.output

    shutil.rmtree(DATA_DIR / project)

def test_list_contexts_project_no_files():
    project = "test-empty-project"
    runner.invoke(app, ["init-project", project])  # creates empty folders

    result = runner.invoke(app, ["list-contexts", project])
    assert result.exit_code == 0
    assert f"No context files found in project '{project}'" in result.output

    shutil.rmtree(DATA_DIR / project)

# WALKTHROUGH TESTS
def test_walkthrough_preview_only():
    result = runner.invoke(app, ["walkthrough"], input="n\n")
    assert result.exit_code == 0
    assert "context init my-first-project" in result.output
    assert "Would you like to create your first project now?" in result.output

def test_walkthrough_triggers_interactive():
    with patch("context_core.__main__._run_walkthrough_interactive") as mock_run:
        result = runner.invoke(app, ["walkthrough"], input="y\n")
        assert result.exit_code == 0
        mock_run.assert_called_once()
        assert "Launching interactive setup..." in result.output

def test_run_walkthrough_interactive_flow():
    inputs = "\n".join([
        "test-walkthrough-project",  # project name
        "facts",                     # context type
        "quickstart-notes",         # file name
        "n"                          # don't open editor
    ]) + "\n"

    result = runner.invoke(app, ["walkthrough"], input="y\n" + inputs)

    assert result.exit_code == 0
    assert "Project 'test-walkthrough-project' initialized" in result.output
    assert "Created file" in result.output
    assert "You’re ready!" in result.output

    shutil.rmtree(DATA_DIR / "test-walkthrough-project")
