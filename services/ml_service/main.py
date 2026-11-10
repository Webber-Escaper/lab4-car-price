import json

from fastapi import FastAPI, HTTPException, Response
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Gauge, Histogram
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from pydantic import BaseModel, Field

from api_handler import FastAPIHandler, REFERENCE_YEAR


app = FastAPI(title="LR4 Car Price Prediction Service", version="3.0", docs_url=None)
# Serve the Swagger page files locally for an offline classroom demonstration.
app.mount("/static", StaticFiles(directory="static"), name="static")
handler = FastAPIHandler()


class CarFeatures(BaseModel):
    # Keep the Lab3 format: the ID and car features share one JSON body.
    item_id: int = Field(ge=0, examples=[123])
    Car_Name: str = Field(examples=["ritz"])
    Year: int = Field(ge=1990, le=REFERENCE_YEAR, examples=[2014])
    Present_Price: float = Field(gt=0, allow_inf_nan=False, examples=[5.59])
    Driven_kms: int = Field(ge=0, examples=[27000])
    Fuel_Type: str = Field(examples=["Petrol"])
    Selling_type: str = Field(examples=["Dealer"])
    Transmission: str = Field(examples=["Manual"])
    Owner: int = Field(ge=0, examples=[0])
    Car_Age: int | None = Field(default=None, ge=0, examples=[4])


# Count prediction requests separately for each HTTP status code.
REQUEST_COUNT = Counter("http_requests_total", "Prediction requests", ["status"])
for status in ["200", "422", "500"]:
    REQUEST_COUNT.labels(status=status).inc(0)

# Histogram limits use the same price unit as the original dataset.
PRICE_BUCKETS = [0, 1, 2, 3, 5, 8, 12, 20, 35, 50, 100]
PREDICTED_PRICES = Histogram(
    "model_prediction_value", "Predicted selling prices", buckets=PRICE_BUCKETS
)
INPUT_PRICES = Histogram(
    "input_present_price", "Reference prices of successfully predicted cars",
    buckets=PRICE_BUCKETS,
)

# This fixed reference was calculated from the Lab2 cleaned dataset.
with open("/models/reference_data.json") as reference_file:
    reference_data = json.load(reference_file)
REFERENCE_PRICE = Gauge("reference_present_price_mean", "Lab2 mean reference price")
REFERENCE_PRICE.set(reference_data["present_price_mean"])


@app.middleware("http")
async def count_prediction_requests(request, call_next):
    # Health checks and metric collection do not count as prediction requests.
    if request.url.path != "/api/prediction":
        return await call_next(request)

    status = 500
    try:
        # Let FastAPI validate the input and run the requested endpoint.
        response = await call_next(request)
        status = response.status_code
        return response
    finally:
        # Also count rejected inputs and unexpected server errors.
        REQUEST_COUNT.labels(status=str(status)).inc()


@app.get("/")
def root():
    return {"Hello": "World"}


@app.get("/health")
def health():
    return {"status": "ok", "service_version": 3}


@app.get("/docs", include_in_schema=False)
def docs():
    return get_swagger_ui_html(
        openapi_url="/openapi.json", title="Lab4 API",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css", swagger_favicon_url="data:,",
    )


@app.get("/metrics", include_in_schema=False)
def metrics():
    # Prometheus reads this text endpoint every five seconds.
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/api/prediction")
def prediction(data: CarFeatures):
    item_id = data.item_id
    # The ID is returned to the caller and excluded from the model input.
    features = data.model_dump(exclude={"item_id"})

    try:
        price = handler.predict(features)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    # Only successful predictions enter these two histograms.
    PREDICTED_PRICES.observe(price)
    INPUT_PRICES.observe(features["Present_Price"])
    return {"item_id": item_id, "predict": price}
