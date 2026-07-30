from sqlalchemy import Column, Integer, String, DateTime
from app.models.user_model import Base
from datetime import datetime, timezone

class DatasetMetadata(Base):
    __tablename__ = "dataset_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    minio_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
