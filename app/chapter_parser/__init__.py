import re

from app import common
from app import logger_setup

from .parse_chapter import Chapter, ParseChapter

logger = logger_setup.get_logger(__name__)


def get_chapter(identificator: str):
    if chapter_id := common.get_id_from_url(identificator, 'chapter'):
        logger.debug(f'{identificator} is URL')
        return ParseChapter(chapter_id)  # type: ignore
    elif re.match(common.id_pattern, identificator):
        logger.debug(f'{identificator} is id')
        return ParseChapter(identificator)
    else:
        exit(f'Invalid identificator: {identificator}')
