from json import dumps
from typing import Dict
from uuid import UUID

from pydantic import BaseModel

from ..utils.aws import get_file_content, save_file_content
from ..utils.immanga import get_chapter_ids
from ..utils.json_encoding import UUIDEncoder
from ..utils.notify import notify_text
from ..utils.todoist import add_task


class InMangaParser(BaseModel):
    first_chapter_uuid: UUID
    manga_name: str

    def get_public_url(self, chapter_number, chapter_id):
        return f"https://inmanga.com/ver/manga/{self.manga_name}/{chapter_number}/{chapter_id}"

    @property
    def aws_filename(self):
        return self.manga_name.replace(" ", "-").replace(":", "") + "-manga"

    def parse(self, silent: bool):
        chapter_ids = get_chapter_ids(self.first_chapter_uuid)

        registered_chapters: Dict[str, UUID] = {
            a: UUID(b)
            for a, b in get_file_content(self.aws_filename, default="{}").items()
        }

        modified = False
        for chapter_number, chapter_id in chapter_ids.items():
            if chapter_id not in registered_chapters.values():
                modified = True
                self.notify_new(chapter_number, chapter_id, silent=silent)
                registered_chapters[str(chapter_number)] = chapter_id

        if modified:
            save_file_content(
                dumps(registered_chapters, cls=UUIDEncoder, indent=2),
                self.aws_filename,
            )

    def notify_new(self, chapter_number: float, chapter_id: UUID, silent: bool = False):
        if silent:
            return

        try:
            chapter_title = str(int(chapter_number))
        except ValueError:
            chapter_title = str(chapter_number)

        url = self.get_public_url(chapter_number, chapter_id)
        manga_name = self.manga_name.replace("-", " ").title()
        msg = f"Nuevo manga de {manga_name}: [Capítulo {chapter_title}]({url})"
        notify_text(msg=msg)
        add_task(msg=msg)
