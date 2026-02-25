import os
import pandas as pd
from shared.models import works
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert

def create_connection():
    connection_url = os.environ.get("DB_CONNECTION_URL")
    if not connection_url:
        raise ValueError("DB_CONNECTION_URL not defined")
    return create_engine(connection_url)

def get_last_update_ts(engine):
    query = """SELECT last_updated_date FROM ingestion_metadata ORDER BY id DESC LIMIT 1;"""
    with engine.connect() as connection:
        df = pd.read_sql(query, con=connection)
    return df\
        .at[0, "last_updated_date"]\
        .isoformat()

def upsert_records(engine, records):
    stmt = insert(works).values(records)

    update_cols = {
        c.name: stmt.excluded[c.name]
        for c in works.columns
        if c.name != "id"
    }

    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=update_cols,
        where=works.c.updated_date < stmt.excluded.updated_date
    )

    with engine.begin() as conn:
        conn.execute(stmt)