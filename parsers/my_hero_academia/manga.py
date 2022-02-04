from uuid import UUID

from ..base.manga import INMangaParser

FIRST_CHAPTER_UUID = UUID("a0e29937-0c82-42e5-bf20-4eb7066f9ebe")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/Boku-no-Hero-Academia/{chapter_number}/{chapter_id}"
)

mha_manga_parser = INMangaParser(
    first_chapter_uuid=FIRST_CHAPTER_UUID,
    public_base_url=PUBLIC_BASE_URL,
    manga_name="my hero academia",
)
