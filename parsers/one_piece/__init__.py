import typer

from .anime import anime_app
from .anime import parse as parse_anime
from .manga import manga_app
from .manga import parse as parse_manga

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(anime_app, name="anime")
app.add_typer(manga_app, name="manga")


@app.command("parse")
def parse():
    """Parse manga and anime."""

    parse_anime()
    parse_manga()


del anime_app, manga_app, typer
