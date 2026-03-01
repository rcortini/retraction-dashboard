from fastapi import APIRouter
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