<<<<<<< HEAD
from fastapi import FastAPI
from routes import base
from routes import data

app=FastAPI()
app.include_router(base.base_router)
app.include_router(data.data_router)
=======
from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv (".env")
from src import base
app=FastAPI()
app.include_router(base.base_router)
>>>>>>> 4ecfb2c7aab09975915c463532460ed9f3f1cbb9
