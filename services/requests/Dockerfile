FROM python:3.11-slim

WORKDIR /requests_service
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requests.py .

CMD ["python", "requests.py"]

# Build from services/requests.
# docker build -t car_price_requests:2 .
# Run after starting the Compose prediction service.
# docker run --rm --network lab4_car_price_default car_price_requests:2
