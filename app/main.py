"""
Cloud Platform Automation - Python Service
Demonstrates health checks, structured logging, and operational endpoints.
"""

import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.logging_config import get_logger

app = FastAPI(title="cloud-platform-service", version="1.0.0")
logger = get_logger(__name__)

# Simple in-memory counters (no database required)
counters = {
    "requests_total": 0,
    "errors_total": 0,
    "health_checks": 0,
}

START_TIME = time.time()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log every request with structured fields."""
    request_id = str(uuid.uuid4())[:8]
    start = time.time()

    response = await call_next(request)

    duration_ms = round((time.time() - start) * 1000, 2)
    counters["requests_total"] += 1

    logger.info(
        "request completed",
        extra={
            "request_id": request_id,
            "method": request.method,
            "endpoint": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.get("/health")
async def health():
    """Liveness probe — confirms the service is running."""
    counters["health_checks"] += 1
    return {
        "status": "healthy",
        "service": "cloud-platform-service",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": round(time.time() - START_TIME, 1),
    }


@app.get("/ready")
async def ready():
    """Readiness probe — confirms the service is ready to serve traffic."""
    return {
        "ready": True,
        "checks": {
            "app": "ok",
            "config": "ok",
        },
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/metrics")
async def metrics():
    """Operational counters for lightweight observability."""
    return {
        "service": "cloud-platform-service",
        "uptime_seconds": round(time.time() - START_TIME, 1),
        "counters": counters,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/simulate-error")
async def simulate_error():
    """Intentional error endpoint to demonstrate structured error logging."""
    counters["errors_total"] += 1
    request_id = str(uuid.uuid4())[:8]

    logger.error(
        "simulated error triggered",
        extra={
            "request_id": request_id,
            "endpoint": "/simulate-error",
            "status_code": 500,
            "error_type": "SimulatedError",
            "message": "This is a controlled error for demo purposes",
        },
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "SimulatedError",
            "message": "This is a controlled error for demo and logging purposes.",
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )
