"""Pydantic schemas for wearable sensor data ingestion."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class VitalSign(BaseModel):
    """Core vital sign reading from a wearable device."""
    heart_rate: float = Field(..., ge=0, le=300, description="BPM")
    spo2: float = Field(..., ge=50.0, le=100.0, description="Blood oxygen %")
    temperature: float = Field(..., ge=30.0, le=45.0, description="Celsius")
    respiratory_rate: Optional[float] = Field(None, ge=0, le=60)
    systolic_bp: Optional[float] = Field(None, ge=50, le=250)
    diastolic_bp: Optional[float] = Field(None, ge=30, le=150)

    @field_validator("heart_rate")
    @classmethod
    def heart_rate_not_zero(cls, v: float) -> float:
        if v == 0:
            raise ValueError("Heart rate of 0 indicates sensor error")
        return v


class PatientMetadata(BaseModel):
    """Patient and device identification metadata."""
    patient_id: str = Field(..., min_length=6, max_length=64)
    device_id: str = Field(..., pattern=r"^WD-[A-Z0-9]{8}$")
    ward: Optional[str] = None
    age: Optional[int] = Field(None, ge=0, le=130)
    gender: Optional[str] = Field(None, pattern=r"^(M|F|O)$")


class WearableReading(BaseModel):
    """Composite wearable reading: vitals + metadata + timestamp."""
    reading_id: str
    timestamp: datetime
    patient: PatientMetadata
    vitals: VitalSign
    signal_quality: float = Field(1.0, ge=0.0, le=1.0)
    firmware_version: str = "1.0.0"

    @property
    def is_critical(self) -> bool:
        return (
            self.vitals.spo2 < 90
            or self.vitals.heart_rate > 150
            or self.vitals.heart_rate < 40
        )
