import pickle
from typing import Any

from project import EnvironmentConfig, get_logger
from project.cache_db.redis.client import RedisClient

class CacheService:
    def __init__(self):
        self.logger = get_logger()
        self.redis_client = RedisClient.get_client()
        self.cache_expiration = int(EnvironmentConfig.get_string('database.redis.cache_expiration'))
        self.key_prefix = EnvironmentConfig.get_string('database.redis.default_key')

    async def save(self, key:str, data:Any, expire: int = 60):
        self.logger.info(f"Saving key: {key} to Redis")
        if not data:
            self.logger.error(f"No data for key: {key}")
            return
        if not key:
            self.logger.error("No key while saving")
            return
        expiry = expire if expire is not None else self.cache_expiration
        try:
            key = f'{self.key_prefix}_{key}'
            expiry_seconds = expiry*60
            if isinstance(data, int):
                await self.redis_client.set(key, data, ex=expiry_seconds)
            elif isinstance(data, (list, tuple, set, dict)):
                await self.redis_client.set(key, pickle.dumps(data), ex=expiry_seconds)
            else:
                await self.redis_client.set(key, pickle.dumps(data), ex=expiry_seconds)
        except Exception as exception:
            self.logger.error(f"Failed to save key:{key}, with exception: {exception}")

    async def retrieve(self, key:str):
        self.logger.info(f"Retrieving key:{key} from Redis")
        value = await self.redis_client.get(f'{self.key_prefix}_{key}')
        if value:
            return pickle.loads(value)
        else:
            return None

    async def delete_cache(self, key:str):
        self.logger.info(f"Deleting key:{key} from Redis")
        try:
            await self.redis_client.delete(f'{self.key_prefix}_{key}')
        except Exception as exception:
            self.logger.error(f"Failed to delete key {key}: {exception}")
