from pydantic import BaseModel
from datetime import datetime

class DatasetMetadataResponse(BaseModel):
    id: int
    filename: str
    file_size_bytes: int
    minio_path: str
    created_at: datetime

    class Config:
        from_attributes = True
