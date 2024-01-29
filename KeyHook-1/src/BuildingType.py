from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

import Room
from sqla_util import Base


class BuildingType(Base):
    __tablename__ = "building_types"
    type = Column("type", String(40), nullable=False, primary_key=True)

    rooms: [Room] = relationship("Room", back_populates="type", viewonly=False, lazy="subquery")

    def __init__(self, type: str):
        self.type = type

    def __str__(self):
        return f"{self.type}"

    def __repr__(self):
        return self.__str__
