from fastapi import FastAPI
from app import models
from app.db import engine
from app.routes import router

# Crear las tablas en la base de datos si no existen
models.Base.metadata.create_all(bind=engine)

# Instancia de la aplicación FastAPI
app = FastAPI(
    title="Globant Data Engineering Challenge",
    version="1.0.0"
)

# Registrar rutas
app.include_router(router)
