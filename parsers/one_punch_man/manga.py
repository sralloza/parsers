from json import dumps, loads
from typing import Dict
from uuid import UUID

import typer

from parsers.config import settings
from parsers.utils.immanga import get_chapter_ids
from parsers.utils.json_encoding import UUIDEncoder
from parsers.utils.notify import notify_text

FIRST_CHAPTER_UUID = UUID("8dcb38ab-2677-4e39-844f-2ac891e607be")
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Punch-Man/{chapter_number}/{chapter_id}"
)

manga_app = typer.Typer(add_completion=False)



@manga_app.command(help="Finds new chapters")
def parse(silent: bool = False):
    chapter_ids = get_chapter_ids(FIRST_CHAPTER_UUID)

    registered_chapters: Dict[str, UUID] = {
        a: UUID(b)
        for a, b in loads(
            settings.one_punch_man_manga_uuids_path.read_text("utf8")
        ).items()
    }

    for chapter_number, chapter_id in chapter_ids.items():
        if chapter_id not in registered_chapters.values():
            try:
                notify_new(chapter_number, chapter_id, silent=silent)
                registered_chapters[str(chapter_number)] = chapter_id
                settings.one_punch_man_manga_uuids_path.write_text(
                    dumps(registered_chapters, cls=UUIDEncoder, indent=2), "utf8"
                )
            except Exception as exc:
                print(exc)


def notify_new(chapter_number: float, chapter_id: UUID, silent: bool = False):
    if silent:
        return

    try:
        chapter_title = str(int(chapter_number))
    except ValueError:
        chapter_title = str(chapter_number)

    url = PUBLIC_BASE_URL.format(chapter_number=chapter_number, chapter_id=chapter_id)
    notify_text(msg=f"Nuevo manga de one punch man: [Capítulo {chapter_title}]({url})")


@manga_app.command(help="Reset the uuids file")
def reset():
    settings.one_punch_man_manga_uuids_path.write_text("{}", "utf8")


@manga_app.command("open", help="Try to open the uuids file")
def open_file():
    typer.launch(settings.one_punch_man_manga_uuids_path.as_posix())


@manga_app.command(help="Print uuids file content to stdout")
def show():
    text = settings.one_punch_man_manga_uuids_path.read_text("utf8")
    n = max([len(x) for x in text.splitlines()])

    typer.secho("=" * n, fg="bright_cyan")
    typer.secho(text)
    typer.secho("=" * n, fg="bright_cyan")
