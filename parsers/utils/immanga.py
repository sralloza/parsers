import inspect
from typing import Dict
from uuid import UUID

from bs4 import BeautifulSoup
from requests.adapters import RetryError

from ..utils.networking import session
from ..utils.notify import notify_text

PARSE_BASE_URL = (
    "https://inmanga.com/chapter/chapterIndexControls?identification={chapter_id}"
)


def get_chapter_ids(first_chapter_uuid: UUID) -> Dict[float, UUID]:
    try:
        r = session.get(PARSE_BASE_URL.format(chapter_id=first_chapter_uuid))
    except RetryError as exc:
        name = inspect.getmodule(inspect.stack()[1][0]).__name__
        msg = f"Max retries when parsing `immanga` from parser {name!r} [{exc}]"
        notify_text(msg)
        print(msg)
        exit(1)

    soup = BeautifulSoup(r.text, "html.parser")

    ids = {}
    for opt in soup.find(id="ChapList")("option"):
        number = float(opt.text.replace(",", ""))
        ids[number] = UUID(opt["value"])
    return ids
