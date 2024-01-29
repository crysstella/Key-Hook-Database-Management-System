from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from sqla_util import Base


class DoorName(Base):
    __tablename__ = "door_names"
    location = Column("location", String(40), nullable=False, primary_key=True)

    door = relationship("Door", lazy="subquery")

    def __init__(self, location: str):
        self.location = location

    def __str__(self):
        return f"{self.location}"

    def __repr__(self):
        return self.__str__()
