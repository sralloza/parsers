from io import BytesIO
from json import JSONEncoder, dumps, loads
from pathlib import Path
from threading import Lock, Thread
from typing import Dict, List
from uuid import UUID, uuid4
import warnings
import typer
from bs4 import BeautifulSoup
from PIL import Image

from .config import settings
from .networking import session
from .notify import notify_pdf, notify_text


class DoNotUseWarning(Warning):
    pass


FIRST_CHAPTER_UUID = "8d23d3d6-7c59-4223-bfbc-6f87aa8259dd"
PARSE_BASE_URL = (
    "https://inmanga.com/chapter/chapterIndexControls" "?identification={chapter_id}"
)
PUBLIC_BASE_URL = (
    "https://inmanga.com/ver/manga/One-Piece/{chapter_number}/{chapter_id}"
)
IMAGE_URL = "https://pack-yak.intomanga.com/images/manga/One-Piece/chapter/x/page/{page_number}/{page_id}"

manga_app = typer.Typer(add_completion=False)


class UUIDEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return obj.hex
        return JSONEncoder.default(self, obj)


@manga_app.command(help="Finds new chapters")
def parse(silent: bool = False):
    chapter_ids = get_chapter_ids()

    registered_chapters: Dict[str, UUID] = {
        a: UUID(b)
        for a, b in loads(settings.manga_uuids_path.read_text("utf8")).items()
    }

    for chapter_number, chapter_id in chapter_ids.items():
        if chapter_id not in registered_chapters.values():
            try:
                notify_new(chapter_number, chapter_id, silent=silent)
                # gen_pdf_and_send(chapter_number, chapter_id, silent=silent)
                registered_chapters[str(chapter_number)] = chapter_id
                settings.manga_uuids_path.write_text(
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
    notify_text(msg=f"Nuevo manga de one piece: [Capítulo {chapter_title}]({url})")


def gen_pdf_and_send(chapter_number: float, chapter_id: UUID, silent: bool = False):
    warnings.warn("Do not generate pdf", DoNotUseWarning)

    if silent:
        return

    try:
        chapter_title = str(int(chapter_number))
    except ValueError:
        chapter_title = str(chapter_number)

    file = BytesIO()
    file.name = "chapter.pdf"
    get_pdf_by_chapter_id(chapter_id, file)
    file.seek(0)
    file_content = file.read()
    file.close()

    caption = f"Nuevo manga de one piece: {chapter_title}"
    notify_pdf(
        filename=f"one-piece-manga-{chapter_title}.pdf",
        caption=caption,
        file_content=file_content,
    )


def get_chapter_ids() -> Dict[float, UUID]:
    r = session.get(PARSE_BASE_URL.format(chapter_id=FIRST_CHAPTER_UUID))
    soup = BeautifulSoup(r.text, "html.parser")

    ids = {}
    for opt in soup.find(id="ChapList")("option"):
        number = float(opt.text.replace(",", ""))
        ids[number] = UUID(opt["value"])
    return ids


def is_grey_scale(img: Image.Image):
    w, h = img.size
    for i in range(w):
        for j in range(h):
            r, g, b = img.getpixel((i, j))
            if r != g != b:
                return False
    return True


def fetch_image(url: str, page, image_list: Dict[int, Image.Image], lock: Lock):
    r = session.get(url, stream=True)
    with lock:
        im = Image.open(r.raw)
        im.load()
        # out = BytesIO()
        # im.save(out, format="png")
        # size = out.tell()
        # if im.size[1] != 1200:
        # if not is_grey_scale(im):
        #     im.save(f"avoid/{uuid4()}.png")
        #     return
        # if size > 999999:
        #     return
        # print(f"{page:2d}", out.tell(), im.size)
        image_list[page] = im


def get_pdf_by_chapter_id(chapter_id: UUID, file):
    r = session.get(PARSE_BASE_URL.format(chapter_id=chapter_id))
    soup = BeautifulSoup(r.text, "html.parser")

    pages = {}
    for opt in soup.find(id="PageList")("option"):
        number = int(opt.text.replace(",", ""))
        pages[number] = UUID(opt["value"])

    images = {}
    threads = []
    lock = Lock()
    for page_number, page_id in pages.items():
        attrs = dict(page_number=page_number, page_id=page_id)
        t = Thread(
            target=fetch_image,
            args=(IMAGE_URL.format(**attrs), page_number, images, lock),
            daemon=True,
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pages = sorted(images.keys())
    image_list = [images[x] for x in pages]

    im = image_list[0]
    im.save(file, save_all=True, append_images=image_list[1:])


@manga_app.command(help="Reset the uuids file")
def reset():
    settings.manga_uuids_path.write_text("{}", "utf8")


@manga_app.command("open", help="Try to open the uuids file")
def open_file():
    typer.launch(settings.manga_uuids_path.as_posix())


@manga_app.command(help="Print uuids file content to stdout")
def show():
    text = settings.manga_uuids_path.read_text("utf8")
    n = max([len(x) for x in text.splitlines()])

    typer.secho("=" * n, fg="bright_cyan")
    typer.secho(text)
    typer.secho("=" * n, fg="bright_cyan")
