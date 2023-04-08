from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from .core.config import settings
from .api.api import router as api_router
app = FastAPI()

DB_URL = f"mongodb://{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}"

ALLOWED_HOSTS = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[settings.DATABASE_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

@app.get('/')
async def root():
    return {'message': 'Welcome to BlogApp'}

app.include_router(api_router)