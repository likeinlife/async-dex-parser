from typing import Tuple

from app.logger_setup import get_logger

logger = get_logger(__name__)


class SelectChapters:
    """Select chapter ranges like `1, 2, 2-10, 20-30, ~8`"""

    def __init__(self, chapters_select: str) -> None:
        self.input = chapters_select.replace(' ', '').split(',')
        self.include, self.exclude = self.__make_lists()

    def __contains__(self, number: str) -> bool:
        """Check if this chapter in range"""
        include_flag = any(map(lambda x: self.__check_number(x, number), self.include))
        exclude_flag = any(map(lambda x: self.__check_number(x, number), self.exclude))
        if include_flag and not exclude_flag:
            logger.debug(f'Chapter {number} in range')
            return True
        logger.debug(f'Chapter {number} not in range')
        return False

    def __make_lists(self):
        include = []
        exclude = []
        for item in self.input:
            if '~' in item:
                exclude.append(self.__make_range(item))
            else:
                include.append(self.__make_range(item))
        logger.debug(f'Including chapters {include=}')
        logger.debug(f'Excluding {exclude=}')
        return include, exclude

    def __make_range(self, number: str):
        number = number.replace('~', '')
        if number.replace('.', '').isnumeric():
            return float(number)
        elif '-' in number:
            return self.__get_start_and_end(number)
        else:
            exit(f'Incorrect range: {number}. Not a number nor range')

    def __get_start_and_end(self, chapter_range: str) -> Tuple[float, float]:
        """Transform '1-20' to tuple(1, 20)"""
        start, end = list(map(self.__make_range, chapter_range.split('-')))

        if isinstance(start, float) and isinstance(end, float):
            return start, end
        else:
            exit(f'Not a digits {chapter_range}')

    @staticmethod
    def __check_number(chapter_range: float | Tuple[float, float], value_to_check: str) -> bool:
        """Check number if it is in :chapter_range:"""
        if isinstance(chapter_range, float):
            if value_to_check == str(chapter_range):
                return True
        if isinstance(chapter_range, tuple):
            if chapter_range[0] <= float(value_to_check) <= chapter_range[1]:
                return True
        return False

    def __repr__(self) -> str:
        return f'{self.include}; excluding {self.exclude}'
