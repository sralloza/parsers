from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_chat_id: int
    inmanga_base_url: str
    todoist_token: str
    s3_bucket_name: str


settings = Settings()
