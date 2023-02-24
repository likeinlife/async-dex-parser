import parse_chapter
import time


def main(ch_id: str):
    start = time.time()
    chapter = parse_chapter.get_parser(ch_id)
    print(chapter)
    parse_chapter.ImageDownloader(chapter)
    delta = time.time() - start
    print(delta)


if __name__ == "__main__":
    ch_id = '957fb831-8952-46ec-bf12-09c4ff0e6fad'
    main(ch_id)
