from typing import List
from datetime import datetime, timezone
from app.schemas.dataset_schema import DatasetMetadataResponse
from app.utils.logger import logger

class DatasetService:
    @staticmethod
    async def upload_dataset(filename: str, file_bytes: bytes) -> DatasetMetadataResponse:
        logger.info(f"Dataset upload initiated: {filename} ({len(file_bytes)} bytes)")
        # Separation of Storage Logic:
        # 1. Stream file_bytes to MinIO bucket 'raw-datasets'
        # 2. Save metadata (filename, file_size_bytes, minio_path) to PostgreSQL
        minio_path = f"raw-datasets/{filename}"
        return DatasetMetadataResponse(
            id=101,
            filename=filename,
            file_size_bytes=len(file_bytes),
            minio_path=minio_path,
            created_at=datetime.now(timezone.utc)
        )

    @staticmethod
    async def list_datasets(skip: int = 0, limit: int = 10) -> List[DatasetMetadataResponse]:
        logger.info(f"Listing datasets with pagination skip={skip}, limit={limit}")
        return [
            DatasetMetadataResponse(
                id=1,
                filename="sample_training_data.csv",
                file_size_bytes=2048500,
                minio_path="raw-datasets/sample_training_data.csv",
                created_at=datetime.now(timezone.utc)
            )
        ]
