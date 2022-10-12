from typing import Any, Dict

from flask import Request

from persistency.models.car_model import Car


def map_create_car_request_to_model(request: Request) -> Car:
    request_data: Dict[str, Any] = request.get_json()
    car_model: Car = Car(model=request_data["model"], color=request_data["color"], owner_id=request_data["owner-id"])
    return car_model


def map_car_model_to_response(car_model: Car) -> Dict[str, Any]:
    return {"id": car_model.id, "model": car_model.model, "color": car_model.color, "owner-id": car_model.owner_id}
