from .parse_chapter import SingleParser, MassParser, ImageDownloader, Chapter


def get_chapter(chapter_id: str | list[str]):
    if isinstance(chapter_id, str):
        return SingleParser(chapter_id)
    elif isinstance(chapter_id, list):
        return MassParser(chapter_id)
    else:
        raise Exception('chapter_id not a list[str] or str')
