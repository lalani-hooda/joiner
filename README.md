# joiner

Simple command line tool to join two data files on an index and export a flat file of the result

Currently this only supports reading from and writing to `csv` and `excel` files.

## Installation

Clone the repository

```
$ python3 -m venv venv
$ source ./venv/bin/activate
(venv) $ pip install -r requirements.txt
```

## Usage

Example Usage

```bash
(venv) $ python main.py -l user_id -o data/final.csv data/user.csv data/user_project.csv

# DESCRIPTION
#         left            <_io.TextIOWrapper name='data/user.csv' mode='r' encoding='utf8'>
#         right           <_io.TextIOWrapper name='data/user_project.csv' mode='r' encoding='utf-8'>
#         left_key        user_id
#         right_key       user_id
#         output          data/final.csv
#    user_id  user_id
# 0    44921    44921
# 1    44921    44921
# 2    44921    44921
# 3    44921    44921
# 4    44921    44921
```

Command line interface

```
usage: main.py [-h] -l LEFT_KEY [-r RIGHT_KEY] -o OUTPUT left right

a small command line tool to join files

positional arguments:
  left                  left table to join
  right                 right table to join

optional arguments:
  -h, --help            show this help message and exit
  -r RIGHT_KEY, --right-key RIGHT_KEY
                        right field to join on (leave empty for natural join)

required named arguments:
  -l LEFT_KEY, --left-key LEFT_KEY
                        left field to join on
  -o OUTPUT, --output OUTPUT
                        output file
```
