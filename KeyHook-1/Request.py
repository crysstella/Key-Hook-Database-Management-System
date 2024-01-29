import datetime

from sqlalchemy import Integer, ForeignKey, Column, DateTime, Sequence, String, ForeignKeyConstraint, Identity
from sqlalchemy.orm import relationship

from sqla_util import Base

from Employee import Employee


class Request(Base):
    __tablename__ = "requests"
    requests_id = Column("requests_id", Integer, Identity(start=0, cycle=True), nullable=False, primary_key=True)
    borrow_date = Column("borrow_date", DateTime, nullable=False, primary_key=False)
    employees_id = Column("employees_id", Integer, ForeignKey("employees.id"), nullable=False, primary_key=False)
    rooms_number = Column("rooms_number", Integer, nullable=False, primary_key=False)
    building_type = Column("building_type", String(40), nullable=False, primary_key=False)
    key_id = Column("key_id", Integer, ForeignKey("key_copies.key_id"), nullable=False, primary_key=False)

    table_args = (ForeignKeyConstraint((building_type, rooms_number),
                                       ["rooms.building_type", "rooms.number"]))

    employee = relationship("Employee", back_populates="room_list")
    room = relationship("Room", back_populates="employee_list")

    def __init__(self, borrow_date: datetime, employees_id: int, rooms_number: int,
                 building_type: str, key_id: int):
        self.borrow_date = borrow_date
        self.employees_id = employees_id
        self.rooms_number = rooms_number
        self.building_type = building_type
        self.key_id = key_id

    def __str__(self):
        return f"Request {self.requests_id} from Employee {self.employees_id} for {self.building_type} {self.rooms_number} on {self.borrow_date}"

    def __repr__(self):
        return self.__str__()
