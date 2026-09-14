import sys
from app.utils.logger import logger
from app.services.inference_worker_service import InferenceWorkerService

sys.stdout.reconfigure(encoding='utf-8')

logger.info("==================================================")
logger.info("🚀 AI Ecosystem Inference Worker Started")
logger.info("Connecting to Redis Queue 'inference_job_queue' on localhost:6379")
logger.info("==================================================")

InferenceWorkerService.process_queue_item(
    '{"job_id": "inf_job_1789393676922", "text": "Apple Inc. was founded by Steve Jobs in Cupertino, California.", "model_name": "conll2003_ner", "model_version": "latest"}'
)
