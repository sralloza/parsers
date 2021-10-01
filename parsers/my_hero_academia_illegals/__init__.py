import click

from ..base.parse_command import add_parse_command
from .manga import manga_app


@click.group(no_args_is_help=True, help="My Hero Academia: Illegals")
def mhai_app():
    pass


mhai_app.add_command(manga_app, name="manga")
add_parse_command(mhai_app, manga_app=manga_app, name="one piece")
