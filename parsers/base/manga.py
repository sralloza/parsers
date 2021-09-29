from json import dumps, loads
from pathlib import Path
from typing import Dict
from uuid import UUID

import click

from ..utils.immanga import get_chapter_ids
from ..utils.json_encoding import UUIDEncoder
from ..utils.notify import notify_text
from ..utils.options import silent_option
from ..utils.todoist import add_task


def add_manga_app(
    first_chapter_uuid: UUID,
    uuids_path: Path,
    public_base_url: str,
    manga_name: str,
):
    @click.group(no_args_is_help=True, help=f"Manage {manga_name} manga")
    def manga_app():
        pass

    @manga_app.command("parse", help="Finds new chapters")
    @silent_option()
    def parse(silent: bool):
        chapter_ids = get_chapter_ids(first_chapter_uuid)

        registered_chapters: Dict[str, UUID] = {
            a: UUID(b) for a, b in loads(uuids_path.read_text("utf8")).items()
        }

        for chapter_number, chapter_id in chapter_ids.items():
            if chapter_id not in registered_chapters.values():
                notify_new(chapter_number, chapter_id, silent=silent)
                registered_chapters[str(chapter_number)] = chapter_id
                uuids_path.write_text(
                    dumps(registered_chapters, cls=UUIDEncoder, indent=2), "utf8"
                )

    def notify_new(chapter_number: float, chapter_id: UUID, silent: bool = False):
        if silent:
            return

        try:
            chapter_title = str(int(chapter_number))
        except ValueError:
            chapter_title = str(chapter_number)

        url = public_base_url.format(
            chapter_number=chapter_number, chapter_id=chapter_id
        )
        msg = f"Nuevo manga de {manga_name}: [Capítulo {chapter_title}]({url})"
        notify_text(msg=msg)
        add_task(msg=msg)

    @manga_app.command("reset", help="Reset the uuids file")
    def reset():
        uuids_path.write_text("{}", "utf8")

    @manga_app.command("open", help="Try to open the uuids file")
    def open_file():
        click.launch(uuids_path.as_posix())

    @manga_app.command("show", help="Print uuids file content to stdout")
    def show():
        text = uuids_path.read_text("utf8")
        n = max([len(x) for x in text.splitlines()])

        click.secho("=" * n, fg="bright_cyan")
        click.secho(text)
        click.secho("=" * n, fg="bright_cyan")

    return manga_app
