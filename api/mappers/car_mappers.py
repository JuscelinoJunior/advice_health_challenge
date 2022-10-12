from persistency.models.car_model import Car


def map_create_car_request_to_model(request):
    request_data = request.get_json()
    car_model = Car(model=request_data["model"], color=request_data["color"], owner_id=request_data["owner-id"])
    return car_model


def map_car_model_to_response(car_model):
    return {"id": car_model.id, "model": car_model.model, "color": car_model.color, "owner-id": car_model.owner_id}
