from fastapi import APIRouter

from app.models.vitals_model import (
    VitalsInput
)

from app.orchestrator.vitals_orchestrator import (
    process_vitals
)

from app.services.vitals_history_service import (
    save_vitals_history
)

router = APIRouter(
    prefix="/vitals",
    tags=["Vitals Analysis"]
)

analysis_router = APIRouter(
    prefix="/analysis",
    tags=["Vitals Analysis"]
)


@router.post("/")
@analysis_router.post("/vitals")
async def analyze_vitals_route(
    data: VitalsInput,
    user_id: str = "demo_user"
):
    vitals_data = data.model_dump()
    analysis = process_vitals(vitals_data)
    save_vitals_history(user_id, vitals_data, analysis)
    return analysis
