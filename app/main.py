from fastapi import FastAPI
from app import models
from app.db import engine
from app.routes import router
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Globant Challenge",
)

app.include_router(router)
