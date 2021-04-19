import sentry_sdk
import typer

from .config import settings
from .one_piece import app as one_piece_app
from .one_piece import parse as parse_one_piece

sentry_sdk.init(
    settings.sentry_url, traces_sample_rate=1.0, ignore_errors=[KeyboardInterrupt]
)

app = typer.Typer(add_completion=False)
app.add_typer(one_piece_app, name="one-piece")


@app.command("parse")
def parse():
    """Parse manga and anime."""

    parse_one_piece()
