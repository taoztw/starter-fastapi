import sys
import aioredis
from exts import logger
from config import settings


class RedisCli(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisCli, cls).__new__(cls)
        return cls._instance

    def __init__(self, *, url: str, socket_timeout: int = 5):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._redis_client = None
            self.url = url
            self.socket_timeout = socket_timeout

    async def init_redis_connect(self) -> aioredis.Redis:
        try:
            self._redis_client = await aioredis.from_url(
                url=self.url,
                socket_timeout=self.socket_timeout,
                decode_responses=True,
            )
            if not await self._redis_client.ping():
                logger.info("连接redis超时")
                sys.exit()
            logger.info("redis 连接成功")
            return self._redis_client
        except Exception as e:
            logger.error(f"连接redis异常: {e}")
            sys.exit()

    async def get_redis(self) -> aioredis.Redis:
        if self._redis_client is None:
            self._redis_client = await self.init_redis_connect()
        return self._redis_client

    async def close_redis_connect(self) -> None:
        if self._redis_client:
            await self._redis_client.close()


RedisClient = RedisCli(url=settings.REDIS_URL, socket_timeout=settings.REDIS_TIMEOUT)
