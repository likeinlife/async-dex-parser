from .parse_chapter import Chapter, ImageDownloader, MassParser, ParseChapter
import re

from app import common


def get_chapter(identificator: str):
    if chapter_id := common.get_id_from_url(identificator, 'chapter'):
        return ParseChapter(chapter_id)
    elif re.match(common.id_pattern, identificator):
        return ParseChapter(identificator)
    else:
        exit(f'Invalid identificator: {identificator}')
