import click

from ..utils.options import silent_option


def add_parse_command(
    primary_app: click.Group,
    *,
    manga_app: click.Group = None,
    anime_app: click.Group = None,
    name: str,
):
    functions = []
    if manga_app:
        functions.append(manga_app.commands["parse"].callback)
    if anime_app:
        functions.append(anime_app.commands["parse"].callback)

    @primary_app.command("parse", help=f"Parse {name} both manga and anime")
    @silent_option()
    def parse(silent: bool):
        for func in functions:
            func(silent=silent)


# @app.command("parse", help="Parse one piece both manga and anime")
# @silent_option()
# def parse(silent: bool):
#     parse_manga = manga_app.commands["parse"].callback
#     parse_anime(silent=silent)
#     parse_manga(silent=silent)
