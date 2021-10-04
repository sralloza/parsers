from uuid import UUID

from ..base.manga import add_manga_app
from ..config import settings

FIRST_CHAPTER_UUID = UUID("03b07c1a-3677-4eb8-bc99-307f41546588")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/mha-illegals/{chapter_number}/{chapter_id}"
)

manga_app = add_manga_app(
    FIRST_CHAPTER_UUID,
    settings.my_hero_academia_illegals_manga_uuids_path,
    PUBLIC_BASE_URL,
    "my hero academia: illegals",
)
