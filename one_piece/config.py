from os import makedirs
from pathlib import Path
from pydantic import BaseSettings, validator
import typer


class Settings(BaseSettings):
    app_dir: Path = Path(typer.get_app_dir("one-piece-parser"))
    bot_token: str = "1038586894:AAHE8CPZXXaZJ0KVTxuRXFV6TnQn9qddLaU"
    chat_id: int = 752192090
    base_url: str = "https://animebymega.blogspot.com/2020/07/one-piece-933-sub-espanol-por-mega.html"
    sentry_url: str = (
        "https://098e3c6525744bb2bba46d71a2a5e213@o560014.ingest.sentry.io/5696723"
    )

    @validator("app_dir")
    def create_app_dir(cls, v):
        if isinstance(v, Path):
            if not v.is_dir():
                makedirs(v)
        return v

    @property
    def anime_links_file_path(self):
        v = self.app_dir / "anime-links"
        if not v.is_file():
            v.write_text("[]", "utf8")
        return v

    @property
    def manga_uuids_path(self):
        v = self.app_dir / "manga-uuids"
        if not v.is_file():
            v.write_text("{}", "utf8")
        return v


settings = Settings()
