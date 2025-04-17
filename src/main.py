from fastapi import FastAPI
from routes import base
from routes import data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

from stores import LLMProviderFactory
from stores.llm.LLMEnums import LLMEnums

app = FastAPI()


@app.on_event("startup")
async def startup_db_clint():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongo_db = app.mongo_conn[settings.MONGODB_DB]
    
    llm_provider_factory = LLMProviderFactory(settings)

    #generation client
    app.generation_client = llm_provider_factory.create(provider_name=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODLE_ID)

    #embedding client
    app.embedding_client = llm_provider_factory.create(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODLE_ID,embedding_size=settings.EMBEDDING_SIZE)

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongo_conn.close()


app.include_router(base.base_router)
app.include_router(data.data_router)
