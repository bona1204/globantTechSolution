from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract, case
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
    result = load_csv_to_table(db, file_path, model)
    return {
        "message": f"{table_name} loaded successfully",
        "inserted_rows": result["inserted"],
        "skipped_duplicates": result["skipped_duplicates"]
    }

@router.get("/report/hired_employees_by_quarter")
def hired_employees_by_quarter(db: Session = Depends(get_db)):
    query = db.query(
        Department.department.label("department"),
        Job.job.label("job"),
        func.sum(case(((extract('quarter', HiredEmployee.datetime) == 1, 1)), else_=0)).label("Q1"),
        func.sum(case(((extract('quarter', HiredEmployee.datetime) == 2, 1)), else_=0)).label("Q2"),
        func.sum(case(((extract('quarter', HiredEmployee.datetime) == 3, 1)), else_=0)).label("Q3"),
        func.sum(case(((extract('quarter', HiredEmployee.datetime) == 4, 1)), else_=0)).label("Q4"),
    ).join(Department, Department.id == HiredEmployee.department_id
    ).join(Job, Job.id == HiredEmployee.job_id
    ).filter(func.extract("year", HiredEmployee.datetime) == 2021
    ).group_by(Department.department, Job.job
    ).having(func.count(HiredEmployee.id) > 0
    ).order_by(Department.department, Job.job)

    return [dict(row._mapping) for row in query.all()]

@router.get("/report/top_10_departments")
def top_10_departments(db: Session = Depends(get_db)):
    query = (
        db.query(
            Department.id.label("department_id"),
            Department.department.label("department"),
            func.count(HiredEmployee.id).label("total_hires")
        )
        .join(HiredEmployee, Department.id == HiredEmployee.department_id)
        .filter(func.extract("year", HiredEmployee.datetime) == 2021)
        .group_by(Department.id, Department.department)
        .order_by(func.count(HiredEmployee.id).desc())
    )
    return [dict(row._mapping) for row in query.all()]
