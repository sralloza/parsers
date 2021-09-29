from os import makedirs
from pathlib import Path

import click
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    app_dir: Path = Path(click.get_app_dir("parsers"))
    bot_token: str
    chat_id: int
    base_url: str
    sentry_url: str
    todoist_token: str

    @validator("app_dir")
    def create_app_dir(cls, v):
        if isinstance(v, Path):
            if not v.is_dir():
                makedirs(v)
        return v

    @property
    def one_piece_anime_links_file_path(self):
        v = self.app_dir / "op-anime-links"
        if not v.is_file():
            v.write_text("[]", "utf8")
        return v

    @property
    def one_piece_manga_uuids_path(self):
        v = self.app_dir / "op-manga-uuids"
        if not v.is_file():
            v.write_text("{}", "utf8")
        return v

    @property
    def one_punch_man_manga_uuids_path(self):
        v = self.app_dir / "opm-manga-uuids"
        if not v.is_file():
            v.write_text("{}", "utf8")
        return v

    @property
    def my_hero_academia_manga_uuids_path(self):
        v = self.app_dir / "mha-manga-uuids"
        if not v.is_file():
            v.write_text("{}", "utf8")
        return v


settings = Settings()
