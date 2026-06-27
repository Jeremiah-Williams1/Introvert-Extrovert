FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your model files and the worker
COPY ./worker .

CMD ["python", "worker.py"]