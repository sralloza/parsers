import click

from ..base.parse_command import add_parse_command
from .manga import manga_app


@click.group(no_args_is_help=True, help="One Punch Man")
def opm_app():
    pass


opm_app.add_command(manga_app, name="manga")

add_parse_command(opm_app, manga_app=manga_app, name="one piece")
