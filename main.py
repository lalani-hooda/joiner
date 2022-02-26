import argparse
import io
import logging
import pathlib
from enum import Enum, auto

import pandas as pd


class DataType(Enum):
    CSV = auto()
    EXCEL = auto()
    JSON = auto()
    JSONL = auto()


def _dump_args(args: argparse.Namespace):
    """dump command line arguments from argparse to stdout

    Args:
        args (argparse.Namespace): parsed command line arguments from argparse
    """

    t = vars(args)
    s = ["DESCRIPTION"]
    [s.append(f"\t{k:10}\t{t[k]}") for _, k in enumerate(t)]
    logging.debug("\n".join(s))


def _get_data_type(file_path: str) -> DataType:
    """get data type of a file from the file path

    Args:
        file_path (str): path of file

    Returns:
        DataType: enum of data type
    """

    assert len(DataType) == 4, "_get_data_type: non-exhaustive handling of data types"
    ext = pathlib.Path(file_path).suffix
    if ext == ".csv":
        return DataType.CSV
    if ext in [".xls", ".xlsx"]:
        return DataType.EXCEL
    if ext == ".json":
        return DataType.JSON
    if ext == ".jsonl":
        return DataType.JSONL


def _read_file(file_path: str) -> pd.DataFrame:
    """read a file as a pandas dataframe

    Args:
        file_path (str): path of file to turn into dataframe

    Returns:
        pd.DataFrame: file loaded as dataframe
    """

    assert len(DataType) == 4, "_read_file: non-exhaustive handling of data types"
    dtype = _get_data_type(file_path)

    logging.info(f"reading file: {file_path!r} of data type: {dtype!s}")
    if dtype == DataType.CSV:
        return pd.read_csv(file_path)
    if dtype == DataType.EXCEL:
        return pd.read_excel(file_path)
    if dtype == DataType.JSON:
        return pd.read_json(file_path)
    if dtype == DataType.JSONL:
        return pd.read_json(file_path, lines=True)


def _write_file(df: pd.DataFrame, file_path: str):
    """write dataframe to file

    Args:
        df (pd.DataFrame): dataframe to write
        file_path (str): path of file to write
    """

    assert len(DataType) == 4, "_write_file: non-exhaustive handling of data types"
    dtype = _get_data_type(file_path)

    logging.info(f"writing file: {file_path!r} of data type: {dtype!s}")
    if dtype == DataType.CSV:
        df.to_csv(file_path, index=False)
    elif dtype == DataType.EXCEL:
        df.to_excel(file_path, index=False)
    elif dtype == DataType.JSON:
        df.to_json(file_path, orient="records")
    elif dtype == DataType.JSONL:
        df.to_json(file_path, lines=True, orient="records")


def _get_args() -> argparse.Namespace:
    """receive and parse command line arguments

    Returns:
        argparse.Namespace: parsed arguments
    """

    parser = argparse.ArgumentParser(
        description="a small command line tool to join files"
    )
    parser.add_argument(
        "left",
        help="left table to join",
        type=argparse.FileType("r", encoding="unicode_escape"),
    )
    parser.add_argument(
        "right",
        help="right table to join",
        type=argparse.FileType("r", encoding="unicode_escape"),
    )

    required_named = parser.add_argument_group("required named arguments")
    required_named.add_argument(
        "-l", "--left-key", help="left field to join on", required=True
    )
    parser.add_argument(
        "-r",
        "--right-key",
        help="right field to join on (leave empty for natural join)",
        required=False,
    )
    parser.add_argument(
        "-c",
        "--cardinality",
        choices=["1:1", "1:m", "m:1", "m:m"],
        help="validate data cardinality during join",
        default="m:m",
    )
    parser.add_argument(
        "-j",
        "--join-method",
        choices=["left", "right", "outer", "inner", "cross"],
        help="SQL equivalent join method",
        default="inner",
    )
    parser.add_argument("-v", "--verbose", help="verbose output", action="store_true")
    required_named.add_argument("-o", "--output", help="output file", required=True)

    return parser.parse_args()


if __name__ == "__main__":
    args = _get_args()

    if args.right_key is None:
        args.right_key = args.left_key

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.ERROR)

    _dump_args(args)

    left_name = args.left.name
    right_name = args.right.name

    args.left.close()
    args.right.close()

    left_df = _read_file(left_name)
    right_df = _read_file(right_name)

    try:
        logging.info(
            f"joining:\n\tdataframes: {left_name!r} & {right_name!r}\n\ton: {args.left_key!r} = {args.right_key!r}\n\twith: {args.cardinality!r} cardinality"
        )
        merged_df = left_df.merge(
            right_df,
            left_on=args.left_key,
            right_on=args.right_key,
            how=args.join_method,
            validate=args.cardinality,
            indicator=True,
        )
        logging.debug(f"\n{merged_df[[args.left_key, args.right_key]].head()!r}")
    except pd.errors.MergeError as e:
        logging.error(e)
        exit(1)

    _write_file(merged_df, args.output)
