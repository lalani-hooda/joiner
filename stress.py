import argparse
import logging
import time

from main import _get_args, _dump_args, main


def _render_test_args(num_records: int) -> list[str]:
    """render test args and return the list of arguments

    Args:
        num_records (int): number of records for files in `samples` dir

    Returns:
        list[str]: list of rendered arguments
    """

    return [
        "-l",
        "movie_id",
        "-j",
        "left",
        "-c",
        "m:1",
        "-o",
        "samples/joined.csv",
        f"samples/{num_records//1000}k.csv",
        "samples/mubi_movie_data.csv",
    ]


if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)

    print(f"{'rows':<10}  time")
    for n in [10_000, 25_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]:
        args = _render_test_args(n)

        start = time.time()
        main(args)
        end = time.time() - start
        s = f"{n//1000}k:"
        print(f"{s:<10} {end:.2f}s")
