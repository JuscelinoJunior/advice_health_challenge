from copy import deepcopy

from persistency.models.car_model import Car
from persistency.models.owner_model import Owner
from tests.utils.garbage_collector import GarbageCollector
from tests.utils.request_utils import request_to_api
from tests.utils.test_utils import create_car_in_database, create_owner_in_database

CAR_BODY_PARAMETERS = {"model": "hatch", "color": "yellow"}


def test_create_car():
    garbage_collector = GarbageCollector()

    try:
        car_owner_id = create_owner_in_database()

        body_parameters = deepcopy(CAR_BODY_PARAMETERS)

        body_parameters["owner-id"] = car_owner_id

        create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")
        
        assert status_code == 201

        new_car_id = create_car_response["id"]
        garbage_collector.register_new_object(new_object_id=new_car_id, new_object_modal=Car)
    finally:
        garbage_collector.clean_objects_from_database()


def test_create_car_same_owner_after_three_times():
    garbage_collector = GarbageCollector()

    try:
        car_owner_id = create_owner_in_database()

        body_parameters = deepcopy(CAR_BODY_PARAMETERS)
        body_parameters["owner-id"] = car_owner_id

        for _ in range(0, 3):
            create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

            assert status_code == 201

            new_car_id = create_car_response["id"]
            garbage_collector.register_new_object(new_object_id=new_car_id, new_object_modal=Car)

        create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

        assert status_code == 400
        assert "The selected owner already has three cars" in create_car_response["detail"]
    finally:
        garbage_collector.clean_objects_from_database()


def test_create_car_without_model():
    body_parameters = deepcopy(CAR_BODY_PARAMETERS)
    del body_parameters["model"]

    create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

    assert status_code == 400
    assert "'model' is a required property" in create_car_response["detail"]


def test_create_car_without_color():
    body_parameters = deepcopy(CAR_BODY_PARAMETERS)
    del body_parameters["color"]

    create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

    assert status_code == 400
    assert "'color' is a required property" in create_car_response["detail"]


def test_create_car_without_owner_id():
    create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=CAR_BODY_PARAMETERS, method="POST")

    assert status_code == 400
    assert "'owner-id' is a required property" in create_car_response["detail"]


def test_create_car_with_invalid_color():
    body_parameters = deepcopy(CAR_BODY_PARAMETERS)
    body_parameters["owner-id"] = 1
    body_parameters["color"] = "white"

    create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

    assert status_code == 400
    assert "'white' is not one of" in create_car_response["detail"]


def test_create_car_with_invalid_model():
    body_parameters = deepcopy(CAR_BODY_PARAMETERS)
    body_parameters["owner-id"] = 1
    body_parameters["model"] = "bus"

    create_car_response, status_code = request_to_api(endpoint="/cars", body_parameters=body_parameters, method="POST")

    assert status_code == 400
    assert "'bus' is not one of" in create_car_response["detail"]


def test_get_cars():
    create_owner_response, status_code = request_to_api(endpoint="/cars", body_parameters=None, method="GET")

    assert status_code == 200


def test_delete_cars():
    garbage_collector = GarbageCollector()

    try:
        # Create an owner so the car can have an owner
        owner_id = create_owner_in_database()

        # Create a car in the database that will be deleted
        car_id = create_car_in_database(owner_id)

        garbage_collector.register_new_object(new_object_id=owner_id, new_object_modal=Owner)

        response, status_code = request_to_api(endpoint="/cars/" + str(car_id), body_parameters=None, method="DELETE")

        assert status_code == 204
    finally:
        garbage_collector.clean_objects_from_database()


def test_delete_no_existent_car():
    response, status_code = request_to_api(endpoint="/owners/1200", body_parameters=None, method="DELETE")

    assert status_code == 404
    assert "object was not found" in response["detail"]
