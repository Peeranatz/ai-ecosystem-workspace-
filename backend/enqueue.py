import asyncio
from arq import create_pool
from arq.connections import RedisSettings
from core.config import settings

async def main():
    redis = await create_pool(RedisSettings(host=settings.redis_host, port=settings.redis_port))
    await redis.enqueue_job("simple_work", {"msg": "hello from sky"})
    print("Job enqueued!")

if __name__ == "__main__":
    asyncio.run(main())
