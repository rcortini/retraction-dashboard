from fastapi import APIRouter
# from service import summarize_data

# init the routing
router = APIRouter(prefix="/status", tags=["status"])

# Overview of the status of the API
@router.get("/overview")
def get_data():
    return {'status':'OK'}
