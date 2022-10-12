from sqlalchemy.orm import Session

from persistency import db_engine
from persistency.models.car_model import Car
from persistency.models.owner_model import Owner


class GarbageCollector:

    def __init__(self):
        self.registered_objects = []

    def register_new_object(self, new_object_id, new_object_modal):
        """
        Register a new object in the list to be deleted.
        """
        self.registered_objects.append({"id": new_object_id, "modal_class": new_object_modal})

    def clean_objects_from_database(self):
        """
        Remove all registered objects from the database.
        """
        db_session = Session(db_engine)

        parent_owners = set()
        for object_to_be_deleted in self.registered_objects:
            modal_class = object_to_be_deleted["modal_class"]
            object_id = object_to_be_deleted["id"]

            if modal_class == Car:
                car_model = db_session.query(Car).filter_by(id=object_id).first()
                parent_owners.add(car_model.owner_id)

            db_session.query(modal_class).filter(modal_class.id == object_id).delete()

        for owner_id in parent_owners:
            db_session.query(Owner).filter(owner_id == Owner.id).delete()

        db_session.commit()
        db_session.close()
