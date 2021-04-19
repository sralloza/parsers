from typing import Dict
from uuid import UUID

from bs4 import BeautifulSoup

from parsers.utils.networking import session

PARSE_BASE_URL = (
    "https://inmanga.com/chapter/chapterIndexControls" "?identification={chapter_id}"
)


def get_chapter_ids(first_chapter_uuid: UUID) -> Dict[float, UUID]:
    r = session.get(PARSE_BASE_URL.format(chapter_id=first_chapter_uuid))
    soup = BeautifulSoup(r.text, "html.parser")

    ids = {}
    for opt in soup.find(id="ChapList")("option"):
        number = float(opt.text.replace(",", ""))
        ids[number] = UUID(opt["value"])
    return ids
