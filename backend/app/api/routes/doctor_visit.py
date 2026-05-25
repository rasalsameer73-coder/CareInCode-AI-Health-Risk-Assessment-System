from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

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


# -------------------------
# SIMPLE REQUEST MODEL
# -------------------------

class DoctorVisitRequest(BaseModel):
    user_id: str
    medications: list = []
    symptoms: list = []


# -------------------------
# GET SAVED PREP
# -------------------------

@router.get("")
def load_doctor_visit_prep(user_id: str = "demo_user"):

    record = get_doctor_visit_data(user_id)

    if not record:
        raise HTTPException(
            status_code=404,
            detail="No saved doctor visit preparation found."
        )

    return record


# -------------------------
# HISTORY
# -------------------------

@router.get("/history/{user_id}")
def load_doctor_visit_history(user_id: str):

    records = get_doctor_visit_history(user_id)

    return {
        "records": records
    }


# -------------------------
# SAVE PREP
# -------------------------

@router.post("")
def save_doctor_visit_prep(payload: DoctorVisitPayload):

    record = save_doctor_visit_data(
        payload.user_id,
        [item.dict() for item in payload.medications],
        [item.dict() for item in payload.symptoms],
    )

    return record


# -------------------------
# GENERATE SUMMARY
# -------------------------

@router.post("/generate-summary")
async def generate_summary(data: DoctorVisitRequest):

    summary = f"""
Patient ID: {data.user_id}

Symptoms:
{", ".join(data.symptoms) if data.symptoms else "No symptoms added"}

Medications:
{", ".join(data.medications) if data.medications else "No medications added"}

Suggested Questions:
- What could be causing these symptoms?
- Are additional tests needed?
- Should medications be adjusted?
"""

    return {
        "success": True,
        "summary": summary
    }