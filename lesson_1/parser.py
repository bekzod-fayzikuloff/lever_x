"""
    Постарался изменить механизм выполнения задания, добавить возможность расширения путем простого наследования от
    абстрактного класса переопределением астрактных методов и появится возможность внедрения новых поддерживаемых
    форматов без добавления условий, также можно добавить плюшки с помощью класса наследующего от str и Enum
    Ну и оптимизировать перебор элементов и теперь оно O(n + m)
"""
from argparse import ArgumentParser
import json
import abc
from copy import deepcopy
from typing import Tuple, Any
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml

import argument_parser
import exceptions


def get_io_files(rooms_file_path: str, students_file_path: str) -> Tuple[Any, Any]:
    with open(rooms_file_path, "r") as rooms_file, open(students_file_path) as students_file:
        rooms = json.load(rooms_file)
        students = json.load(students_file)
        return rooms, students


def _parse_data(rooms: dict, students: dict) -> dict:
    """
    Getting information from files and return formatted dict
    :return:
    """
    rooms_copy = deepcopy(rooms)

    for index, room in enumerate(rooms):
        room_students: list = []
        rooms_copy[index]["room_students"] = room_students

    for student in students:
        rooms_copy[student["room"]]["room_students"].append(student)

    return rooms_copy


class Parser(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def parse(self, data):
        pass

    @abc.abstractstaticmethod
    def get_type():
        pass


class JsonParser(Parser):
    """
        Класс реализуещий логику взаимодействия с json файлами
    """

    def parse(self, data: dict) -> str:
        return json.dumps(data, indent=4)

    @staticmethod
    def get_type():
        return "json"


class XmlParser(Parser):
    """
        Класс реализуещий логику взаимодействия с xml файлами
    """
    def parse(self, data: dict) -> str:

        def node_rename(node):
            return "room" if len(node) < 5 else "student"

        xml = dicttoxml(data, attr_type=False, custom_root="Room", item_func=node_rename)
        pretty_xml = parseString(xml).toprettyxml()
        return pretty_xml

    @staticmethod
    def get_type():
        return "xml"


class DataWriter:
    """
        Класс имплементирующий обращение к классам реализующие дальнейщую логику программы
    """

    def __init__(self, engine):
        """
        :param engine:
        """
        self.engine = engine

    def write_file(self, output: str, data: dict) -> None:
        """
        :param output:
        :param data:
        :return:
        """
        with open(output, "w") as file:
            file.write(self.engine.parse(data))


def main(parser: ArgumentParser) -> None:
    arguments = vars(parser.parse_args())

    students_file_path: str = arguments.get("students")
    rooms_file_path: str = arguments.get("rooms")
    out_filename: str = arguments.get("output")

    if out_filename.rsplit(".")[-1] in [sub.get_type() for sub in Parser.__subclasses__()]:
        for subclass in Parser.__subclasses__():
            if out_filename.rsplit(".")[-1] == subclass.get_type():
                input_data = _parse_data(*get_io_files(rooms_file_path, students_file_path))
                DataWriter(subclass()).write_file(out_filename, input_data)
    else:
        raise exceptions.UnSupportedTypeException("Unsupported file type")


if __name__ == "__main__":
    argument_conf = [
        ['-s', '--students'],
        ['-r', '--rooms'],
        ['-o', '--output']
    ]
    main(argument_parser.define_argparse("dsdsd", argument_conf))
