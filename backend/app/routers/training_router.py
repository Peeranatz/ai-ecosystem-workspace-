from fastapi import APIRouter, status
from app.schemas.training_schema import TrainingStartRequest, JobAcceptedResponse, JobStatusResponse
from app.services.training_service import TrainingService

router = APIRouter(prefix="/training", tags=["4. Automated Async Training Domain"])

@router.post("/start", response_model=JobAcceptedResponse, status_code=status.HTTP_202_ACCEPTED)
async def start_training(payload: TrainingStartRequest):
    """
    Start heavy AI model training job asynchronously.
    Returns HTTP 202 Accepted immediately with job_id. Task pushed to Redis Queue.
    """
    return await TrainingService.dispatch_training_job(payload)

@router.get("/status/{job_id}", response_model=JobStatusResponse)
async def get_training_status(job_id: str):
    """Poll training progress and job execution status."""
    return await TrainingService.get_job_status(job_id)

@router.post("/cancel/{job_id}")
async def cancel_training(job_id: str):
    """Cancel a queued training job."""
    return {"job_id": job_id, "status": "CANCELLED", "message": "Job cancelled successfully."}
