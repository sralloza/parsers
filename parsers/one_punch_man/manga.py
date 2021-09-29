from uuid import UUID

import typer

from parsers.base.manga import add_manga_app
from parsers.config import settings

FIRST_CHAPTER_UUID = UUID("8dcb38ab-2677-4e39-844f-2ac891e607be")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Punch-Man/{chapter_number}/{chapter_id}"
)

manga_app = typer.Typer(add_completion=False, no_args_is_help=True)

add_manga_app(
    manga_app,
    FIRST_CHAPTER_UUID,
    settings.one_punch_man_manga_uuids_path,
    PUBLIC_BASE_URL,
    "one punch man",
)
