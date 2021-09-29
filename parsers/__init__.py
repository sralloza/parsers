from bdb import BdbQuit

import click
import sentry_sdk

from .config import settings
from .my_hero_academia import mha_app as my_hero_academia_app
from .my_hero_academia import parse as parse_my_hero_academia
from .one_piece import app as one_piece_app
from .one_piece import parse as parse_one_piece
from .one_punch_man import opm_app as one_punch_man_app
from .one_punch_man import parse as parse_one_punch_man
from .utils.options import silent_option

sentry_sdk.init(
    settings.sentry_url,
    traces_sample_rate=1.0,
    ignore_errors=[KeyboardInterrupt, BdbQuit],
)


@click.group(no_args_is_help=True, help="Manage animes and mangas")
def main_app():
    pass


main_app.add_command(one_piece_app, name="one-piece")
main_app.add_command(one_punch_man_app, name="one-punch-man")
main_app.add_command(my_hero_academia_app, name="my-hero-academia")


@main_app.command("parse", help="Parse everything")
@silent_option()
def parse(silent: bool = False):
    parse_one_piece(silent=silent)
    parse_one_punch_man(silent=silent)
    parse_my_hero_academia(silent=silent)
