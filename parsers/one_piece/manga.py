from json import dumps, loads
from parsers.base.manga import add_manga_app
from typing import Dict
from uuid import UUID

import typer

from parsers.config import settings
from parsers.utils.immanga import get_chapter_ids
from parsers.utils.json_encoding import UUIDEncoder
from parsers.utils.notify import notify_text

FIRST_CHAPTER_UUID = UUID("8d23d3d6-7c59-4223-bfbc-6f87aa8259dd")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Piece/{chapter_number}/{chapter_id}"
)

manga_app = typer.Typer(add_completion=False, no_args_is_help=True)

add_manga_app(
    manga_app,
    FIRST_CHAPTER_UUID,
    settings.one_piece_manga_uuids_path,
    PUBLIC_BASE_URL,
    "one piece",
)
