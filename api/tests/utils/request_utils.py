import json

import requests


def request_to_api(endpoint, body_parameters, method):
    if method == "POST":
        response = requests.post("http://127.0.0.1:5000" + endpoint, data=json.dumps(body_parameters),
                                 headers={"Content-Type": "application/json"})
    elif method == "DELETE":
        response = requests.delete("http://127.0.0.1:5000" + endpoint, data=json.dumps(body_parameters),
                                   headers={"Content-Type": "application/json"})
        if len(response.content) == 0:
            return None, response.status_code
    else:
        response = requests.get("http://127.0.0.1:5000" + endpoint, data=json.dumps(body_parameters),
                                headers={"Content-Type": "application/json"})

    return response.json(), response.status_code
