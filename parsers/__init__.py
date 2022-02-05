import click

from .config import settings
from .mangas import parse_mangas
from .one_piece import parse_op_anime
from .utils.options import silent_option


@click.group(no_args_is_help=True, help="Parse all")
def app():
    pass


@app.command("parse")
@silent_option()
def parse(silent: bool):
    parse_mangas(silent=silent)
    if settings.parse_one_piece_anime:
        parse_op_anime(silent=silent)
