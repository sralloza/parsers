"""Parsers configuration."""

from json import loads
from pathlib import Path
from typing import Literal, Optional

from jsonschema import ValidationError, validate
from pydantic import BaseSettings, validator

from ..utils.environment import load_dotenv_vars

load_dotenv_vars()

OP_INDEX_URL = (
    "https://animebymega.blogspot.com/2020/07/"
    "one-piece-933-sub-espanol-por-mega.html"
)


class Settings(BaseSettings):
    """Parsers settings."""

    manga_config_path: Optional[Path]
    op_anime_index_url: Literal[OP_INDEX_URL] = OP_INDEX_URL
    parse_one_piece_anime: bool = False
    s3_bucket_name: str
    telegram_bot_token: str
    telegram_chat_id: int
    todoist_token: Optional[str]
    todoist_project_id: Optional[str]
    todoist_due_str: Optional[str] = "today"

    @property
    def todoist_enabled(self) -> bool:
        """Checks if todoist should be enabled based on other settings."""
        return self.todoist_project_id is not None and self.todoist_token is not None

    # pylint: disable=no-self-argument,no-self-use
    @validator("manga_config_path")
    def validate_manga_config(cls, v: Optional[Path]):
        """Validates manga.json config."""

        if v is None:
            return None

        manga_config = loads(v.read_text("utf8"))
        manga_config_schema = loads(
            Path(__file__).with_name("manga-config-schema.json").read_text("utf8")
        )
        validate_schema(manga_config, manga_config_schema)
        return v


def _format_jsonschema_validation_error(exc):
    """Converts an error raised by the jsonschema module into a custom string."""

    error_msg = ""
    if exc.absolute_path and len(exc.absolute_path) > 0:
        error_msg = f"'{'.'.join([str(x) for x in exc.absolute_path])}': "

    return error_msg + exc.message


def validate_schema(data, schema):
    """Validates a schema using jsonschema."""
    try:
        validate(data, schema)
    except ValidationError as exc:
        raise ValidationError(_format_jsonschema_validation_error(exc)) from None


settings = Settings()
