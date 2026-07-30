from fastapi import APIRouter
from app.schemas.system_schema import PredictionRequest, PredictionResponse
from app.services.inference_service import InferenceService

router = APIRouter(prefix="/predict", tags=["5. Inference Domain"])

@router.post("", response_model=PredictionResponse)
async def predict_inference(payload: PredictionRequest):
    """Execute low-latency AI inference prediction."""
    return await InferenceService.predict(payload)
