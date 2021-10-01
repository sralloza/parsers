import click

from ..base.parse_command import add_parse_command
from .anime import anime_app
from .manga import manga_app


@click.group(no_args_is_help=True, help="One Piece")
def op_app():
    pass


op_app.add_command(anime_app, name="anime")
op_app.add_command(manga_app, name="manga")

add_parse_command(op_app, anime_app=anime_app, manga_app=manga_app, name="one piece")
