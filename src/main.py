from fastapi import FastAPI
from routes import base,data,nlp
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

from stores import LLMProviderFactory
from stores.llm.LLMEnums import LLMEnums

from stores.vectordb import VectorDBEnums
from stores.vectordb.VectorDBProvidersFactory import VectorDBProvidersFactory
app = FastAPI()


@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongo_db = app.mongo_conn[settings.MONGODB_DB]
    
    llm_provider_factory = LLMProviderFactory(settings)
    Vector_DB_Providers_Factory = VectorDBProvidersFactory(settings)
    #generation client
    app.generation_client = llm_provider_factory.create(provider_name=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODLE_ID)

    #embedding client
    app.embedding_client = llm_provider_factory.create(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODLE_ID,embedding_size=settings.EMBEDDING_MODLE_SIZE)

    #vector db client
    app.vector_db_client = Vector_DB_Providers_Factory.create(provider_name=settings.VECTOR_DB_BACKEND)
    app.vector_db_client.connect()

@app.on_event("shutdown")
async def shutdown_span():
    app.mongo_conn.close()
    app.vector_db_client.disconnect()


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

