from uuid import UUID

from ..base.manga import INMangaParser

FIRST_CHAPTER_UUID = UUID("8d23d3d6-7c59-4223-bfbc-6f87aa8259dd")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Piece/{chapter_number}/{chapter_id}"
)


op_manga_parser = INMangaParser(
    first_chapter_uuid=FIRST_CHAPTER_UUID,
    public_base_url=PUBLIC_BASE_URL,
    manga_name="one piece",
)
