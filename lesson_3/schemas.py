import dataclasses
import datetime


@dataclasses.dataclass
class RoomCount:
    room_id: int
    student_count: int


@dataclasses.dataclass
class Room:
    id: int
    name: str


class RoomDiffGender(Room):
    pass


class BiggestAgeDiff:
    def __init__(self, time_diff, room_id):
        self.time_diff = time_diff
        self.room_id = room_id


class YoungStudentRoom:

    def __init__(self, avg_year_time, room_id):
        self.avg_year_time = datetime.datetime.fromtimestamp(avg_year_time.__float__()).__str__()
        self.room_id = room_id
