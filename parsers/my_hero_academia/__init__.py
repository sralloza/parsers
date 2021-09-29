import click

from ..utils.options import silent_option
from .manga import manga_app


@click.group(no_args_is_help=True, help="My Hero Academia")
def mha_app():
    pass


mha_app.add_command(manga_app, name="manga")


@mha_app.command("parse", help="Parse my hero academia both manga and anime")
@silent_option()
def parse(silent: bool):
    parse_manga = manga_app.commands["parse"].callback
    parse_manga(silent=silent)
