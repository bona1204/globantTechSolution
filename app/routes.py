from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Department, Job, HiredEmployee
from app.crud import load_csv_to_table

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/{table_name}")
def upload_csv(table_name: str, db: Session = Depends(get_db)):
    table_map = {
        "departments": (Department, "data/departments.csv"),
        "jobs": (Job, "data/jobs.csv"),
        "hired_employees": (HiredEmployee, "data/hired_employees.csv")
    }
    if table_name not in table_map:
        return {"error": "Invalid table name"}
    
    model, file_path = table_map[table_name]
    load_csv_to_table(db, file_path, model)
    return {"message": f"{table_name} loaded successfully"}
