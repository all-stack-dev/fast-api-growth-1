from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

from project import get_logger, EnvironmentConfig


class NoSQLClient:
    _mongo_client = None
    _database = None

    @classmethod
    def setup_logger(cls):
        return get_logger()

    @classmethod
    def get_env_details(cls):
        logger = cls.setup_logger()
        url =  EnvironmentConfig.get_string('database.mongodb.url')
        database_name = EnvironmentConfig.get_string('database.mongodb.database_name')
        if not url:
            logger.error("Cannot connect to database with the url")
            exit(1)
        if not database_name:
            logger.error("Cannot connect to database with the given database name")
            exit(1)
        return url, database_name

    @classmethod
    async def initialize_database(cls):
        logger = cls.setup_logger()
        if cls._mongo_client is None:
            url, database_name = cls.get_env_details()
            try:
                cls._mongo_client = AsyncIOMotorClient(url, server_api=ServerApi('1'))
                cls._database = cls._mongo_client[database_name]
                logger.info("Successfully connected to database")
            except Exception as exception:
                logger.error(f"Failed to connect to database. Exception: {exception}")
                exit(1)

    @classmethod
    def get_client(cls):
        logger = cls.setup_logger()
        if cls._database is None:
            logger.error("Cannot connect to database with the given database name")
            raise ConnectionError("Cannot connect to database with the given database name")
        return cls._database

    @classmethod
    def get_collection(cls, collection_name):
        database = cls.get_client()
        return database[collection_name]