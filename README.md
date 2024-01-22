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
2. 
```cmd
poetry 
```
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

# Env variables
- THREADS (default - 5) - connection count at the same time. Recommended to set under 15
- TIMEOUT_INT (default - 30) - seconds to make connection with mangadex server
- LOGGING_LEVEL (default - logging.INFO)
-	NAME_MAX_LENGTH: int = Field(40) - the maximum length of the title
-	LOGS_MAX_SIZE (default - 256) - in bytes
-	ENABLE_STREAM_HANDLER (default - False) - print logs to console
