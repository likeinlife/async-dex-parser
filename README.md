# async-dex-parser
Main CLi file - CLI_parse_chapter.py

Installing:
- `git clone https://github.com/likeinlife/async-dex-parser.git`
- `python -m venv venv`  # virtual environment creating
- Windows:
  - `venv\Scripts\activate`  # Make sure scenarios are enabled. `Set-ExecutionPolicy RemoveSigned`
- Linux:
  - TODO
- `pip install -r requirements.txt`  # installing modules

```
usage: CLI_parse_chapter.py [-h] {chapter,title,fav} ...

positional arguments:
  {chapter,title,fav}
    chapter            Download chapter by its id
    title              Title info
    fav                Actions with favourite list

options:
  -h, --help           show this help message and exit
```
Tip to easy use:
  Make .bat file with content:
  ```bat
  @C:\...\async-dex-parser\env\Scripts\python.exe C:\...\async-dex-parser\CLI_parse_chapter.py %*
  ```
