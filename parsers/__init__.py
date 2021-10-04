from bdb import BdbQuit

import click
import sentry_sdk

from .config import settings
from .my_hero_academia import mha_app
from .my_hero_academia_illegals import mhai_app
from .one_piece import op_app
from .one_punch_man import opm_app
from .utils.options import silent_option

APPS = [mha_app, op_app, opm_app, mhai_app]

sentry_sdk.init(
    settings.sentry_url,
    traces_sample_rate=1.0,
    ignore_errors=[KeyboardInterrupt, BdbQuit],
)


@click.group(no_args_is_help=True, help="Manage animes and mangas")
def main_app():
    pass


main_app.add_command(mha_app, name="one-piece")
main_app.add_command(mhai_app, name="my-hero-academia-illegals")
main_app.add_command(op_app, name="one-punch-man")
main_app.add_command(opm_app, name="my-hero-academia")


@main_app.command("parse", help="Parse everything")
@silent_option()
def parse(silent: bool):
    for app in APPS:
        func = app.commands["parse"].callback
        func(silent=silent)
