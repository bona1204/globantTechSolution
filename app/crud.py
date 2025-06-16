import pandas as pd
from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def load_csv_to_table(session: Session, file_path: str, model):
    df = pd.read_csv(file_path)

    if model == models.HiredEmployee:
        df['datetime'] = pd.to_datetime(df['datetime'])

    for record in df.to_dict(orient="records"):
        session.add(model(**record))
    session.commit()
