import typer

from .manga import manga_app
from .manga import parse as parse_manga

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(manga_app, name="manga")


@app.command("parse")
def parse():
    """Parse manga and anime."""

    parse_manga()


del manga_app, typer
