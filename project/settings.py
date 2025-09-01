from contextlib import asynccontextmanager
from typing import AsyncGenerator


from fastapi import FastAPI

from project import get_logger, NoSQLClient, RedisClient, StorageClient


class App(FastAPI):
    def __init__(self):
        self.logger = get_logger()
        super().__init__(lifespan=self.lifespan)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI) -> AsyncGenerator[None, None]:
        self.logger.info("Starting app")
        await self.on_start()
        yield

    async def on_start(self):
        await NoSQLClient.initialize_database()
        self.logger.info("Initialized Mongodb Database")
        await RedisClient.initialize_redis()
        self.logger.info("Initialized Redis Database")
        await StorageClient.initialize_storage_client()
        self.logger.info("Initialized Storage Client")

    def handle_docs(self):
        pass
