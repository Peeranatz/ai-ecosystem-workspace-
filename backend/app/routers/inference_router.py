from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List

from app.services.inference_worker_service import InferenceWorkerService

router = APIRouter(prefix="/inference", tags=["Inference Worker & MLflow"])

class PredictRequest(BaseModel):
    text: str = Field(..., example="Apple Inc. was founded by Steve Jobs in Cupertino, California.")
    model_name: str = Field(default="conll2003_ner", example="conll2003_ner")
    model_version: str = Field(default="latest", example="latest")

@router.post("/predict", summary="Submit text for NER inference prediction")
def enqueue_prediction(request: PredictRequest):
    """
    Submits a text payload for Token Classification / Named Entity Recognition (NER) inference.
    Enqueues prediction task into Redis list queue and returns tracking job_id.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")
    
    return InferenceWorkerService.enqueue_prediction(
        text=request.text,
        model_name=request.model_name,
        model_version=request.model_version
    )

@router.get("/job/{job_id}", summary="Get inference job prediction result")
def get_prediction_job(job_id: str = Path(..., example="inf_job_1788114000000")):
    """
    Queries prediction job status and extracted entities from Redis KV store.
    """
    result = InferenceWorkerService.get_prediction_result(job_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Inference Job ID '{job_id}' not found or expired.")
    return result

@router.get("/models", summary="List registered models in MLflow Server")
def list_registered_models():
    """
    Queries MLflow Tracking Server for registered model names, versions, and stage tags.
    """
    return InferenceWorkerService.list_mlflow_models()
