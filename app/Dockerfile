FROM python:3.11-slim
WORKDIR /app
COPY app.py .
RUN pip install --no-cache-dir \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-http \
    requests
CMD ["python", "app.py"]
