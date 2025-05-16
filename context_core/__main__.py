import typer

app = typer.Typer()

@app.command()
def hello():
    """Say hello!"""
    typer.echo("👋 Hello from Context Utility!")

@app.command()
def init(project_name: str):
    """Initialize a context project."""
    typer.echo(f"🚀 Initialized context project: {project_name}")

def main():
    app()

if __name__ == "__main__":
    main()
