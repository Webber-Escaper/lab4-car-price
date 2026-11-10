FROM python:3.11-slim

WORKDIR /ml_service
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py api_handler.py ./
COPY static ./static
VOLUME /models
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Build from services/ml_service. Version 3 follows the existing version 2.
# docker build -t car_price_prediction:3 .
# docker run --rm -p 127.0.0.1:8004:8000 -v "$(pwd)/../models:/models:ro" car_price_prediction:3
