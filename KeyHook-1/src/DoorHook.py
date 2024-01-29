from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from sqla_util import Base


class DoorHook(Base):
    __tablename__ = "door_hook_junction"
    hook_id = Column("hook_id", Integer, ForeignKey("hooks.id"), nullable=False, primary_key=True)
    door_id = Column("door_id", Integer, ForeignKey("doors.id"), nullable=False, primary_key=True)

    door = relationship("Door", back_populates="hook_list", lazy="subquery")
    hook = relationship("Hook", back_populates="door_list", lazy="subquery")

    def __init__(self, hook_id: int, door_id: int):
        self.hook_id = hook_id
        self.door_id = door_id

    def __str__(self):
        return f"Hook {self.hook_id} → Door {self.door_id}"

    def __repr__(self):
        return self.__str__()
