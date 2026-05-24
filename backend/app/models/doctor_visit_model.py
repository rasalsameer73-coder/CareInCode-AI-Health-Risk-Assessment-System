from typing import List, Optional

from pydantic import BaseModel


class MedicationEntry(BaseModel):
    id: str
    name: str
    dosage: Optional[str] = None
    reason: Optional[str] = None


class SymptomEntry(BaseModel):
    id: str
    date: str
    location: Optional[str] = None
    intensity: int
    triggers: Optional[str] = None
    notes: Optional[str] = None


class DoctorVisitSummary(BaseModel):
    headline: str
    facts: List[str]
    summaryText: str
    questions: List[str]


class DoctorVisitPayload(BaseModel):
    user_id: str = "demo_user"
    medications: List[MedicationEntry] = []
    symptoms: List[SymptomEntry] = []
    summary: Optional[DoctorVisitSummary] = None
