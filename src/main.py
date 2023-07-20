from fastapi import FastAPI
from src.utils import AiohttpClient
from src.views.dashboards import router

app = FastAPI()
app.include_router(router=router)


@app.on_event("startup")
async def startup():
    AiohttpClient.get_aiohttp_session()


@app.on_event("shutdown")
async def shutdown():
    await AiohttpClient.close_aiohttp_client()
