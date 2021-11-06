from json import dumps, loads
from pathlib import Path
from typing import Dict
from uuid import UUID

import click
from pydantic.main import BaseModel

from parsers.utils.aws import get_file_content, save_file_content

from ..utils.immanga import get_chapter_ids
from ..utils.json_encoding import UUIDEncoder
from ..utils.notify import notify_text
from ..utils.todoist import add_task


class INMangaParser(BaseModel):
    first_chapter_uuid: UUID
    public_base_url: str
    manga_name: str

    @property
    def aws_filename(self):
        return self.manga_name.replace(" ", "-") + "-manga"

    def parse(self, silent: bool):
        chapter_ids = get_chapter_ids(self.first_chapter_uuid)

        registered_chapters: Dict[str, UUID] = {
            a: UUID(b) for a, b in get_file_content(self.aws_filename).items()
        }

        for chapter_number, chapter_id in chapter_ids.items():
            if chapter_id not in registered_chapters.values():
                self.notify_new(chapter_number, chapter_id, silent=silent)
                registered_chapters[str(chapter_number)] = chapter_id
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

        url = self.public_base_url.format(
            chapter_number=chapter_number, chapter_id=chapter_id
        )
        msg = f"Nuevo manga de {self.manga_name}: [Capítulo {chapter_title}]({url})"
        notify_text(msg=msg)
        add_task(msg=msg)
