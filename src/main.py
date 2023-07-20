from fastapi import FastAPI
from src.utils import AiohttpClient
from src.views.dashboards import router as dash_router
from src.views.base import router as base_router

app = FastAPI()
app.include_router(router=base_router)
app.include_router(router=dash_router)


@app.on_event("startup")
async def startup():
    AiohttpClient.get_aiohttp_session()


@app.on_event("shutdown")
async def shutdown():
    await AiohttpClient.close_aiohttp_client()
