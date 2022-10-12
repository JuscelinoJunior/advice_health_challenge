from copy import deepcopy

from persistency.models.car_model import Car
from persistency.models.owner_model import Owner
from tests.utils.garbage_collector import GarbageCollector
from tests.utils.request_utils import request_to_api
from tests.utils.test_utils import create_owner_in_database, create_car_in_database

OWNER_BODY_PARAMETERS = {"first-name": "John", "last-name": "Doe"}


def test_create_owner():
    garbage_collector = GarbageCollector()

    try:
        create_owner_response, status_code = request_to_api(endpoint="/owners", body_parameters=OWNER_BODY_PARAMETERS,
                                                            method="POST")

        assert status_code == 201
        assert create_owner_response

        new_owner_id = create_owner_response["id"]

        garbage_collector.register_new_object(new_object_id=new_owner_id, new_object_modal=Owner)
    finally:
        garbage_collector.clean_objects_from_database()


def test_create_owner_without_first_name():
    body_parameters = deepcopy(OWNER_BODY_PARAMETERS)
    del body_parameters["first-name"]

    create_owner_response, status_code = request_to_api(endpoint="/owners", body_parameters=body_parameters,
                                                        method="POST")

    assert status_code == 400
    assert "'first-name' is a required property" in create_owner_response["detail"]


def test_create_owner_without_last_name():
    body_parameters = deepcopy(OWNER_BODY_PARAMETERS)
    del body_parameters["last-name"]

    create_owner_response, status_code = request_to_api(endpoint="/owners", body_parameters=body_parameters,
                                                        method="POST")

    assert status_code == 400
    assert "'last-name' is a required property" in create_owner_response["detail"]


def test_get_owners():
    create_owner_response, status_code = request_to_api(endpoint="/owners", body_parameters=None, method="GET")

    assert status_code == 200


def test_delete_owner():
    garbage_collector = GarbageCollector()

    try:
        owner_id = create_owner_in_database()

        garbage_collector.register_new_object(new_object_id=owner_id, new_object_modal=Owner)

        _, status_code = request_to_api(endpoint="/owners/" + str(owner_id), body_parameters=None, method="DELETE")

        assert status_code == 204
    finally:
        garbage_collector.clean_objects_from_database()


def test_delete_no_existent_owner():
    response, status_code = request_to_api(endpoint="/owners/" + "1200", body_parameters=None, method="DELETE")

    assert status_code == 404
    assert "object was not found" in response["detail"]


def test_delete_owner_still_has_a_car():
    garbage_collector = GarbageCollector()

    try:
        # Create an owner to the database that will be deleted
        owner_id = create_owner_in_database()

        # Create a car in the database so the owner has a car
        car_id = create_car_in_database(owner_id)

        garbage_collector.register_new_object(new_object_id=car_id, new_object_modal=Car)
        garbage_collector.register_new_object(new_object_id=owner_id, new_object_modal=Owner)

        response, status_code = request_to_api(endpoint="/owners/" + str(owner_id),
                                               body_parameters=None, method="DELETE")

        assert status_code == 400
        assert "still has a car" in response["detail"]
    finally:
        garbage_collector.clean_objects_from_database()
