import pandas as pd
from sqlalchemy.orm import Session
def load_csv_to_table(session: Session, file_path: str, model):
    column_names_map = {
        "departments": ["id", "department"],
        "jobs": ["id", "job"],
        "hired_employees": ["id", "name", "datetime", "department_id", "job_id"]
    }

    table_name = model.__tablename__
    columns = column_names_map[table_name]

    df = pd.read_csv(file_path, header=None, names=columns)

    if table_name == "hired_employees":
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    df = df.dropna()

    records = df.to_dict(orient="records")

    existing_ids = {r[0] for r in session.query(model.id).all()}
    records = [r for r in records if int(r["id"]) not in existing_ids]
    skipped_duplicates = len(df) - len(records)

    if table_name == "hired_employees":
        batch_size = 1000
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            session.bulk_save_objects([model(**record) for record in batch])
            session.commit()
    else:
        for record in records:
            session.add(model(**record))
        session.commit()
    return {
        "inserted": len(records),
        "skipped_duplicates": skipped_duplicates
    }