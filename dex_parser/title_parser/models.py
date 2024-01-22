from dataclasses import dataclass


@dataclass
class TitleChapter:
    id: str
    chapter: str
    language: str
    pages: int
