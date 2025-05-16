import shutil
from pathlib import Path
from typer.testing import CliRunner
from context_core.__main__ import app

runner = CliRunner()
DATA_DIR = Path("context_data")


def test_hello_command():
    result = runner.invoke(app, ["hello"])
    assert result.exit_code == 0
    assert "👋 Hello from Context Utility!" in result.output


def test_init_creates_project_structure():
    project_name = "test-project"
    project_path = DATA_DIR / project_name

    # Clean before test
    if project_path.exists():
        shutil.rmtree(project_path)

    result = runner.invoke(app, ["init", project_name])
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
    result1 = runner.invoke(app, ["init", project_name])
    assert result1.exit_code == 0
    assert project_path.exists()

    # Second run: try to re-create it
    result2 = runner.invoke(app, ["init", project_name])
    assert result2.exit_code != 0
    assert "already exists" in result2.output

    # Clean up
    shutil.rmtree(project_path)


def test_init_fails_without_project_name():
    result = runner.invoke(app, ["init"])
    assert result.exit_code != 0
    assert "Usage:" in result.output or "Missing argument" in result.output


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
