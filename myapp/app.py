from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

# --- OpenTelemetry Imports ---
from opentelemetry import metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


# 1. Initialize OTel Metrics BEFORE the app
# Use 'otel-collector' because that is the name of your container in the docker network
resource = Resource.create({"service.name": "hello-world-api"})
exporter = OTLPMetricExporter(endpoint="http://otel-collector:4317", insecure=True)
reader = PeriodicExportingMetricReader(
    exporter, export_interval_millis=30000
)  # Export every 30s
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

app = FastAPI(title="Hello World API", version="1.0.0")

# 2. Attach the Instrumentor
# This captures http_server_duration, requests_total, etc.
FastAPIInstrumentor.instrument_app(app)


class HelloResponse(BaseModel):
    message: str
    status: str


@app.get("/", response_class=HTMLResponse)
async def hello_world():
    """Main route that returns Hello World"""
    return "<h1>Hello, World!</h1>"


@app.get("/api/hello", response_model=HelloResponse)
async def hello_api():
    """API endpoint that returns JSON"""
    return HelloResponse(message="Hello, World!", status="success")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
