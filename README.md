# Description

Python CLI to download chapters from MangaDex.
You can:
1. Download chapters by id or url
2. Download chapters from title

# Download and use

## exe
Download latest release

## build
1. Download repository
```cmd
git clone https://github.com/likeinlife/async-dex-parser.git
```
2. Download `pyoxydizer` via pip, cargo, etc
3. cd to `pyoxidizer_builder`, then type
```cmd
pyoxidizer.exe build --release
```
4. .exe file appear in `pyoxidizer_builder/build/<your_system>/release/install`

## python
1. Download repository
```cmd
git clone https://github.com/likeinlife/async-dex-parser.git
```
2. Download dependencies
```cmd
pip install .
```
3. Use
```python
python -m dex_parser --help
```

# Use cases
## Download chapters from title
  - `dex title c26269c7-0f5d-4966-8cd5-b79acb86fb7a` - show title information
  - `dex title Sewayaki Kitsune`
  - `dex title Sewayaki Kitsune -f` - find manga and add it to favorite list
  - `dex title Sewayaki Kitsune --mass` - download all available chapters on english language
  - `dex title Sewayaki Kitsune -m -l any` - download all available chapters on any language

## Download chapter from url/id
  - `dex chapter ce7f8709-c27c-465d-bdd9-d9c0c99b3735` - download chapter
  - `dex chapter ce7f8709-c27c-465d-bdd9-d9c0c99b3735 -n '91 chapter' -d './test'` - will download 91 chapter in folder `./test`

## Favorite list
  - `dex fav list` - show your favorite list
  - `dex fav download` - download chapter from fav list
  - `dex fav add "Sewayaki Kitsune" c26269c7-0f5d-4966-8cd5-b79acb86fb7a` - add Sewayaki Kitsune manga to your favorite list
  - `dex fav del 1` - delete the first title in your list

# Env variables
- THREADS (default - 5) - connection count at the same time. Recommended to set under 15
- TIMEOUT_INT (default - 30) - seconds to make connection with mangadex server
- LOGGING_LEVEL (default - logging.INFO)
-	NAME_MAX_LENGTH: int = Field(40) - the maximum length of the title
-	LOGS_MAX_SIZE (default - 256) - in bytes
-	ENABLE_STREAM_HANDLER (default - False) - print logs to console
