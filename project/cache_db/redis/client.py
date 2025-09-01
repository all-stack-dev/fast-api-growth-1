import redis.asyncio as redis

from project import get_logger, EnvironmentConfig


class RedisClient:
    _redis_client = None

    @classmethod
    def setup_logger(cls):
        return get_logger()

    @classmethod
    def get_env_details(cls):
        logger = cls.setup_logger()
        redis_enabled = EnvironmentConfig.get_boolean('database.redis.enabled')
        host = EnvironmentConfig.get_string('database.redis.host')
        port = int(EnvironmentConfig.get_string('database.redis.port'))
        if redis_enabled:
            if not host:
                logger.error("Cannot connect redis server without host")
                exit(1)
            if not port:
                logger.error("Cannot connect redis server without port")
                exit(1)
            return redis_enabled, host, port
        else:
            return False, None, None

    @classmethod
    async def initialize_redis(cls):
        logger = cls.setup_logger()
        if cls._redis_client is None:
            redis_enabled, host, port = cls.get_env_details()
            if redis_enabled:
                try:
                    connection_pool = redis.ConnectionPool(host=host, port=port, db=0)
                    cls._redis_client = redis.Redis(connection_pool=connection_pool)
                    await cls._redis_client.ping()
                except Exception as exception:
                    logger.error(f"Cannot connect to redis server: {exception}")
                    exit(1)

    @classmethod
    def get_client(cls):
        logger = cls.setup_logger()
        if cls._redis_client is None:
            logger.info("Redis client is not initialized")
            raise ConnectionError("Redis client is not initialized")
        return cls._redis_client



