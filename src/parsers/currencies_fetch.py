import asyncio
import logging
import urllib.parse
from typing import List

from pydantic import ValidationError

from src.models import ForexResponse
from src.config import ACCESS_KEY, BASE_API_URL
from src.utils import get_request, AiohttpClient


async def get_historical_currency_data(
    dates: List,
    base_currency: str,
    symbols: List[str]
):
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
        return {"Error": e}
