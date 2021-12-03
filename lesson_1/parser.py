import json
import abc
from copy import deepcopy
from typing import Optional
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml

from lesson_1 import exceptions


class ParseData:
    """
    """

    def __init__(self, room_file_path: str, student_file_path: str):
        """
        :param room_file_path:
        :param student_file_path:
        """
        self.room_file_path = room_file_path
        self.student_file_path = student_file_path

    def parse_data(self) -> dict:
        """
        Getting information from files and return formatted dict
        :return:
        """
        with open(self.room_file_path, "r") as room_file, open(self.student_file_path, "r") as student_file:
            rooms = json.load(room_file)
            students = json.load(student_file)

        rooms_copy = deepcopy(rooms)

        for index, room in enumerate(rooms):
            room_students: list = []
            for student in students:
                if room["id"] == student["room"]:
                    room_students.append(student)
            rooms_copy[index]["room_students"] = room_students

        return rooms_copy


class Writer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def write_file(self, data):
        pass


class JsonWriter(Writer):
    """
        Класс реализуещий логику взаимодействия с json файлами
    """

    def __init__(self, filename: Optional[str] = "output.json"):
        self.filename = filename
        _filetype = self.filename.lower().rsplit(".")[-1]
        if _filetype != "json":
            raise exceptions.UnSupportedTypeException("Unsupported file type \nneed file with .json extension")

    def write_file(self, data: dict) -> None:
        if data is None:
            data = {}
        with open(self.filename, 'w+') as file:
            file.write(json.dumps(data, indent=4))


class XmlWriter(Writer):
    """
        Класс реализуещий логику взаимодействия с xml файлами
    """

    def __init__(self, filename: Optional[str] = "output.xml"):
        self.filename = filename
        _filetype = filename.lower().rsplit(".")[-1]
        if _filetype != "xml":
            raise exceptions.UnSupportedTypeException("Unsupported file type \nneed file with .json extension")

    def write_file(self, data: dict) -> None:

        def node_rename(node):
            return "room" if len(node) < 5 else "student"

        xml = dicttoxml(data, attr_type=False, custom_root="Room", item_func=node_rename)
        pretty_xml = parseString(xml).toprettyxml()
        with open(self.filename, 'w+') as file:
            file.write(pretty_xml)


class DataWriter:
    """
        Класс имплементирующий обращение к классам реализующие дальнейщую логику программы
    """

    def __init__(self, filename):
        """
        :param filename:
        """
        self.filename = filename
        _filetype = filename.lower().rsplit(".")[-1]
        if _filetype == "xml":
            self.engine = XmlWriter(self.filename)
        elif _filetype == "json":
            self.engine = JsonWriter(self.filename)
        else:
            raise exceptions.UnSupportedTypeException("Unsupported file type \nNeed file with .json or xml extension")

    def write_file(self, data: dict) -> None:
        """
        :param data:
        :return:
        """
        self.engine.write_file(data)


if __name__ == "__main__":
    file_parser = ParseData("rooms.json", "students.json")
    file_content = file_parser.parse_data()
    data_writer = DataWriter("output.xml")
    data_writer.write_file(file_content)
