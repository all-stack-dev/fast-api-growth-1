from contextlib import asynccontextmanager
from typing import AsyncGenerator


from fastapi import FastAPI

from project import get_logger, NoSQLClient

class App(FastAPI):
    def __init__(self):
        self.logger = get_logger()
        super().__init__(lifespan=self.lifespan)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI)-> AsyncGenerator[None, None]:
        self.logger.info("Starting app")
        await self.on_start()
        yield

    async def on_start(self):
        await NoSQLClient.initialize_database()
        self.logger.info("Initialized Database")

    def handle_docs(self):
        pass