from typing import Optional
from pydantic import BaseModel, Field


class VitalsInput(BaseModel):

    heart_rate: Optional[float] = Field(None, ge=20, le=250)

    spo2: Optional[float] = Field(None, ge=50, le=100)

    temperature: Optional[float] = Field(None, ge=30, le=45)

    systolic_bp: Optional[float] = Field(None, ge=50, le=250)

    diastolic_bp: Optional[float] = Field(None, ge=30, le=200)

    weight: Optional[float] = Field(None, ge=1, le=500)

    steps: Optional[int] = Field(None, ge=0, le=100000)

    sleep_hours: Optional[float] = Field(None, ge=0, le=24)