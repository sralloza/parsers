from json import loads
from pathlib import Path
from typing import Optional

from jsonschema import ValidationError, validate
from pydantic import BaseSettings, validator

from ..utils.environment import load_dotenv_vars

load_dotenv_vars()

OP_INDEX_URL = (
    "https://animebymega.blogspot.com/2020/07/"
    "one-piece-933-sub-espanol-por-mega.html"
)


class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_chat_id: int
    op_anime_index_url: str
    todoist_token: str
    s3_bucket_name: str
    manga_config_path: Optional[Path]

    @validator("manga_config_path")
    def validate_manga_config(cls, v: Optional[Path]):
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
    try:
        validate(data, schema)
    except ValidationError as exc:
        raise ValidationError(_format_jsonschema_validation_error(exc)) from None


settings = Settings()
