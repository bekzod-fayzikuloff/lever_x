from argparse import ArgumentParser

from mysql import connector
from mysql.connector import CMySQLConnection

import db
import parse
import exceptions
from config import connection_config, define_argparse


def main(service: db.PrettyOutService, parser: ArgumentParser) -> None:
    arguments = vars(parser.parse_args())

    students_file_path: str = arguments.get("students")
    rooms_file_path: str = arguments.get("rooms")
    out_filename: str = arguments.get("output")

    if out_filename.rsplit(".")[-1] in [sub.get_type() for sub in parse.Parser.__subclasses__()]:
        for subclass in parse.Parser.__subclasses__():
            if out_filename.rsplit(".")[-1] == subclass.get_type():

                for record in [*service.get_highest_age_diff(), *service.get_diff_gender_rooms(),
                               *service.get_younger_students_room(), *service.get_room_studs_count()]:

                    parse.DataWriter(subclass()).write_file(out_filename, record.__dict__)
    else:
        raise exceptions.UnSupportedTypeException("Unsupported file type")


if __name__ == "__main__":
    conn: CMySQLConnection = connector.connect(**connection_config.__dict__)
    session = db.Session(connection=conn)
    ser = db.PrettyOutService(session)

    argument_conf = [
        ['-du', '--user'],
        ['-dp', '--password'],
        ['-dh', '--host'],
        ['-d', '--database'],
        ['-s', '--students'],
        ['-r', '--rooms'],
        ['-o', '--output']
    ]

    main(ser, define_argparse("Mysql python", argument_conf))
