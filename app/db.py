from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import os

Base = declarative_base()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "globant_db")
DB_USER = os.getenv("DB_USER", "globant_user")
DB_PASS = os.getenv("DB_PASS", "your_password")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MAX_RETRIES = 10
WAIT_SECONDS = 3

for attempt in range(1, MAX_RETRIES + 1):
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()
        print("✅ Conexión a MySQL exitosa.")
        break
    except Exception as e:
        print(f"⏳ Intento {attempt} de conexión a MySQL fallido. Esperando {WAIT_SECONDS}s...")
        time.sleep(WAIT_SECONDS)
        
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)