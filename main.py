import argparse
from enum import Enum, auto
import io
import pandas as pd
import pathlib


class DataType(Enum):
    CSV = auto()
    EXCEL = auto()


def _dump_args(args: argparse.Namespace):
    """dump command line arguments from argparse to stdout

    Args:
        args (argparse.Namespace): parsed command line arguments from argparse
    """

    t = vars(args)
    print('DESCRIPTION')
    [print(f'\t{k:10}\t{t[k]}') for _, k in enumerate(t)]


def _get_data_type(file_path: str) -> DataType:
    """get data type of a file from the file path

    Args:
        file_path (str): path of file

    Returns:
        DataType: enum of data type
    """

    ext = pathlib.Path(file_path).suffix
    if ext == '.csv':
        return DataType.CSV
    if ext in ['.xls', '.xlsx']:
        return DataType.EXCEL


def _read_file(file: io.TextIOWrapper) -> pd.DataFrame:
    """read a file as a pandas dataframe

    Args:
        file (io.TextIOWrapper): file to turn into dataframe

    Returns:
        pd.DataFrame: file loaded as dataframe
    """

    dtype = _get_data_type(file.name)
    if dtype == DataType.CSV:
        return pd.read_csv(file)
    if dtype == DataType.EXCEL:
        return pd.read_excel(file)


def _write_file(df: pd.DataFrame, file_path: str):
    """write dataframe to file

    Args:
        df (pd.DataFrame): dataframe to write
        file_path (str): path of file to write
    """

    dtype = _get_data_type(file_path)
    if dtype == DataType.CSV:
        df.to_csv(file_path, index=False)
    elif dtype == DataType.EXCEL:
        df.to_excel(file_path, index=False)


def _get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='a small command line tool to join files')
    parser.add_argument('left', help='left table to join',
                        type=argparse.FileType('r', encoding='utf8'))
    parser.add_argument('right', help='right table to join',
                        type=argparse.FileType('r', encoding='utf-8'))

    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument(
        '-l', '--left-key', help='left field to join on', required=True)
    parser.add_argument(
        '-r', '--right-key', help='right field to join on (leave empty for natural join)', required=False)
    parser.add_argument('-j', '--join-method', choices=[
                        'left', 'right', 'inner'], help='SQL equivalent join method', default='inner')
    required_named.add_argument(
        '-o', '--output', help='output file', required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    if args.right_key is None:
        args.right_key = args.left_key

    _dump_args(args)

    left_df = _read_file(args.left)
    right_df = _read_file(args.right)

    merged_df = left_df.merge(
        right_df, left_on=args.left_key, right_on=args.right_key, how=args.join_method)
    print(merged_df[[args.left_key, args.right_key]].head())

    _write_file(merged_df, args.output)

    args.left.close()
    args.right.close()
