from typing import Dict, Any
from aiogram import BaseMiddleware
from sqlalchemy.ext.asyncio import async_sessionmaker
from aiogram.types import TelegramObject


class DBMiddleware(BaseMiddleware):
    def __init__(self, sessionmarker: async_sessionmaker):
        self.sessionmarker = sessionmarker

    async def __call__(
            self,
            handler,
            event: TelegramObject,
            data: Dict[str, Any]
    ):
        async with self.sessionmarker() as session:
            data['session'] = session
            return await handler(event, data)