from dataclasses import dataclass


@dataclass
class Chapter:
    id: str
    manga_name: str
    chapter_number: str
    chapter_name: str
    language: str
    pages_number: int
