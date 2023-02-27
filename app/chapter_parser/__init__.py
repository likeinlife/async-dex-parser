from .parse_chapter import Chapter, ImageDownloader, MassParser, SingleParser


def get_chapter(chapter_id: str | list[str]):
    if isinstance(chapter_id, str):
        return SingleParser(chapter_id)
    elif isinstance(chapter_id, list):
        return MassParser(chapter_id)
    else:
        raise Exception('chapter_id not a list[str] or str')
