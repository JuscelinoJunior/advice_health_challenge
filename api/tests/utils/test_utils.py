from sqlalchemy.orm import Session

from persistency import db_engine
from persistency.models.car_model import Car
from persistency.models.owner_model import Owner


def create_car_in_database(owner_id):
    db_session = Session(db_engine)

    car_model = Car(model="hatch", color="yellow", owner_id=owner_id)

    db_session.add(car_model)
    db_session.commit()

    car_id = car_model.id

    db_session.close()

    return car_id


def create_owner_in_database():
    owner_model = Owner(first_name="John", last_name="Doe")

    db_session = Session(db_engine)
    db_session.add(owner_model)
    db_session.commit()

    owner_id = owner_model.id

    db_session.close()

    return owner_id
