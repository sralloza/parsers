from collections import namedtuple
from json import dumps, loads
from typing import List

import click
from bs4 import BeautifulSoup

from ..config import settings
from ..utils.networking import session
from ..utils.notify import notify_text
from ..utils.options import silent_option
from ..utils.todoist import add_task

Link = namedtuple("Link", "title url")


@click.group(no_args_is_help=True, help="Manage one piece anime")
def anime_app():
    pass


def get_latest_link() -> Link:
    response = session.get(settings.base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    container = list(
        soup.find_all("a", class_="imgbtn imgbtn--red imgbtn--rubber daicon-download")
    )[-1]

    try:
        title = container.parent.parent.parent.previous_sibling.text
        assert title
    except (AttributeError, AssertionError):
        title = container.parent.parent.previous_sibling.text

    return Link(title, container["href"])


@anime_app.command(help="Parse anime")
@silent_option()
def parse(silent: bool):
    """Check for new One Piece episodes and send the new links via Telegram."""

    link = get_latest_link()

    registered_links: List[str] = loads(
        settings.one_piece_anime_links_file_path.read_text("utf8")
    )

    if link.url in registered_links:
        return

    if not silent:
        msg = f"Nuevo capítulo de One Piece: [{link.title}]({link.url})"
        notify_text(msg)
        add_task(msg)

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
    click.launch(settings.one_piece_anime_links_file_path.as_posix())


@anime_app.command(help="Print links file content to stdout")
def show():
    text = settings.one_piece_anime_links_file_path.read_text("utf8")
    n = max([len(x) for x in text.splitlines()])

    click.secho("=" * n, fg="bright_cyan")
    click.secho(text)
    click.secho("=" * n, fg="bright_cyan")
