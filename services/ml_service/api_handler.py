import pickle

import pandas as pd


REFERENCE_YEAR = 2018
FEATURE_COLUMNS = [
    "Car_Name", "Year", "Present_Price", "Driven_kms", "Fuel_Type",
    "Selling_type", "Transmission", "Owner", "Car_Age",
]


class FastAPIHandler:
    def __init__(self, model_path="/models/model.pkl"):
        # Load the saved Lab2 model once when the service starts.
        with open(model_path, "rb") as model_file:
            self.model = pickle.load(model_file)

    def predict(self, features):
        # Work on a copy so the original input stays available.
        car_data = features.copy()

        # Use the same age calculation as Lab1 and Lab2.
        if car_data.get("Car_Age") is None:
            car_data["Car_Age"] = REFERENCE_YEAR - car_data["Year"]

        # One car becomes one row, with the original feature order.
        frame = pd.DataFrame([car_data])
        frame = frame[FEATURE_COLUMNS]

        # The model returns an array. This API needs the first value.
        predictions = self.model.predict(frame)
        price = float(predictions[0])
        return price
