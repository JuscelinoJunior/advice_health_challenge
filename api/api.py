from typing import Dict, Any, Tuple, List, Optional

import connexion  # type: ignore
from flask import jsonify, request, Response
from flask_cors import CORS  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm import Session  # type: ignore

from exceptions.exceptions import OwnerAlreadyHasThreeCars, ObjectNotFound, OwnerStillHasACar  # type: ignore
from exceptions.exception_handler import JSONExceptionHandler  # type: ignore
from mappers.car_mappers import map_create_car_request_to_model, map_car_model_to_response  # type: ignore
from mappers.owner_mappers import map_create_owner_request_to_model, map_owner_model_response  # type: ignore
from persistency import db_engine  # type: ignore
from persistency.models.car_model import Car
from persistency.models.owner_model import Owner


def create_car() -> Tuple[Response, int]:
    """
    Add a new car to the database.

    Add a new car defining the model, color and owner identifier. An owner can have only
    three cars. The model has to be one of: hatch, sedan or convertible. The color has to be
    one of: yellow, blue or gray

    :return: a json object with the new car data, including the identifier, and the status code
    :rtype: Tuple

    :raises: OwnerAlreadyHasThreeCars: if the defined owner already has three cars
    """
    car_model: Car = map_create_car_request_to_model(request)

    db_session: Session = Session(db_engine)

    try:
        request_data = request.get_json()
        many_cars = db_session.query(Car).filter(request_data["owner-id"] == Car.owner_id).count()  # type: ignore

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


def delete_car(car_id) -> Tuple[Response, int]:
    """
    Delete a defined car by the identifier.

    :param car_id: identifier of the car to be deleted

    :return: a json object with a success message and the status code
    :rtype: Tuple

    :raises: ObjectNotFound: if the car identifier was not found in the database
    """
    db_session: Session = Session(db_engine)

    try:
        is_deleted: int = db_session.query(Car).filter(car_id == Car.id).delete()
        db_session.commit()
        if is_deleted == 0:
            raise ObjectNotFound()
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify({"description": "The car was deleted successfully"}), 204


def read_all_cars() -> Response:
    """
    Retrieve a list with all the cars from the database.

    :return: a json object with a list with the car data
    :rtype: Response
    """
    db_session: Session = Session(db_engine)

    read_all_cars_response: List[Dict[str, Any]] = []

    try:
        owner_models: List[Car] = db_session.query(Car).all()

        for owner_model in owner_models:
            read_car_response: Dict[str, Any] = map_car_model_to_response(owner_model)
            read_all_cars_response.append(read_car_response)
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify(read_all_cars_response)


def create_owner() -> Tuple[Response, int]:
    """
    Add a new car to the database defining the first name and last name.

    :return: a json object with the new owner data and the status code
    :rtype: Tuple
    """
    owner_model = map_create_owner_request_to_model(request)

    db_session = Session(db_engine)

    try:
        db_session.add(owner_model)
        db_session.commit()
        create_owner_response = map_owner_model_response(owner_model)
    except Exception as exception:
        db_session.rollback()
        raise exception
    finally:
        db_session.close()

    return jsonify(create_owner_response), 201


def delete_owner(owner_id: int) -> Tuple[Response, int]:
    """
    Delete a defined car by the identifier.

    :param owner_id: identifier of the owner to be deleted

    :return: a json object with a success message
    :rtype: Tuple

    :raises: ObjectNotFound: if the owner identifier was not found in the database
    """
    db_session: Session = Session(db_engine)

    try:
        is_deleted: int = db_session.query(Owner).filter(owner_id == Owner.id).delete()
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


def read_all_owners() -> Response:
    """
    Retrieve a list with all the owner from the database.

    :return: a json object with a list with the owner data
    :rtype: Response
    """
    db_session: Session = Session(db_engine)

    read_all_owners_response: List[Dict[str, Any]] = []

    try:
        owner_models: List[Owner] = db_session.query(Owner).all()

        for owner_model in owner_models:
            read_owner_response: Dict[str, Any] = map_owner_model_response(owner_model)
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
