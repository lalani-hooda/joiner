# joiner

Simple command line tool to join two data files on an index and export a flat file of the result

Currently this only supports reading from and writing to `csv`, `excel`, and `json`/`jsonl` files.

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
(venv) $ python ./main.py -l id -r user_id -j left -o data/final.csv data/user.csv data/user_project.csv

# DESCRIPTION
#         left            <_io.TextIOWrapper name='data/user.csv' mode='r' encoding='utf8'>
#         right           <_io.TextIOWrapper name='data/user_project.csv' mode='r' encoding='utf-8'>
#         left_key        id
#         right_key       user_id
#         join_method     left
#         output          data/final.csv
#       id  user_id
# 0  44921  44921.0
# 1  44921  44921.0
# 2  44921  44921.0
# 3  44921  44921.0
# 4  44921  44921.0
```

Command line interface

```
usage: main.py [-h] -l LEFT_KEY [-r RIGHT_KEY] [-j {left,right,inner}] -o OUTPUT left right

a small command line tool to join files

positional arguments:
  left                  left table to join
  right                 right table to join

optional arguments:
  -h, --help            show this help message and exit
  -r RIGHT_KEY, --right-key RIGHT_KEY
                        right field to join on (leave empty for natural join)
  -j {left,right,inner}, --join-method {left,right,inner}
                        SQL equivalent join method

required named arguments:
  -l LEFT_KEY, --left-key LEFT_KEY
                        left field to join on
  -o OUTPUT, --output OUTPUT
                        output file
```
