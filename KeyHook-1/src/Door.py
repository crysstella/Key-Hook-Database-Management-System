from sqlalchemy import String, Column, ForeignKey, Integer, ForeignKeyConstraint, Sequence, Identity
from sqlalchemy.orm import relationship

import DoorHook
import Hook
from sqla_util import Base
from DoorHook import DoorHook


class Door(Base):
    __tablename__ = "doors"
    id = Column("id", Integer, Identity(start=0, cycle=True), nullable=False, primary_key=True)
    building_type = Column("building_type", String(40), nullable=False, primary_key=False)
    room_number = Column("room_number", Integer, nullable=False, primary_key=False)
    location = Column("location", String(40), ForeignKey("door_names.location"), nullable=False, primary_key=False)

    table_args = (ForeignKeyConstraint((building_type, room_number),
                                       ["rooms.building_type", "rooms.number"]))

    hook_list: [DoorHook] = relationship("DoorHook", back_populates="door", viewonly=False, lazy="subquery")

    def __init__(self, building_type, room_number, location):
        self.building_type = building_type
        self.room_number = room_number
        self.location = location
        self.hook_list = list()

    def add_hook(self, hook: Hook):
        for door_hook in self.hook_list:
            if door_hook == hook:
                return

        door_hook = DoorHook(hook, self)
        hook.door_list.append(door_hook)
        self.hook_list.append(door_hook)

    def __str__(self):
        return f"Door with ID {self.id} at {self.location} of {self.building_type} {self.room_number}"

    def __repr__(self):
        return self.__str__()
