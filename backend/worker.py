import sys
import os
import time
import json
import redis

# Ensure backend directory is in sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import settings
from app.utils.logger import logger
from app.services.trainer_worker_service import TrainerWorkerService, SCHEDULED_QUEUE_NAME

def run_worker_loop():
    logger.info("==========================================================")
    logger.info("🚀 AI Ecosystem Trainer Worker Started (GPU/CPU PyTorch Runtime)")
    logger.info(f"Connecting to Redis Scheduled Queue: {settings.REDIS_HOST}:{settings.REDIS_PORT}")
    logger.info("==========================================================")
    
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

    while True:
        try:
            current_time = int(time.time())
            
            # Fetch ready jobs from Redis Sorted Set where score <= current_timestamp
            ready_jobs = redis_client.zrangebyscore(SCHEDULED_QUEUE_NAME, min=0, max=current_time)
            
            if ready_jobs:
                for job_raw in ready_jobs:
                    # Remove job from Redis Sorted Set to claim execution lock
                    removed_count = redis_client.zrem(SCHEDULED_QUEUE_NAME, job_raw)
                    if removed_count > 0:
                        payload = json.loads(job_raw)
                        logger.info(f"Claimed Scheduled Job '{payload.get('job_id')}' (Scheduled at: {payload.get('scheduled_at')})")
                        
                        # Execute Trainer Worker Task
                        result = TrainerWorkerService.execute_training_job(payload)
                        logger.info(f"Job '{payload.get('job_id')}' completed successfully: {result['status']}")
            
            time.sleep(2) # Poll queue every 2 seconds
        except Exception as err:
            logger.error(f"Trainer Worker Loop Exception: {err}")
            time.sleep(5)

if __name__ == "__main__":
    run_worker_loop()
