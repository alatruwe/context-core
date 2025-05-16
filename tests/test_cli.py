import shutil
from pathlib import Path
from typer.testing import CliRunner
from context_core.__main__ import app

runner = CliRunner()
DATA_DIR = Path("context_data")


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
