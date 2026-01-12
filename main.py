from fastapi import FastAPI

from routes.proxy import router

app = FastAPI()

app.include_router(router)
