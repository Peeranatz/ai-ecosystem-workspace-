from pydantic import BaseModel
from typing import Optional, Dict, Any

class TrainingStartRequest(BaseModel):
    model_name: str
    dataset_id: int
    epochs: int = 10
    hyperparameters: Optional[Dict[str, Any]] = None

class JobAcceptedResponse(BaseModel):
    job_id: str
    status: str = "PENDING"
    message: str = "Training job submitted to Redis queue successfully."

class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # PENDING, RUNNING, COMPLETED, FAILED
    progress_percentage: float = 0.0
    result_model_version: Optional[str] = None
