import click

from ..utils.options import silent_option
from .manga import manga_app


@click.group(no_args_is_help=True, help="One Punch Man")
def opm_app():
    pass


opm_app.add_command(manga_app, name="manga")


@opm_app.command("parse", help="Parse one punch man both manga and anime")
@silent_option()
def parse(silent: bool):
    parse_manga = manga_app.commands["parse"].callback
    parse_manga(silent=silent)
