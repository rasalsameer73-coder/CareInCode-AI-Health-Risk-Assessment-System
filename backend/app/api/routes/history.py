from fastapi import APIRouter

from app.services.health_record_service import (
    get_user_records
)
from app.services.vitals_history_service import (
    get_user_vitals_history
)

router = APIRouter(
    prefix="/history",
    tags=["History"]
)


@router.get("/{user_id}")
async def get_history(
    user_id: str
):
    records = get_user_records(user_id)
    return {
        "records": records
    }


@router.get("/vitals/{user_id}")
async def get_vitals_history(
    user_id: str
):
    records = get_user_vitals_history(user_id)
    return {
        "records": records
    }