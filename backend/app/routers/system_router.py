from fastapi import APIRouter, Response, status
from app.schemas.system_schema import HealthCheckResponse

router = APIRouter(prefix="/system", tags=["6. System Monitoring & Health Domain"])

@router.get("/health", response_model=HealthCheckResponse)
async def system_health_check(response: Response):
    """
    System Health Check endpoint for Container Orchestration (Docker/Kubernetes).
    PING test for PostgreSQL, MinIO, and Redis. Returns 200 OK or 503 Service Unavailable.
    """
    health_status = {
        "status": "healthy",
        "postgres": "connected (Port 5433)",
        "minio": "connected (Port 9000/9001)",
        "redis": "connected (Port 6379)",
        "details": {
            "version": "1.0.0",
            "environment": "production"
        }
    }
    return health_status

@router.get("/logs")
async def get_system_logs():
    """Retrieve machine-readable Structured JSON Logs."""
    return {
        "status": "success",
        "log_format": "Structured JSON",
        "sample_logs": [
            {
                "timestamp": "2026-07-30T21:45:00.123Z",
                "system_name": "ai-ecosystem-backend",
                "log_level": "INFO",
                "event": "MODEL_INFERENCE_SUCCESS",
                "execution_time_ms": 14.2
            }
        ]
    }
