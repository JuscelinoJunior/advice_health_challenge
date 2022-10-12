from sqlalchemy import Column, Integer, Text

from persistency import Base


class Owner(Base):
    __tablename__ = "owner"
    __friendly_class_name__ = "Owner"

    id = Column("owner_id", Integer, primary_key=True, nullable=False)
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
