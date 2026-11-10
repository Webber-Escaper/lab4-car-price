import os
import random
import time

import httpx


# Compose uses the service name. An environment variable also allows local tests.
URL = os.getenv("ML_SERVICE_URL", "http://ml_service:8000/api/prediction")


def main():
    item_id = 1
    while True:

        car_data = {
            "item_id": item_id,
            "Car_Name": random.choice(["ritz", "ciaz", "swift", "fortuner"]),
            "Year": random.randint(2010, 2018),
            "Present_Price": round(random.uniform(5.0, 30.0), 2),
            "Driven_kms": random.randint(5000, 120000),
            "Fuel_Type": random.choice(["Petrol", "Diesel"]),
            "Selling_type": random.choice(["Dealer", "Individual"]),
            "Transmission": random.choice(["Manual", "Automatic"]),
            "Owner": random.randint(0, 2),
        }
        # Show the actual input
        print("Car data:", car_data, flush=True)

        try:
            response = httpx.post(URL, json=car_data, timeout=10)
            print(item_id, response.status_code, response.text, flush=True)
        except httpx.HTTPError as error:
            # Keep the loop alive if the service is temporarily unavailable.
            print("Request failed:", error, flush=True)

        item_id = item_id + 1
        # The teacher suggests a random delay between zero and five seconds.
        delay = random.uniform(0, 5)
        time.sleep(delay)


if __name__ == "__main__":
    main()
