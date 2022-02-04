from pydantic import BaseSettings


class Settings(BaseSettings):
    telegram_bot_token: str
    telegram_chat_id: int
    op_anime_index_url: str = "https://animebymega.blogspot.com/2020/07/one-piece-933-sub-espanol-por-mega.html"
    todoist_token: str
    s3_bucket_name: str


settings = Settings()
