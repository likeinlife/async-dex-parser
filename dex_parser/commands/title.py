import itertools
import textwrap
import uuid
from pathlib import Path
from typing import Annotated, Optional

import typer

from dex_parser import common, title_parser
from dex_parser.config import config
from dex_parser.help import CHAPTER_SELECT_HELP
from dex_parser.logger_setup import get_logger

logger = get_logger(__name__)

router = typer.Typer(help='Title actions')


@router.command('download', help='Download title chapters')
def download(
    title_identification: Annotated[str, typer.Argument(help='Title url, id or name')],
    language: Annotated[str, typer.Option('--language', '-l', help='Language')] = 'en',
    directory: Annotated[Optional[Path], typer.Option('--directory', '-d', help='Directory to save')] = None,
    add_to_favorite: Annotated[bool, typer.Option('--favorite', '-f', help='Add to favorite list')] = False,
    show_id: Annotated[bool, typer.Option('--show-id', '-si', help="Show chapters' id")] = False,
    number_result: Annotated[Optional[int], typer.Option('--number-result', '-n', help='Show only n results')] = False,
    no_chapters_print: Annotated[
        bool, typer.Option('--no-chapters-print', '-no-print', help='Dont print chapters numbers')
    ] = False,
    disable_creating_title_dir: Annotated[
        bool,
        typer.Option(
            '--disable-title-dir',
            '-dd',
            help='Add to favorite list',
        ),
    ] = False,
):
    from .favorite import add_to_favorite_list

    title = find_title(title_identification, language)
    if len(title.chapters) == 0:
        print('No chapters found')
        return

    if add_to_favorite:
        add_to_favorite_list(name=title.name, id=uuid.UUID(title.id))

    download_chapters(
        title=title,
        directory=directory,
        disable_creating_title_dir=disable_creating_title_dir,
        no_chapters_print=no_chapters_print,
        number_result=number_result,
        show_id=show_id,
    )


class MakeChaptersTable:
    def __init__(
        self,
        title: title_parser.TitleParser,
        show_id: bool = False,
        number_result: int | None = None,
        no_chapters_print: bool = False,
    ) -> None:
        self.title = title
        self.show_id = show_id
        self.number_result = number_result
        self.no_chapters_print = no_chapters_print
        self.content, self.headers = self._check_option_show_id()
        self._check_option_cut_results()

    def _check_no_verbose(self) -> bool:
        if self.no_chapters_print:
            return True
        return False

    def _check_option_cut_results(self):
        if self.number_result:
            self.content = itertools.islice(self.content, self.number_result)

    def _check_option_show_id(self):
        if self.show_id:
            headers = ('chapter', 'language', 'pages', 'id')
            content = [[ch.chapter, ch.language, ch.pages, ch.id] for ch in self.title.chapters]
        else:
            headers = ('chapter', 'language', 'pages')  # type: ignore
            content = [[ch.chapter, ch.language, ch.pages] for ch in self.title.chapters]

        return content, headers

    def print(self) -> None:
        if self.no_chapters_print:
            print('No chapters print')
        print(common.basic_table(self.content, self.headers))


def download_chapters(
    title: title_parser.TitleParser,
    directory: Path | None = None,
    disable_creating_title_dir: bool = False,
    show_id: bool = False,
    number_result: int | None = None,
    no_chapters_print: bool = False,
) -> None:
    print(f'{title.name: ^65}')
    MakeChaptersTable(
        title,
        show_id=show_id,
        number_result=number_result,
        no_chapters_print=no_chapters_print,
    ).print()

    typer.confirm('Download chapters', abort=True)
    while True:
        prompt = typer.prompt('Enter chapter range. `.h` for help')
        if prompt == '.h':
            print(CHAPTER_SELECT_HELP)
            continue
        typer.confirm(f'You are going to download chapters {prompt} from {title.name}', abort=True)

        return title.download(
            prompt,
            directory,
            disable_creating_title_dir,
        )


def choose_title_by_name(titles_ids: list[dict[str, str]], language: str):
    print('There are more than 1 title found by this name')
    headers = ('name', 'id')
    content = (
        (
            textwrap.shorten(title['title'], config.NAME_MAX_LENGTH, placeholder='...'),
            title['id'],
        )
        for title in titles_ids
    )
    table = common.basic_table(content, headers, showindex='always')

    print(table)
    chosen_title = common.choose(titles_ids)
    return title_parser.TitleParser(chosen_title['id'], language)


def find_title(identification: str, language: str) -> title_parser.TitleParser:
    founded = title_parser.get_title_parser(identification=identification, language=language)
    if isinstance(founded, title_parser.TitleParser):
        return founded
    if len(founded) == 1:
        return title_parser.TitleParser(title_id=founded[0]['id'], language=language)
    return choose_title_by_name(titles_ids=founded.titles, language=language)
