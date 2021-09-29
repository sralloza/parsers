import click

from ..utils.options import silent_option
from .anime import anime_app
from .anime import parse as parse_anime
from .manga import manga_app


@click.group(no_args_is_help=True, help="One Piece")
def app():
    pass


app.add_command(anime_app, name="anime")
app.add_command(manga_app, name="manga")


@app.command("parse", help="Parse one piece both manga and anime")
@silent_option()
def parse(silent: bool):
    parse_manga = manga_app.commands["parse"].callback
    parse_anime(silent=silent)
    parse_manga(silent=silent)
