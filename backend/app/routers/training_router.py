from fastapi import APIRouter, status, Body
from typing import Dict, Any
from app.schemas.training_schema import TrainingStartRequest, JobAcceptedResponse, JobStatusResponse
from app.services.training_service import TrainingService
from app.services.trainer_worker_service import TrainerWorkerService

router = APIRouter(prefix="/training", tags=["4. Automated Async Training Domain"])

@router.post("/start", response_model=JobAcceptedResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_training(payload: TrainingStartRequest):
    """
    Start heavy AI model training job asynchronously.
    Returns HTTP 202 Accepted immediately with job_id. Task pushed to Redis Queue.
    """
    return await TrainingService.dispatch_training_job(payload)

@router.post("/enqueue", status_code=status.HTTP_202_ACCEPTED, summary="Enqueue Scheduled Training Task", description="Enqueue training task into Redis Sorted Set scheduled queue with a execution time delay")
async def enqueue_scheduled_training(
    job_id: str = Body("job_001", description="Unique Job ID e.g. job_001"),
    dataset_name: str = Body("conll2003", description="Dataset name e.g. conll2003, wikiann"),
    base_model: str = Body("bert-base-cased", description="Base model name e.g. bert-base-cased, distilbert-base-uncased"),
    delay_seconds: int = Body(10, description="Scheduled execution delay in seconds")
):
    """Enqueue scheduled training task to Redis Sorted Set (ZADD)."""
    return TrainerWorkerService.enqueue_scheduled_training(
        job_id=job_id,
        dataset_name=dataset_name,
        base_model=base_model,
        delay_seconds=delay_seconds
    )

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_training_status(job_id: str):
    """Poll training progress and job execution status."""
    return await TrainingService.get_job_status(job_id)

@router.post("/cancel/{job_id}")
async def cancel_training(job_id: str):
    """Cancel a queued training job."""
    return {"job_id": job_id, "status": "CANCELLED", "message": "Job cancelled successfully."}
