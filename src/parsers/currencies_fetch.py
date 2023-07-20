import asyncio
import logging
import urllib.parse
from typing import List, Optional

from fastapi import HTTPException
from pydantic import ValidationError

from src.keys import ACCESS_KEY
from src.models import ForexResponse
from src.config import BASE_API_URL
from src.utils import get_request, AiohttpClient


async def get_historical_currency_data(
    dates: List[str],
    base_currency: str,
    symbols: List[str]
) -> Optional[List[ForexResponse]]:
    params = {
        "access_key": ACCESS_KEY,
        "base": base_currency,
        "symbols": symbols
    }
    tasks = []

    for date in dates:
        current_url = urllib.parse.urljoin(BASE_API_URL, date)
        tasks.append(get_request(AiohttpClient()(), current_url, params))

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    try:
        responses_data = [ForexResponse(**response) for response in responses]
        return responses_data
    except ValidationError as e:
        logging.error(f"The response didn't match the expected format: {e}")
        raise HTTPException(500, detail=f"Error during validation response from API, {e}")
