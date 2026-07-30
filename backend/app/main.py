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
    system_router
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Enterprise Clean Architecture Web API for AI Ecosystem (FastAPI + PostgreSQL + MinIO + Redis)",
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

# Register Domain Routers
app.include_router(auth_router.router, prefix=settings.API_V1_STR)
app.include_router(dataset_router.router, prefix=settings.API_V1_STR)
app.include_router(model_router.router, prefix=settings.API_V1_STR)
app.include_router(training_router.router, prefix=settings.API_V1_STR)
app.include_router(predict_router.router, prefix=settings.API_V1_STR)
app.include_router(system_router.router, prefix=settings.API_V1_STR)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to AI Ecosystem FastAPI Backend",
        "docs": "/docs",
        "health_check": "/api/v1/system/health"
    }
