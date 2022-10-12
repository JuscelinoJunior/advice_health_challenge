from sqlalchemy import Column, Integer, ForeignKey, Text

from persistency import Base
from persistency.models.owner_model import Owner


class Car(Base):
    __tablename__ = "car"
    __friendly_class_name__ = "Car"

    id = Column("car_id", Integer, primary_key=True, nullable=False)
    model = Column(Text, nullable=False)
    color = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey(Owner.id), nullable=False)
