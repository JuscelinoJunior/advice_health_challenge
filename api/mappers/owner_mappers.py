from typing import Dict, Any

from flask import Request

from persistency.models.car_model import Owner


def map_create_owner_request_to_model(request: Request):
    request_data: Dict[str, Any] = request.get_json()
    owner_model: Owner = Owner(first_name=request_data["first-name"], last_name=request_data["last-name"])
    return owner_model


def map_owner_model_response(owner_model: Owner) -> Dict[str, Any]:
    return {"id": owner_model.id, "first-name": owner_model.first_name, "last-name": owner_model.last_name}
