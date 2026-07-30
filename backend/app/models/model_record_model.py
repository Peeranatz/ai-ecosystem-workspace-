from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.models.user_model import Base
from datetime import datetime, timezone

class ModelRecord(Base):
    __tablename__ = "model_record"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)  # e.g., v1.0.0 (Append-Only Log)
    minio_path = Column(String, nullable=False)
    metrics = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
