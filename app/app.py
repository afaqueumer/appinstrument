from fastapi import FastAPI

from prometheus_client import start_http_server

from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider

# from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from hello import get_hello_message
from greet import get_greet_message

app = FastAPI()

# Start Prometheus client
start_http_server(port=8001, addr="localhost")
# Exporter to export metrics to Prometheus
prefix = "MyAppPrefix"
reader = PrometheusMetricReader(prefix)
# Meter is responsible for creating and recording metrics
set_meter_provider(MeterProvider(metric_readers=[reader]))
meter = get_meter_provider().get_meter("view-name-change", "0.1.2")

@app.get("/hello")
def read_hello():
    return get_hello_message()


@app.get("/greet")
def read_greet():
    return get_greet_message()


# FastAPIInstrumentor.instrument_app(app)
