from pydantic import BaseModel
from typing import Dict, Any

class HealthCheckResponse(BaseModel):
    status: str
    postgres: str
    minio: str
    redis: str
    details: Dict[str, Any]

class PredictionRequest(BaseModel):
    input_data: Any

class PredictionResponse(BaseModel):
    model_version: str
    predictions: Any
    confidence_score: float
