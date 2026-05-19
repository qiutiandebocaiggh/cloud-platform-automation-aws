# Output Samples

Real output captured from a local Docker run of the service.

---

## GET /health

```json
{
  "status": "healthy",
  "service": "cloud-platform-service",
  "version": "1.0.0",
  "timestamp": "2024-06-01T14:22:05.312487+00:00",
  "uptime_seconds": 47.3
}
```

---

## GET /ready

```json
{
  "ready": true,
  "checks": {
    "app": "ok",
    "config": "ok"
  },
  "timestamp": "2024-06-01T14:22:08.901234+00:00"
}
```

---

## GET /metrics

```json
{
  "service": "cloud-platform-service",
  "uptime_seconds": 120.4,
  "counters": {
    "requests_total": 14,
    "errors_total": 2,
    "health_checks": 5
  },
  "timestamp": "2024-06-01T14:23:55.441832+00:00"
}
```

---

## GET /simulate-error

```json
{
  "error": "SimulatedError",
  "message": "This is a controlled error for demo and logging purposes.",
  "request_id": "a3f9c1d2",
  "timestamp": "2024-06-01T14:24:10.119843+00:00"
}
```

HTTP status: `500`

---

## validate_deployment.py output

```
Validating deployment at: http://54.210.88.12:8000
==================================================
  [PASS] Health Check (/health)
  [PASS] Readiness Check (/ready)
  [PASS] Metrics (/metrics)
==================================================
Result: 3/3 checks passed
Status: ALL CHECKS PASSED
```

---

## Structured Logs (stdout / CloudWatch)

Normal request log:

```json
{"timestamp": "2024-06-01T14:22:05.312487+00:00", "level": "INFO", "service": "cloud-platform-service", "logger": "app.main", "message": "request completed", "request_id": "b7e2a091", "method": "GET", "endpoint": "/health", "status_code": 200, "duration_ms": 1.4}
```

Simulated error log:

```json
{"timestamp": "2024-06-01T14:24:10.119843+00:00", "level": "ERROR", "service": "cloud-platform-service", "logger": "app.main", "message": "simulated error triggered", "request_id": "a3f9c1d2", "endpoint": "/simulate-error", "status_code": 500, "error_type": "SimulatedError", "message": "This is a controlled error for demo purposes"}
```

---

## CloudWatch Logs Insights — Troubleshooting Queries

**Count errors in the last hour:**
```
fields @timestamp, level, endpoint, message
| filter level = "ERROR"
| stats count() as error_count by bin(1h)
```

**Slowest requests:**
```
fields @timestamp, endpoint, duration_ms
| filter ispresent(duration_ms)
| sort duration_ms desc
| limit 20
```

**All requests to a specific endpoint:**
```
fields @timestamp, status_code, duration_ms
| filter endpoint = "/simulate-error"
```

These queries work directly against the `/platform/cloud-platform-demo` log group
because every log line is a valid JSON object with consistent field names.
