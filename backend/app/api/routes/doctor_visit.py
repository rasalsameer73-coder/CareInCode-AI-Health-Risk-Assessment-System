from fastapi import APIRouter, HTTPException

from app.models.doctor_visit_model import (
    DoctorVisitPayload,
)
from app.services.doctor_visit_service import (
    get_doctor_visit_data,
    save_doctor_visit_data,
)
from app.services.doctor_visit_history_service import (
    get_doctor_visit_history,
)

router = APIRouter(
    prefix="/doctor-visit-prep",
    tags=["Doctor Visit Prep"],
)


@router.get("/")
def load_doctor_visit_prep(user_id: str = "demo_user"):
    record = get_doctor_visit_data(user_id)
    if not record:
        raise HTTPException(status_code=404, detail="No saved doctor visit preparation found.")
    return record


@router.get("/history/{user_id}")
def load_doctor_visit_history(user_id: str):
    records = get_doctor_visit_history(user_id)
    return {"records": records}


@router.post("/")
def save_doctor_visit_prep(payload: DoctorVisitPayload):
    record = save_doctor_visit_data(
        payload.user_id,
        [item.dict() for item in payload.medications],
        [item.dict() for item in payload.symptoms],
    )
    return record
