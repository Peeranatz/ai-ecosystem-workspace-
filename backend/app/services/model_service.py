from typing import List
from datetime import datetime, timezone
from app.schemas.model_schema import ModelRecordResponse
from app.utils.logger import logger

class ModelService:
    @staticmethod
    async def upload_and_register_model(model_name: str, version: str, file_bytes: bytes) -> ModelRecordResponse:
        logger.info(f"Registering new model version: {model_name} ({version})")
        # Immutability Policy: Always INSERT new version row, never UPDATE
        minio_path = f"models/{model_name}/{version}.pt"
        return ModelRecordResponse(
            id=201,
            model_name=model_name,
            version=version,
            minio_path=minio_path,
            metrics={"accuracy": 0.945, "loss": 0.052},
            created_at=datetime.now(timezone.utc)
        )

    @staticmethod
    async def get_latest_model(model_name: str = "image_classifier") -> ModelRecordResponse:
        logger.info(f"Fetching latest active model for: {model_name}")
        return ModelRecordResponse(
            id=202,
            model_name=model_name,
            version="v2.0.0",
            minio_path=f"models/{model_name}/v2_0_0.pt",
            metrics={"accuracy": 0.962, "loss": 0.038},
            created_at=datetime.now(timezone.utc)
        )

    @staticmethod
    async def list_model_history(model_name: str = "image_classifier") -> List[ModelRecordResponse]:
        logger.info(f"Listing audit history for model: {model_name}")
        return [
            ModelRecordResponse(
                id=201,
                model_name=model_name,
                version="v1.0.0",
                minio_path=f"models/{model_name}/v1_0_0.pt",
                metrics={"accuracy": 0.881, "loss": 0.120},
                created_at=datetime.now(timezone.utc)
            ),
            ModelRecordResponse(
                id=202,
                model_name=model_name,
                version="v2.0.0",
                minio_path=f"models/{model_name}/v2_0_0.pt",
                metrics={"accuracy": 0.962, "loss": 0.038},
                created_at=datetime.now(timezone.utc)
            )
        ]
