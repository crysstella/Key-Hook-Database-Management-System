import logging

from BuildingType import BuildingType
from Door import Door
from DoorName import DoorName
from Hook import Hook
from Request import Request
from RequestStatus import RequestStatus
from Room import Room
from sqla_util import *

import ClassHandling


def main():
    logging.basicConfig()
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.DEBUG)

    building: BuildingType = ClassHandling.addBuilding("CECS")
    room: Room = ClassHandling.addRoom(building, 302)
    doorName: DoorName = ClassHandling.addDoorName("North")
    print(building)
    print(room)
    print(doorName)

    door: Door = ClassHandling.addDoor(building, room, doorName)
    print(door)

    hook: Hook = ClassHandling.addHook(1, [door])
    print(hook)


if __name__ == '__main__':
    main()
