import argparse

from typing import List


def define_argparse(parser_desc: str, parser_arguments: List[list]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"{parser_desc}")

    for argument in parser_arguments:
        parser.add_argument(*argument)
    return parser
