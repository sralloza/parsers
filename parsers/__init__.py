import click

from .my_hero_academia import mha_manga_parser
from .my_hero_academia_illegals import mhai_manga_parser
from .one_piece import op_manga_parser, parse_op_anime
from .one_punch_man import opm_manga_parser
from .utils.options import silent_option


@click.group(no_args_is_help=True, help="Parse all")
@silent_option()
def main_app(silent: bool):
    mha_manga_parser.parse(silent=silent)
    mhai_manga_parser.parse(silent=silent)
    op_manga_parser.parse(silent=silent)
    parse_op_anime(silent=silent)
    opm_manga_parser.parse(silent=silent)
