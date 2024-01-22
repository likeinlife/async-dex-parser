import re

from dex_parser import common, logger_setup

from .parse_chapter import ParseChapter

logger = logger_setup.get_logger(__name__)


def get_chapter_parser(identificator: str):
    """Get chapter by url or id

    Args:
            identificator: url or id
    """
    if chapter_id := common.get_id_from_url(identificator, 'chapter'):
        logger.info(f'{identificator} is URL')
        return ParseChapter(chapter_id)  # type: ignore
    elif re.match(common.id_pattern, identificator):
        logger.info(f'{identificator} is id')
        return ParseChapter(identificator)
    else:
        exit(f'Invalid identificator: {identificator}')
