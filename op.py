from collections import namedtuple
from json import dumps, loads
from os import makedirs
from pathlib import Path
from typing import List

import requests,sentry_sdk
import typer
from bs4 import BeautifulSoup
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    app_dir: Path = Path(typer.get_app_dir("one-piece-parser"))
    bot_token: str = "1038586894:AAHE8CPZXXaZJ0KVTxuRXFV6TnQn9qddLaU"
    chat_id: int = 752192090
    base_url: str = "https://animebymega.blogspot.com/2020/07/one-piece-933-sub-espanol-por-mega.html"
    sentry_url: str = "https://098e3c6525744bb2bba46d71a2a5e213@o560014.ingest.sentry.io/5696723"

    @validator("app_dir")
    def create_app_dir(cls, v):
        if isinstance(v, Path):
            if not v.is_dir():
                makedirs(v)
        return v

    @property
    def links_file_path(self):
        v = self.app_dir / "links"
        if not v.is_file():
            v.write_text("[]", "utf8")
        return v


settings = Settings()
sentry_sdk.init(settings.sentry_url, traces_sample_rate=1.0, ignore_errors=[KeyboardInterrupt])
app = typer.Typer(add_completion=False)
Link = namedtuple("Link", "title url")


def notify_me(msg):
    response = requests.post(
        f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        json={
            "chat_id": settings.chat_id,
            "text": msg,
            "parse_mode": "markdown",
            "disable_web_page_preview": True,
        },
    )
    response.raise_for_status()


def get_latest_link() -> Link:
    response = requests.get(settings.base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    container = list(soup.select("div font a"))[-1]

    try:
        title = container.parent.parent.parent.previous_sibling.text
        assert title
    except (AttributeError, AssertionError):
        title = container.parent.parent.previous_sibling.text

    return Link(title, container["href"])


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context, info: bool = typer.Option(False, "--info", help="Show info.")
):
    """Check for new One Piece episodes and send the new links via Telegram."""

    ctx.obj = typer.echo if info else lambda *a, **k: None

    if ctx.invoked_subcommand:
        return

    ctx.obj("Gettings latest link")
    link = get_latest_link()
    ctx.obj(f"Latest link is {link!r}")

    registered_links: List[str] = loads(settings.links_file_path.read_text("utf8"))
    ctx.obj("Found %d registered links" % len(registered_links))

    if link.url in registered_links:
        ctx.obj("Link is already registered")
        return

    ctx.obj("Link is new, sending notification")

    msg = f"Nuevo capítulo de **One Piece**: [{link.title}]({link.url})"
    notify_me(msg)
    ctx.obj("Notification sent")

    registered_links.append(link.url)
    registered_links.sort()
    settings.links_file_path.write_text(
        dumps(registered_links, indent=4, ensure_ascii=False), encoding="utf8"
    )
    ctx.obj("Links file updated")


@app.command(help="Reset the links list")
def reset(ctx: typer.Context):
    settings.links_file_path.write_text("[]", "utf8")
    ctx.obj("Links reset")


@app.command("open", help="Try to open the links file")
def open_file(ctx: typer.Context):
    typer.launch(settings.links_file_path.as_posix())
    ctx.obj("Opened links file")


@app.command(help="Print links file content to stdout")
def show(ctx: typer.Context):
    ctx.obj("Reading links file info")
    text = settings.links_file_path.read_text("utf8")
    n = max([len(x) for x in text.splitlines()])

    typer.secho("=" * n, fg="bright_cyan")
    typer.secho(text)
    typer.secho("=" * n, fg="bright_cyan")


if __name__ == "__main__":
    app(prog_name="one-piece-parser")
