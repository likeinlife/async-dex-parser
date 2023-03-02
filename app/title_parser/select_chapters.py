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
        exclude_flag = not any(map(lambda x: self.__check_number(x, number), self.exclude))
        if include_flag and exclude_flag:
            return True
        return False

    def __make_lists(self):
        include = []
        exclude = []
        for item in self.input:
            if '~' in item:
                exclude.append(self.__make_range(item))
            else:
                include.append(self.__make_range(item))
        return include, exclude

    def __make_range(self, number: str):
        number = number.replace('~', '')
        if number.isnumeric():
            return float(number)
        elif '-' in number:
            return self.__get_start_and_end(number)
        else:
            exit(f'Something went wrong with chapter range {number}')

    def __get_start_and_end(self, chapter_range: str) -> Tuple[float, float]:
        """Transform '1-20' to tuple(1, 20)"""
        start, end = list(map(self.__make_range, chapter_range.split('-')))

        if isinstance(start, float) and isinstance(end, float):
            return start, end
        else:
            exit(f'Something went wrong with chapter range {chapter_range}')

    @staticmethod
    def __check_number(chapter_range: float | Tuple[float, float], value_to_check: str) -> bool:
        """Check number if it is in :chapter_range:"""
        if isinstance(chapter_range, float):
            if float(value_to_check) == chapter_range:
                return True
        if isinstance(chapter_range, tuple):
            if chapter_range[0] <= float(value_to_check) <= chapter_range[1]:
                return True
        return False

    def __repr__(self) -> str:
        return f'{self.include}; excluding {self.exclude}'
