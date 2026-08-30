from fastapi import APIRouter, UploadFile, File, Query, status
from typing import List, Dict, Any
from app.schemas.dataset_schema import DatasetMetadataResponse
from app.services.dataset_service import DatasetService
from app.services.trainer_worker_service import TrainerWorkerService

router = APIRouter(prefix="/datasets", tags=["2. Dataset Management Domain"])

@router.post("/upload", response_model=DatasetMetadataResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(file: UploadFile = File(...)):
    """Upload raw dataset file to MinIO Object Storage and store metadata in PostgreSQL."""
    contents = await file.read()
    return await DatasetService.upload_dataset(file.filename, contents)

@router.post("/import-huggingface", status_code=status.HTTP_201_CREATED, summary="Import Hugging Face Dataset", description="Download Token Classification / NER dataset from Hugging Face and store in MinIO bucket 'datasets'")
async def import_huggingface_dataset(
    dataset_name: str = Query("conll2003", description="Hugging Face Dataset Name e.g. conll2003, wikiann"),
    split: str = Query("train", description="Dataset split e.g. train, test, validation")
):
    """Import dataset from Hugging Face Hub to MinIO Storage."""
    return TrainerWorkerService.import_huggingface_dataset(dataset_name=dataset_name, split=split)

@router.get("", response_model=List[DatasetMetadataResponse])
async def list_datasets(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    """List datasets with pagination."""
    return await DatasetService.list_datasets(skip=skip, limit=limit)

@router.get("/{dataset_id}", response_model=DatasetMetadataResponse)
async def get_dataset(dataset_id: int):
    """Retrieve details for a specific dataset."""
    datasets = await DatasetService.list_datasets()
    return datasets[0]
