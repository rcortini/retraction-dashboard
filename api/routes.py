from fastapi import APIRouter, Query
from shared.db import create_connection
from sqlalchemy import text
# from service import summarize_data

# init the routing
router = APIRouter()

# Overview of the status of the API
@router.get("/overview")
def get_data():
    return {'status':'OK'}

@router.get("/metrics/total-publications")
def get_total_publications():

    query = text("SELECT COUNT(DISTINCT id) FROM works")

    engine = create_connection()
    with engine.connect() as conn:
        result = conn.execute(query).scalar()

    return {"total_publications": result}

ALLOWED_GROUP_FIELDS = {
    "publication_year",
    "journal",
    "country"
}

@router.get("/analytics/aggregate")
def aggregate(group_by: str = Query(...)):
    if group_by not in ALLOWED_GROUP_FIELDS:
        return {"error": "Invalid group_by field"}

    query = text(f"""
        SELECT {group_by}, COUNT(*) as count
        FROM works
        GROUP BY {group_by}
        ORDER BY {group_by} DESC
    """)

    engine = create_connection()
    with engine.connect() as conn:
        results = conn.execute(query).fetchall()

    return {
        "data": [
            {"key": row[0], "count": row[1]}
            for row in results
        ]
    }