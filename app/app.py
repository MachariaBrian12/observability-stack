import logging
import time
import random
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# ── Tracing setup (→ Tempo) ──────────────────
resource = Resource.create({"service.name": "my-devops-app"})
provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# ── Logging setup (→ Loki) ───────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("my-devops-app")

LOKI_URL = "http://localhost:3100/loki/api/v1/push"

def send_log_to_loki(message, level="info"):
    payload = {
        "streams": [{
            "stream": {"app": "my-devops-app", "level": level},
            "values": [[str(int(time.time() * 1e9)), message]]
        }]
    }
    try:
        requests.post(LOKI_URL, json=payload, timeout=2)
    except Exception as e:
        print(f"Loki error: {e}")

def process_order(order_id):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)
        send_log_to_loki(f"Processing order {order_id}", "info")
        time.sleep(random.uniform(0.1, 0.5))

        with tracer.start_as_current_span("validate_payment"):
            send_log_to_loki(f"Validating payment for order {order_id}", "info")
            time.sleep(random.uniform(0.05, 0.2))

        with tracer.start_as_current_span("update_inventory"):
            send_log_to_loki(f"Updating inventory for order {order_id}", "info")
            time.sleep(random.uniform(0.05, 0.15))

        send_log_to_loki(f"Order {order_id} completed ✅", "info")
        print(f"✅ Order {order_id} processed")

if __name__ == "__main__":
    print("🚀 App started — sending logs to Loki & traces to Tempo")
    for i in range(1, 11):
        process_order(f"ORD-{i:03d}")
        time.sleep(1)
    print("🏁 Done! Check Grafana Explore for logs and traces")
