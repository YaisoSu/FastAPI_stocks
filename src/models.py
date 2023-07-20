from pydantic import BaseModel


class ForexResponse(BaseModel):
    success: bool
    timestamp: int
    historical: bool
    base: str
    date: str
    rates: dict
