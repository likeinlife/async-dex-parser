import typer

from .commands import chapter, favorite, title

app = typer.Typer(name='dex', help='MangaDex parser for titles and chapters.')
app.add_typer(chapter.router, name='chapter')
app.add_typer(favorite.router, name='favorite')
app.add_typer(title.router, name='title')


def parse_args():
    app()
