import argparse
import dataclasses
import os
from functools import wraps
from typing import List
from contextlib import contextmanager

import dotenv

dotenv.load_dotenv()


@contextmanager
def get_session(connection):
    try:
        yield connection
    finally:
        pass


def define_argparse(parser_desc: str, parser_arguments: List[list]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=f"{parser_desc}")

    for argument in parser_arguments:
        parser.add_argument(*argument)

    return parser


@dataclasses.dataclass
class DBConfig:
    user: str
    password: str
    host: str
    database: str


def bing_schema(schema):
    def _bind(func):

        @wraps(func)
        def inner(*args, **kwargs):
            return schema(*func(*args, **kwargs))
        return inner

    return _bind


user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
database = os.getenv('database')

connection_config = DBConfig(user=user,
                             password=password,
                             host=host,
                             database=database)
