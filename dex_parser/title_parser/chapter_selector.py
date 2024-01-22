from typing import Tuple

from dex_parser.logger_setup import get_logger

logger = get_logger(__name__)


def get_chapter_selector(chapter_select_string: str) -> 'ChapterSelector':
    if chapter_select_string == '*':
        return AllChapterSelector(chapter_select_string)
    return ChapterSelector(chapter_select_string)


class ChapterSelector:
    """Select chapter ranges like `1, 2, 2-10, 20-30, ~8`"""

    def __init__(self, chapters_select_string: str) -> None:
        self.input = chapters_select_string.replace(' ', '').split(',')
        self.include, self.exclude = self._make_lists()

    def __contains__(self, number: str) -> bool:
        """Check if this chapter in range"""
        include_flag = any(self._check_number(x, number) for x in self.include)
        exclude_flag = any(self._check_number(x, number) for x in self.exclude)
        if include_flag and not exclude_flag:
            logger.debug(f'Chapter {number} in range')
            return True
        logger.debug(f'Chapter {number} not in range')
        return False

    def _make_lists(self):
        include = []
        exclude = []
        for item in self.input:
            if '~' in item:
                exclude.append(self._make_range(item))
            else:
                include.append(self._make_range(item))
        logger.debug(f'Including chapters {include=}')
        logger.debug(f'Excluding {exclude=}')
        return include, exclude

    def _make_range(self, number: str):
        number = number.replace('~', '')
        if number.replace('.', '').isnumeric():
            if (float_number := float(number)) == int(float_number):
                return int(float_number)
            return float(number)
        elif '-' in number:
            return self._transform_range(number)
        else:
            exit(f'Incorrect range: {number}. Not a number nor range')

    def _transform_range(self, chapter_range: str) -> Tuple[float, float]:
        """Transform '1-20' to tuple(1, 20)."""
        start, end = list(map(self._make_range, chapter_range.split('-')))

        if isinstance(start, float | int) and isinstance(end, float | int):
            return start, end
        else:
            exit(f'Not a digits {chapter_range}')

    @staticmethod
    def _check_number(chapter_range: float | Tuple[float, float], number: str) -> bool:
        """Check number if number in :chapter_range:."""
        if isinstance(chapter_range, float | int):
            if number == str(chapter_range):
                return True
        if isinstance(chapter_range, tuple):
            if chapter_range[0] <= float(number) <= chapter_range[1]:
                return True
        return False

    def __repr__(self) -> str:
        return f'{self.include}; excluding {self.exclude}'


class AllChapterSelector(ChapterSelector):
    """Selects all chapters, for mass download."""

    def __init__(self, _: str) -> None:
        pass

    def __contains__(self, _: str) -> bool:
        return True
