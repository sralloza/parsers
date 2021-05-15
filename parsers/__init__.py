from bdb import BdbQuit

import sentry_sdk
import typer

from .config import settings
from .my_hero_academia import app as my_hero_academia_app
from .my_hero_academia import parse as parse_my_hero_academia
from .one_piece import app as one_piece_app
from .one_piece import parse as parse_one_piece
from .one_punch_man import app as one_punch_man_app
from .one_punch_man import parse as parse_one_punch_man

sentry_sdk.init(
    settings.sentry_url, traces_sample_rate=1.0, ignore_errors=[KeyboardInterrupt, BdbQuit]
)

app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(one_piece_app, name="one-piece")
app.add_typer(one_punch_man_app, name="one-punch-man")
app.add_typer(my_hero_academia_app, name="my-hero-academia")


@app.command("parse")
def parse(silent: bool = False):
    """Parse manga and anime."""

    parse_one_piece(silent=silent)
    parse_one_punch_man(silent=silent)
    parse_my_hero_academia(silent=silent)
