from contextlib import asynccontextmanager
from typing import AsyncGenerator


from fastapi import FastAPI

from project import get_logger

class App(FastAPI):
    def __init__(self):
        self.logger = get_logger()
        super().__init__(lifespan=self.lifespan)

    @asynccontextmanager
    async def lifespan(self, app: FastAPI)-> AsyncGenerator[None, None]:
        self.logger.info("Starting app")
        self.on_start()
        yield

    def on_start(self):
        pass

    def handle_docs(self):
        pass