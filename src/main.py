from fastapi import FastAPI
from routes import base,data,nlp
from helpers.config import get_settings
from stores import LLMProviderFactory
from stores.vectordb.VectorDBProvidersFactory import VectorDBProvidersFactory
from stores.llm.templetes.templete_parser import TemplateParser

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()


@app.on_event("startup")
async def startup_span():
    settings = get_settings()
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"

    app.db_engine = create_async_engine(postgres_conn)
    app.db_client = sessionmaker(
        app.db_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    llm_provider_factory = LLMProviderFactory(settings)
    Vector_DB_Providers_Factory = VectorDBProvidersFactory(settings,
                                                           db_client= app.db_client )
    #generation client
    app.generation_client = llm_provider_factory.create(provider_name=settings.GENERATION_BACKEND)
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODLE_ID)

    #embedding client
    app.embedding_client = llm_provider_factory.create(provider_name=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODLE_ID,embedding_size=settings.EMBEDDING_MODLE_SIZE)

    #vector db client
    app.vector_db_client = Vector_DB_Providers_Factory.create(provider_name=settings.VECTOR_DB_BACKEND)
    await app.vector_db_client.connect()
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANGUAGE,
        default_language=settings.DEFAULT_LANGUAGE,
    )

@app.on_event("shutdown")
async def shutdown_span():
    await app.db_engine.dispose()
    await app.vector_db_client.disconnect()


app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)

