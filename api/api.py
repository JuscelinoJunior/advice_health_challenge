import connexion
from flask import jsonify, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from exceptions.exceptions import OwnerAlreadyHasThreeCars, ObjectNotFound, OwnerStillHasACar
from exceptions.exception_handler import JSONExceptionHandler
from mappers.car_mappers import map_create_car_request_to_model, map_car_model_to_response
from mappers.owner_mappers import map_create_owner_request_to_model, map_owner_model_response
from persistency import db_engine
from persistency.models.car_model import Car
from persistency.models.owner_model import Owner


def create_car():
    """
    Add a new car to the database.

    Add a new car defining the model, color and owner identifier. An owner can have only
    three cars. The model has to be one of: hatch, sedan or convertible. The color has to be
    one of: yellow, blue or gray

    :return: a json object with the new car data, including the identifier
    :rtype: Dict

    :raises OwnerAlreadyHasThreeCars: if the defined owner already has three cars
    """
    car_model = map_create_car_request_to_model(request)

    db_session = Session(db_engine)

    try:
        request_data = request.get_json()
        many_cars = db_session.query(Car).filter(request_data["owner-id"] == Car.owner_id).count()

        if many_cars > 2:
            raise OwnerAlreadyHasThreeCars()

        db_session.add(car_model)
        db_session.commit()
        create_car_response = map_car_model_to_response(car_model)
        return jsonify(create_car_response), 201
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()


def delete_car(car_id):
    """
    Delete a defined car by the identifier.

    :param car_id: identifier of the car to be deleted

    :return: a json object with a success message
    :rtype: Dict

    :raises ObjectNotFound: if the car identifier was not found in the database
    """
    db_session = Session(db_engine)

    try:
        is_deleted = db_session.query(Car).filter(car_id == Car.id).delete()
        db_session.commit()
        if is_deleted == 0:
            raise ObjectNotFound()
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify({"description": "The car was deleted successfully"}), 204


def read_all_cars():
    """
    Retrieve a list with all the cars from the database.

    :return: a json object with a list with the car data
    :rtype: Dict
    """
    db_session = Session(db_engine)

    read_all_cars_response = []

    try:
        owner_models = db_session.query(Car)

        for owner_model in owner_models:
            read_car_response = map_car_model_to_response(owner_model)
            read_all_cars_response.append(read_car_response)
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify(read_all_cars_response)


def create_owner():
    """
    Add a new car to the database defining the first name and last name.

    :return: a json object with the new owner data
    :rtype: Dict
    """
    owner_model = map_create_owner_request_to_model(request)

    db_session = Session(db_engine)

    try:
        db_session.add(owner_model)
        db_session.commit()
        create_owner_response = map_owner_model_response(owner_model)
        return jsonify(create_owner_response), 201
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()


def delete_owner(owner_id):
    """
    Delete a defined car by the identifier.

    :param owner_id: identifier of the owner to be deleted

    :return: a json object with a success message
    :rtype: Dict

    :raises ObjectNotFound: if the owner identifier was not found in the database
    """
    db_session = Session(db_engine)

    try:
        is_deleted = db_session.query(Owner).filter(owner_id == Owner.id).delete()
        db_session.commit()

        if is_deleted == 0:
            raise ObjectNotFound()
    except Exception as exception:
        db_session.rollback()

        if isinstance(exception, IntegrityError):
            raise OwnerStillHasACar() from exception

        raise exception
    finally:
        db_session.close()

    return jsonify({"description": "The owner was deleted successfully"}), 204


def read_all_owners():
    """
    Retrieve a list with all the owner from the database.

    :return: a json object with a list with the owner data
    :rtype: Dict
    """
    db_session = Session(db_engine)

    read_all_owners_response = []

    try:
        owner_models = db_session.query(Owner)

        for owner_model in owner_models:
            read_owner_response = map_owner_model_response(owner_model)
            read_all_owners_response.append(read_owner_response)
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify(read_all_owners_response)


if __name__ == "__main__":
    app = connexion.FlaskApp(__name__, specification_dir='openapi_specifications/')
    webapp = app.app
    CORS(webapp)
    handler = JSONExceptionHandler(app)
    app.add_api("api.json")
    app.run(debug=True)
