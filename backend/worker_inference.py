import time
import json
import redis

from app.core.config import settings
from app.utils.logger import logger
from app.core.telemetry import setup_telemetry
from app.services.inference_worker_service import InferenceWorkerService, INFERENCE_QUEUE_NAME

def main():
    setup_telemetry("ai_inference_worker")
    logger.info("==================================================")

    logger.info("🚀 AI Ecosystem Inference Worker Started")
    logger.info(f"Connecting to Redis Queue '{INFERENCE_QUEUE_NAME}' on {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info("==================================================")
    
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    while True:
        try:
            # BLPOP blocks until an item is available in Redis list (timeout=2 seconds)
            pop_result = redis_client.blpop(INFERENCE_QUEUE_NAME, timeout=2)
            if pop_result:
                queue_name, item_data = pop_result
                InferenceWorkerService.process_queue_item(item_data)
            else:
                time.sleep(0.5)
        except KeyboardInterrupt:
            logger.info("Inference Worker stopping...")
            break
        except Exception as e:
            logger.error(f"Error in Inference Worker loop: {str(e)}")
            time.sleep(2)

if __name__ == "__main__":
    main()
