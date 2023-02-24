import parse_chapter
import time


def main(ch_id: str):
    start = time.time()
    chapter = parse_chapter.get_parser(ch_id)
    print(chapter.chapter_info)
    # parse_chapter.ImageDownloader(chapter)
    delta = time.time() - start
    print(delta)


if __name__ == "__main__":
    ch_id = 'b7a4042f-010a-4a16-bfd9-323237332b48'
    main(ch_id)
