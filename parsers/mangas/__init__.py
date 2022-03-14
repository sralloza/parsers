"""Mangas parsers."""

from json import loads

from ..config import settings
from .base import InMangaParser


def parse_mangas(silent=False):
    """Parses all mangas.

    Args:
        silent (bool, optional): if True, no notification will be sent even if a
            new chapter is found. Defaults to False.
    """
    
    if not settings.manga_config_path:
        return

    mangas = loads(settings.manga_config_path.read_text("utf8"))

    for manga_name, first_chapter_uuid in mangas.items():
        tmp_manga_parser = InMangaParser(
            first_chapter_uuid=first_chapter_uuid,
            manga_name=manga_name,
        )
        tmp_manga_parser.parse(silent=silent)
