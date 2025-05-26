# Local OpenTelemetry Collector + Jaeger Setup

This directory contains a `docker-compose.yml` and `otel-collector-config.yaml` to quickly spin up a local OpenTelemetry (OTEL) Collector and a Jaeger instance for trace visualization.

This setup is ideal for local development and testing of AEP instrumentation.

## What it does:

*   **OTEL Collector (`otel-collector-aep`):**
    *   Receives traces via OTLP (HTTP on port `4318`, gRPC on port `4317`).
    *   Exports traces to Jaeger.
    *   Exports traces, metrics, and logs to its own console logs (for debugging).
*   **Jaeger (`jaeger-aep`):**
    *   Receives traces from the OTEL Collector.
    *   Provides a UI to view traces at [http://localhost:16686](http://localhost:16686).

## How to run:

1.  **Ensure Docker and Docker Compose are installed.**
2.  Navigate to this directory (`examples/collector/`) in your terminal.
3.  Run the services in detached mode:
    ```bash
    docker-compose up -d
    ```

## Configuring your AEP SDK to send data:

To send traces from your AEP-instrumented application (e.g., the Python SDK example) to this local collector, you need to configure the OTLP exporter endpoint. This is typically done via environment variables:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
# For gRPC, you might use:
# export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" 
# export OTEL_EXPORTER_OTLP_PROTOCOL="grpc"

# Then run your application, e.g.:
# python examples/python/minimal_openai.py 
```

If using the `examples/python/minimal_openai.py` script, you can also create/update `examples/python/.env` with:
```
OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
```

**Note:** The default Python SDK `tracing.py` currently uses a `ConsoleSpanExporter`. To send to the OTLP endpoint, you would need to modify `tracing.py` to use an `OTLPSpanExporter` or allow configuration via environment variables (a likely future enhancement for the SDK).

For now, this collector setup is primarily for demonstrating a full pipeline and for SDKs that are configured to export via OTLP.

## Viewing Traces:

*   **Jaeger UI:** Open [http://localhost:16686](http://localhost:16686) in your browser.
    *   Select your service name (e.g., `aep-python-app` or whatever `AEP_SERVICE_NAME` is set to) from the "Service" dropdown.
    *   Click "Find Traces".

## Viewing Collector Logs:

To see the raw telemetry data being processed by the collector (due to the `logging` exporter):

```bash
docker-compose logs otel-collector-aep
```

To follow logs in real-time:
```bash
docker-compose logs -f otel-collector-aep
```

## Stopping the services:

```bash
docker-compose down
``` 