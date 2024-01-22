from textwrap import dedent

CHAPTER_SELECT_HELP = dedent(
    """
	Example: 1, 2, 4-10, ~2-7, ~8.
	It selects 1, 9, 10 chapters.
	1 | 1-10 - Include
	~1 | ~1-10 - Exclude
	* - Selects all chapters
	"""
)
