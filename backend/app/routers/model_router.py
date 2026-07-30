from fastapi import APIRouter, UploadFile, File, Form, status
from typing import List
from app.schemas.model_schema import ModelRecordResponse
from app.services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["3. Model Registry Domain"])

@router.post("/upload", response_model=ModelRecordResponse, status_code=status.HTTP_201_CREATED)
async def upload_model(
    model_name: str = Form(...),
    version: str = Form(...),
    file: UploadFile = File(...)
):
    """Register a new model version (Append-Only Immutability Policy)."""
    contents = await file.read()
    return await ModelService.upload_and_register_model(model_name, version, contents)

@router.get("", response_model=List[ModelRecordResponse])
async def list_models(model_name: str = "image_classifier"):
    """Get audit history of all model versions."""
    return await ModelService.list_model_history(model_name)

@router.get("/latest", response_model=ModelRecordResponse)
async def get_latest_model(model_name: str = "image_classifier"):
    """Get latest stable model version for inference."""
    return await ModelService.get_latest_model(model_name)

@router.get("/{model_id}", response_model=ModelRecordResponse)
async def get_model_by_id(model_id: int):
    """Get specific model record by ID."""
    return await ModelService.get_latest_model()
