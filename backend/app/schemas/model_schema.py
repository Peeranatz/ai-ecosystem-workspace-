from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class ModelRecordResponse(BaseModel):
    id: int
    model_name: str
    version: str
    minio_path: str
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime

    class Config:
        from_attributes = True
