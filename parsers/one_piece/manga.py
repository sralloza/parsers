from uuid import UUID

from parsers.base.manga import add_manga_app
from parsers.config import settings

FIRST_CHAPTER_UUID = UUID("8d23d3d6-7c59-4223-bfbc-6f87aa8259dd")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Piece/{chapter_number}/{chapter_id}"
)


manga_app = add_manga_app(
    FIRST_CHAPTER_UUID,
    settings.one_piece_manga_uuids_path,
    PUBLIC_BASE_URL,
    "one piece",
)
