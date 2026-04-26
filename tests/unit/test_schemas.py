"""Unit tests for wearable data Pydantic schemas."""
import pytest
from pydantic import ValidationError
from src.ingestion.schemas import VitalSign, PatientMetadata, WearableReading
import uuid
from datetime import datetime, timezone


def make_valid_reading(**overrides) -> dict:
    base = {
        "reading_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc),
        "patient": {
            "patient_id": "PAT-000001",
            "device_id": "WD-ABCD1234",
            "ward": "ICU",
            "age": 65,
            "gender": "M",
        },
        "vitals": {
            "heart_rate": 72.0,
            "spo2": 98.5,
            "temperature": 36.8,
        },
    }
    base.update(overrides)
    return base


def test_valid_vital_sign():
    v = VitalSign(heart_rate=75, spo2=98, temperature=36.8)
    assert v.heart_rate == 75


def test_heart_rate_zero_raises():
    with pytest.raises(ValidationError, match="Heart rate of 0"):
        VitalSign(heart_rate=0, spo2=98, temperature=36.8)


def test_spo2_out_of_range():
    with pytest.raises(ValidationError):
        VitalSign(heart_rate=75, spo2=110, temperature=36.8)


def test_valid_patient_metadata():
    p = PatientMetadata(patient_id="PAT-000001", device_id="WD-ABCD1234")
    assert p.patient_id == "PAT-000001"


def test_invalid_device_id_format():
    with pytest.raises(ValidationError):
        PatientMetadata(patient_id="PAT-000001", device_id="INVALID")


def test_wearable_reading_is_critical_false():
    r = WearableReading(**make_valid_reading())
    assert not r.is_critical


def test_wearable_reading_is_critical_low_spo2():
    data = make_valid_reading()
    data["vitals"]["spo2"] = 85.0
    r = WearableReading(**data)
    assert r.is_critical


@pytest.mark.parametrize("hr,expected", [
    (160, True), (30, True), (75, False), (45, False), (150, False)
])
def test_is_critical_heart_rate(hr, expected):
    data = make_valid_reading()
    data["vitals"]["heart_rate"] = hr
    r = WearableReading(**data)
    assert r.is_critical == expected

# 09:59:11 — automated update
# feat: add realistic heart rate variation algorithm in simulator

# 09:59:11 — automated update
# perf improvement at 09:59:11
_CACHE: dict = {}  # perf: switch from json to orjson seriali
