import sentry_sdk
import typer

from .anime import anime_app, parse as parse_anime
from .manga import manga_app, parse as parse_manga
from .config import settings

# sentry_sdk.init(
#     settings.sentry_url, traces_sample_rate=1.0, ignore_errors=[KeyboardInterrupt]
# )
app = typer.Typer(add_completion=False, no_args_is_help=True)
app.add_typer(anime_app, name="anime")
app.add_typer(manga_app, name="manga")

@app.command("parse")
def parse_both():
    """Parse manga and anime."""

    parse_anime()
    parse_manga()

del anime_app, manga_app, settings, sentry_sdk, typer

if __name__ == "__main__":
    app()
