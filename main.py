## main.py
from fastapi import FastAPI
from api.endpoints import router

app = FastAPI(title="Financial File Format Converter API")

app.include_router(router, prefix="/api")

 # Stops all uvicorn instances