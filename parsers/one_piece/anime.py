from collections import namedtuple
from json import dumps, loads
from typing import List

import typer
from bs4 import BeautifulSoup

from parsers.config import settings
from parsers.utils.networking import session
from parsers.utils.notify import notify_text

anime_app = typer.Typer(add_completion=False, no_args_is_help=True)
Link = namedtuple("Link", "title url")


def get_latest_link() -> Link:
    response = session.get(settings.base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    container = list(soup.select("div font a"))[-1]

    try:
        title = container.parent.parent.parent.previous_sibling.text
        assert title
    except (AttributeError, AssertionError):
        title = container.parent.parent.previous_sibling.text

    return Link(title, container["href"])


@anime_app.command()
def parse(silent: bool = False):
    """Check for new One Piece episodes and send the new links via Telegram."""

    link = get_latest_link()

    registered_links: List[str] = loads(
        settings.one_piece_anime_links_file_path.read_text("utf8")
    )

    if link.url in registered_links:
        return

    if not silent:
        msg = f"Nuevo capítulo de **One Piece**: [{link.title}]({link.url})"
        notify_text(msg)

    registered_links.append(link.url)
    registered_links.sort()
    settings.one_piece_anime_links_file_path.write_text(
        dumps(registered_links, indent=2, ensure_ascii=False), encoding="utf8"
    )


@anime_app.command(help="Reset the links list")
def reset():
    settings.one_piece_anime_links_file_path.write_text("[]", "utf8")


@anime_app.command("open", help="Try to open the links file")
def open_file():
    typer.launch(settings.one_piece_anime_links_file_path.as_posix())


@anime_app.command(help="Print links file content to stdout")
def show():
    text = settings.one_piece_anime_links_file_path.read_text("utf8")
    n = max([len(x) for x in text.splitlines()])

    typer.secho("=" * n, fg="bright_cyan")
    typer.secho(text)
    typer.secho("=" * n, fg="bright_cyan")


if __name__ == "__main__":
    anime_app(prog_name="parsers")
