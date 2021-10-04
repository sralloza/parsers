from typing import Any, Dict

from ..config import settings
from ..utils.networking import session


def notify_text(msg: str):
    response = session.post(
        f"https://api.telegram.org/bot{settings.bot_token}/sendMessage",
        json={
            "chat_id": settings.chat_id,
            "text": msg,
            "parse_mode": "markdown",
            "disable_web_page_preview": True,
        },
    )
    response.raise_for_status()


def notify_pdf(file_content: bytes, filename: str, caption: str = None):
    params: Dict[str, Any] = {"chat_id": settings.chat_id}
    if caption:
        params["caption"] = caption

    response = session.post(
        f"https://api.telegram.org/bot{settings.bot_token}/sendDocument",
        params=params,
        files={"document": (filename, file_content)},
    )
    response.raise_for_status()
