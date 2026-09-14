import os
import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME

_telemetry_initialized = False

def setup_telemetry(service_name: str = None):
    global _telemetry_initialized
    if _telemetry_initialized:
        return

    svc_name = service_name or os.getenv("OTEL_SERVICE_NAME", "ai_ecosystem_backend")
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

    resource = Resource.create({SERVICE_NAME: svc_name})

    # 1. Tracing Setup
    trace_provider = TracerProvider(resource=resource)
    trace_exporter = OTLPSpanExporter(endpoint=f"{otlp_endpoint}/v1/traces")
    trace_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(trace_provider)

    # 2. Metrics Setup
    metric_exporter = OTLPMetricExporter(endpoint=f"{otlp_endpoint}/v1/metrics")
    reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=5000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    _telemetry_initialized = True
    logging.info(f"OpenTelemetry initialized for service '{svc_name}' -> OTLP endpoint: {otlp_endpoint}")

def get_tracer(name: str = "ai_ecosystem"):
    return trace.get_tracer(name)

def get_meter(name: str = "ai_ecosystem"):
    return metrics.get_meter(name)
