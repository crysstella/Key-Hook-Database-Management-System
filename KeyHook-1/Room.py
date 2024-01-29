from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

import Request
from sqla_util import Base


class Room(Base):
    __tablename__ = "rooms"
    building_type = Column("building_type", String(40), ForeignKey("building_types.type"),
                           nullable=False, primary_key=True)
    number = Column("number", Integer, nullable=False, primary_key=True)

    employee_list: [Request] = relationship("Request", lazy="subquery")

    type = relationship("BuildingType", back_populates="rooms")

    def __init__(self, building_type: str, number: int):
        self.building_type = building_type
        self.number = number

    def __str__(self):
        return f"{self.building_type} {self.number}"

    def __repr__(self):
        return self.__str__()
