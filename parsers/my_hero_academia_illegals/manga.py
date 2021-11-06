from uuid import UUID

from ..base.manga import INMangaParser

FIRST_CHAPTER_UUID = UUID("03b07c1a-3677-4eb8-bc99-307f41546588")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/mha-illegals/{chapter_number}/{chapter_id}"
)

mhai_manga_parser = INMangaParser(
    first_chapter_uuid=FIRST_CHAPTER_UUID,
    public_base_url=PUBLIC_BASE_URL,
    manga_name="my hero academia: illegals",
)
