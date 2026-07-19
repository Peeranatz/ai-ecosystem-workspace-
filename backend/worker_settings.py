from arq.connections import RedisSettings
from core.config import settings

async def simple_work(ctx, data):
    print(f"Received job data: {data}")
    return {"status": "done", "data": data}

class WorkerSettings:
    functions = [simple_work]
    redis_settings = RedisSettings(host=settings.redis_host, port=settings.redis_port)
