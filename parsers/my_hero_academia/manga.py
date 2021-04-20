from uuid import UUID

import typer

from parsers.base.manga import add_manga_app
from parsers.config import settings

FIRST_CHAPTER_UUID = UUID("a0e29937-0c82-42e5-bf20-4eb7066f9ebe")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/Boku-no-Hero-Acadfemia/{chapter_number}/{chapter_id}"
)

manga_app = typer.Typer(add_completion=False, no_args_is_help=True)

add_manga_app(
    manga_app,
    FIRST_CHAPTER_UUID,
    settings.my_hero_academia_manga_uuids_path,
    PUBLIC_BASE_URL,
    "my hero academia",
)
