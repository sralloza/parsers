from collections import namedtuple
from json import dumps
from typing import List

from bs4 import BeautifulSoup

from ..config import settings
from ..utils.aws import get_file_content, save_file_content
from ..utils.networking import session
from ..utils.notify import notify_text
from ..utils.todoist import add_task

Link = namedtuple("Link", "title url")


def get_latest_link() -> Link:
    response = session.get(settings.inmanga_base_url)
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


def parse_op_anime(silent: bool):
    """Check for new One Piece episodes and send the new links via Telegram."""

    link = get_latest_link()

    registered_links: List[str] = get_file_content("one-piece-anime")

    if link.url in registered_links:
        return

    if not silent:
        msg = f"Nuevo capítulo de One Piece: [{link.title}]({link.url})"
        notify_text(msg)
        add_task(msg)

    registered_links.append(link.url)
    registered_links.sort()
    save_file_content(
        dumps(registered_links, indent=2, ensure_ascii=False), "one-piece-anime"
    )
