# Description
Python program to parse MangaDex.
You can:
1. Download chapters by their id or url
2. See manga's chapters by their id, url or name
3. Add manga to favourite list
# Installing:
1. `git clone https://github.com/likeinlife/async-dex-parser.git`
2. `python -m venv venv`  # virtual environment creating. You can skip this, but modules will install in global scope.
- Windows:
  - `venv\Scripts\activate`  # Make sure scenarios are enabled. `Set-ExecutionPolicy RemoveSigned`
- Linux:
  - TODO
3. `pip install <your path here>`  # installing modules

# Usage
```
usage: parser [-h] {chapter,title,fav} ...

positional arguments:
  {chapter,title,fav}
    chapter            Download chapter by its id
    title              Title info
    fav                Actions with favourite list

options:
  -h, --help           show this help message and exit
```
# Usage cases
`if you made dex.bat or dex.sh`
- title
  - `dex title c26269c7-0f5d-4966-8cd5-b79acb86fb7a` - will show Sewayaki Kitsune manga information
  - `dex title Sewayaki Kitsune`
  - `dex title Sewayaki Kitsune --mass` - will download all available chapters on english language
  - `dex title Sewayaki Kitsune -m -l any` - will download all available chapters on any language

- chapter
  - `dex chapter ce7f8709-c27c-465d-bdd9-d9c0c99b3735` - will download Sewayaki Kitsune 91 chapter

- favoruite list
  - `dex fav list` - show your favourite list
  - `dex fav add -id c26269c7-0f5d-4966-8cd5-b79acb86fb7a -t Sewayaki Kitsune` - add Sewayaki Kitsune manga to your favourite list
  - `dex fav del -id ce7f8709-c27c-465d-bdd9-d9c0c99b3735` - delete Sewayaki Kitsune from your favourite list

# Tip to easy use:

  1. Make .bat file with content:
  ```bat
  @C:\...\async-dex-parser\env\Scripts\python.exe -m app %*
  ```
  2. Write path of .bat file to you environment variables

