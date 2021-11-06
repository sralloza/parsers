from uuid import UUID

from ..base.manga import INMangaParser

FIRST_CHAPTER_UUID = UUID("8dcb38ab-2677-4e39-844f-2ac891e607be")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Punch-Man/{chapter_number}/{chapter_id}"
)


opm_manga_parser = INMangaParser(
    first_chapter_uuid=FIRST_CHAPTER_UUID,
    public_base_url=PUBLIC_BASE_URL,
    manga_name="one punch man",
)
