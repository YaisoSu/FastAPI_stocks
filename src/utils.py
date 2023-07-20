from typing import Optional, Dict

import aiohttp


class AiohttpClient:
    session: Optional[aiohttp.ClientSession] = None

    @classmethod
    def get_aiohttp_session(cls) -> aiohttp.ClientSession:
        if cls.session is None:
            cls.session = aiohttp.ClientSession()

        return cls.session

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.session:
            await cls.session.close()
            cls.session = None

    @classmethod
    def __call__(cls) -> aiohttp.ClientSession:
        assert cls.session is not None
        return cls.session


async def get_request(session: aiohttp.ClientSession, url: str, params: Dict):
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return await response.json()
        else:
            return {"status": response.status, "reason": response.text}
