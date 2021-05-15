import typer

from .anime import anime_app
from .anime import parse as parse_anime
from .manga import manga_app

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(anime_app, name="anime")
app.add_typer(manga_app, name="manga")

parse_manga = next(
    x for x in manga_app.registered_commands if x.name == "parse"
).callback


@app.command("parse")
def parse(silent: bool = False):
    """Parse manga and anime."""

    parse_anime(silent=silent)
    parse_manga(silent=silent)


del anime_app, manga_app, typer
