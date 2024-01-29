import datetime

from sqlalchemy import Integer, ForeignKey, Column, DateTime
from sqlalchemy.orm import relationship

from sqla_util import Base


class LossRequest(Base):
    __tablename__ = "loss_requests"
    requests_id = Column("requests_id", Integer, ForeignKey("requests.requests_id"), nullable=False, primary_key=True)
    loss_date = Column("loss_date", DateTime, nullable=False, primary_key=False)

    request_relationship = relationship("Request", lazy="subquery")

    def __init__(self, requests_id: int, loss_date: datetime):
        self.requests_id = requests_id
        self.loss_date = loss_date
