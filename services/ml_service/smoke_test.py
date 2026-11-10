import json
import math
import os
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, ProxyHandler, build_opener


BASE_URL = os.getenv("LAB4_BASE_URL", "http://127.0.0.1:8004")
client = build_opener(ProxyHandler({}))


def send(car_data):
    # Return the status and body for both successful and rejected requests.
    request = Request(
        BASE_URL + "/api/prediction",
        data=json.dumps(car_data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with client.open(request, timeout=15) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        return error.code, json.load(error)


def main():
    sample_path = Path(__file__).with_name("sample_request.json")
    car_data = json.loads(sample_path.read_text())
    status, result = send(car_data)
    assert status == 200, result
    assert result["item_id"] == car_data["item_id"]
    assert math.isclose(result["predict"], 3.749, abs_tol=1e-9)
    print("Normal prediction passed.")

    explicit_age = dict(car_data, Car_Age=4, item_id=1001)
    status, result = send(explicit_age)
    assert status == 200 and result["item_id"] == 1001, result
    assert math.isclose(result["predict"], 3.749, abs_tol=1e-9)
    print("Automatic age and ID exclusion passed.")

    invalid = car_data.copy()
    invalid.pop("Present_Price")
    status, result = send(invalid)
    assert status == 422, result
    print("Missing-field error 422 passed.")

    status, result = send(dict(car_data, Driven_kms=-1))
    assert status == 422, result
    print("Negative-mileage error 422 passed.")

    # Exercise the estimator's numerical error path for the 5xx graph.
    status, result = send(dict(car_data, Present_Price=1e308))
    assert status == 500, result
    print("Deliberate numerical error 500 passed.")

    status, result = send(car_data)
    assert status == 200, result
    assert math.isclose(result["predict"], 3.749, abs_tol=1e-9)
    print("Normal prediction after errors passed.")


if __name__ == "__main__":
    main()
