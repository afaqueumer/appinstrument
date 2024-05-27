from fastapi import FastAPI
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from starlette_exporter import PrometheusMiddleware, handle_metrics
from starlette_exporter.optional_metrics import response_body_size
from starlette_exporter.optional_metrics import request_body_size

from hello import get_hello_message
from greet import get_greet_message
from tokens import get_token_count

app = FastAPI()

app.add_middleware(PrometheusMiddleware,
                   app_name="myfastapp",
                   prefix='myapp',
                   optional_metrics=[response_body_size, request_body_size],)
app.add_route("/metrics", handle_metrics)


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


@app.post("/count_tokens")
def count_token(input: str):
    return get_token_count(input)
