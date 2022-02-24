# joiner

Simple command line tool to join two data files on an index and export a flat file of the result

## Installation

Clone the repository
```
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Usage

| short | long          | value | description            |
|:----- |:------------- | ----- | ---------------------- |
| `-l`  | `--left`      | `str` | left 'table' to join   |
| `-r`  | `--right`     | `str` | right 'table' to join  |
| `-lk` | `--left-key`  | `str` | left field to join on  |
| `-rk` | `--right-key` | `str` | right field to join on |

