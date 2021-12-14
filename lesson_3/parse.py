import json
import abc
from copy import deepcopy
from typing import Tuple, Any
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml


def get_io_files(rooms_file_path: str, students_file_path: str) -> Tuple[Any, Any]:
    with open(rooms_file_path, "r") as rooms_file, open(students_file_path) as students_file:
        rooms = json.load(rooms_file)
        students = json.load(students_file)
        return rooms, students


def parse_data(rooms: dict, students: dict) -> dict:
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


class SQLParser:

    @staticmethod
    def parse(data: dict) -> str:
        values_placeholder = ', '.join(['%s'] * len(data))
        columns = ', '.join([f"{key}" for key in data.keys()])
        query = "INSERT INTO room (%s) VALUES (%s)" % (columns, values_placeholder)
        return query


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
