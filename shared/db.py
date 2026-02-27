import os
import pandas as pd
from shared.models import works, ingestion_metadata
from sqlalchemy import create_engine, text, select
from sqlalchemy.dialects.postgresql import insert

def create_connection():
    connection_url = os.environ.get("DB_CONNECTION_URL")
    if not connection_url:
        raise ValueError("DB_CONNECTION_URL not defined")
    return create_engine(connection_url)

def get_last_update_ts(engine):
    stmt = select(ingestion_metadata.c.last_updated_date).where(
        ingestion_metadata.c.source == "openalex"
    )

    with engine.connect() as conn:
        result = conn.execute(stmt).scalar_one()

    return result.isoformat()

def upsert_records(engine, records):
    stmt = insert(works).values(records)

    update_cols = {
        c.name: stmt.excluded[c.name]
        for c in works.columns
        if c.name != "id"
    }

    max_updated_date = max(r[-1] for r in records)
    with engine.begin() as conn:
        # upsert records
        upsert_stmt = stmt.on_conflict_do_update(
            index_elements=["id"],
            set_=update_cols,
            where=works.c.updated_date < stmt.excluded.updated_date
        )    
        conn.execute(upsert_stmt)

        # update the checkpoint timestamp
        checkpoint_stmt = text("""
            UPDATE ingestion_metadata
            SET last_updated_date = :ts,
                last_run_at = NOW()
            WHERE source = 'openalex'
        """)
        
        conn.execute(checkpoint_stmt, {"ts": max_updated_date})
    

