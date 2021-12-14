from typing import Union

from mysql.connector import CMySQLConnection
from mysql.connector.cursor_cext import CMySQLCursor

import schemas
from config import get_session  # bing_schema


class Session:
    def __init__(self, connection: CMySQLConnection):
        self.connection = connection

    def execute(self, query, params: tuple = None) -> CMySQLCursor:
        with get_session(self.connection) as session:
            cursor = session.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor

    def create_schema(self, schema: Union[str, dict, list]) -> None:
        if isinstance(schema, str):
            self.execute(schema)
        if isinstance(schema, dict):
            for table in schema:
                self.execute(schema[table])
        if isinstance(schema, list):
            for table in schema:
                self.execute(table)

    def insert(self, table, data: dict) -> None:
        try:
            values_placeholder = ', '.join(['%s'] * len(data))
            columns = ', '.join([key for key in data.keys()])
            query = "INSERT INTO %s (%s) VALUES (%s)" % (table, columns, values_placeholder)
            self.execute(query, tuple(data.values()))
        except Exception as e:
            print(e)


class Service:
    def __init__(self, session):
        self.session = session

    def add_rooms(self, rooms: list) -> None:
        for room in rooms:
            self.session.insert('room', room)
        self.session.connection.close()

    def add_students(self, students: list) -> None:
        for student in students:
            self.session.insert('student', student)
        self.session.connection.close()

    def get_room_studs_count(self) -> CMySQLCursor:
        query = "SELECT `room`, COUNT(*) FROM `student` GROUP BY `room`"
        cursor = self.session.execute(query)
        return cursor

    def get_younger_students_room(self, limit: int = 5) -> CMySQLCursor:
        query = 'SELECT AVG(`birthday`), `room` FROM `student` GROUP BY `room` ORDER BY `birthday` LIMIT %s'
        cursor = self.session.execute(query, (limit, ))
        return cursor

    def get_highest_age_diff(self, limit: int = 5) -> CMySQLCursor:
        query = 'SELECT DATEDIFF(min(`birthday`), max(`birthday`)) AS `diff`, `room`  ' \
                'FROM `student`  GROUP BY `room` ORDER BY `diff` LIMIT %s'
        cursor = self.session.execute(query, (limit, ))
        return cursor

    def get_diff_gender_rooms(self) -> CMySQLCursor:
        query = 'SELECT `room`.`id`, `room`.`name` FROM `room` ' \
                'JOIN (SELECT * FROM `student` WHERE `sex`="M") AS male_studs ' \
                'JOIN (SELECT * FROM `student` WHERE `sex`="F") AS female_studs ' \
                'ON `male_studs`.`room`=`room`.`id` AND `female_studs`.`room`=`room`.`id` GROUP BY(`room`.`id`);'
        cursor = self.session.execute(query)
        return cursor


class PrettyOutService(Service):

    # @bing_schema(schema=schemas.RoomCount)
    def get_room_studs_count(self) -> list:
        return [schemas.RoomCount(*record) for record in super().get_room_studs_count()]

    # @bing_schema(schema=schemas.RoomDiffGender)
    def get_diff_gender_rooms(self) -> list:
        return [schemas.RoomDiffGender(*record) for record in super().get_diff_gender_rooms()]

    # @bing_schema(schema=schemas.YoungStudentRoom)
    def get_younger_students_room(self, limit: int = 5) -> list:
        return [schemas.YoungStudentRoom(*record) for record in super().get_younger_students_room(limit)]

    # @bing_schema(schema=schemas.BiggestAgeDiff)
    def get_highest_age_diff(self, limit: int = 5) -> list:
        return [schemas.BiggestAgeDiff(*record) for record in super().get_highest_age_diff(limit)]
