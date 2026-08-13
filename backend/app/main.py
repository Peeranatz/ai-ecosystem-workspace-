from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import settings
from app.utils.logger import logger
from app.routers import (
    auth_router,
    dataset_router,
    model_router,
    training_router,
    predict_router,
    system_router,
    label_studio_router
)

# Detailed Tag Metadata for OpenAPI & Swagger UI
tags_metadata = [
    {
        "name": "1. Authentication & Security Domain",
        "description": "Stateless JWT Authentication, Password Hashing with Bcrypt, and Protected Profile Routes (`/api/v1/auth`)."
    },
    {
        "name": "2. Dataset Management Domain",
        "description": "Separation of Storage: Raw dataset upload to MinIO S3 Object Storage (`raw-datasets`) and Metadata indexing in PostgreSQL 17."
    },
    {
        "name": "3. Model Registry Domain",
        "description": "Append-Only Immutability Policy: Model versioning (`v1.0.0`, `v1.1.0`), Audit Trail, and Rollback to latest stable weights."
    },
    {
        "name": "4. Automated Async Training Domain",
        "description": "Asynchronous Task Queue Pattern: Returns `HTTP 202 Accepted` immediately with `job_id`, pushing task to Redis Queue for Background Workers."
    },
    {
        "name": "5. Inference Domain",
        "description": "Low-Latency Prediction Channel: Loads PyTorch weights from MinIO/RAM cache for real-time model predictions."
    },
    {
        "name": "6. Label Studio Component Domain",
        "description": "Data Annotation SDK Integration: Create projects, import raw dataset tasks, and export labeled annotations (`/api/v1/ls`)."
    },
    {
        "name": "7. System Monitoring & Health Domain",
        "description": "Observability & Container Health Checks: PING verification for PostgreSQL, MinIO, Redis (`/system/health`) and Structured JSON Logging (`/system/logs`)."
    }
]

app = FastAPI(
    title="AI Ecosystem Enterprise Web API",
    version="1.0.0",
    description="""
# 🚀 AI Ecosystem Enterprise Web API Platform

Enterprise Clean Architecture Web API for managing the complete MLOps AI Lifecycle:
* **Architecture Style**: Clean Layered Architecture (`routers/`, `schemas/`, `services/`, `models/`, `core/`, `utils/`)
* **Storage Isolation**: PostgreSQL 17 (Relational Metadata) + MinIO (S3 Object Storage) + Redis 6379 (In-Memory Queue)
* **Async Processing**: Non-blocking `HTTP 202 Accepted` Task Queue with Time-Series & Non-Time-Series Workers
* **Observability**: Machine-Readable Structured JSON Logging & Docker Health Monitoring
""",
    terms_of_service="https://github.com/Peeranatz/ai-ecosystem-workspace-",
    contact={
        "name": "AI Ecosystem Development Team (Sky & Kim)",
        "url": "https://github.com/Peeranatz/ai-ecosystem-workspace-",
        "email": "peeranat.j@aiecosystem.io"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=tags_metadata,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Structured JSON Middleware Logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    
    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - {process_time:.2f}ms",
        extra={
            "extra_data": {
                "http_method": request.method,
                "endpoint": request.url.path,
                "status_code": response.status_code,
                "execution_time_ms": round(process_time, 2),
                "client_ip": request.client.host if request.client else "unknown"
            }
        }
    )
    return response

# Register All Domain Routers
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(dataset_router.router, prefix=settings.API_V1_STR)
app.include_router(model_router.router, prefix=settings.API_V1_STR)
app.include_router(training_router.router, prefix=settings.API_V1_STR)
app.include_router(predict_router.router, prefix=settings.API_V1_STR)
app.include_router(label_studio_router.router, prefix=settings.API_V1_STR)
app.include_router(system_router.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["7. System Monitoring & Health Domain"], summary="Root Health Status")
async def root():
    return {
        "message": "Welcome to AI Ecosystem Enterprise Web API Platform",
        "docs_swagger": "/docs",
        "docs_redoc": "/redoc",
        "openapi_json": f"{settings.API_V1_STR}/openapi.json",
        "health_check": f"{settings.API_V1_STR}/system/health"
    }
