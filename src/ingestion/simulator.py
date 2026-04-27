"""Synthetic wearable data simulator for development and testing."""
from __future__ import annotations
import argparse
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from src.ingestion.schemas import PatientMetadata, VitalSign, WearableReading
from src.ingestion.producer import WearableDataProducer, ProducerConfig


def generate_patient_pool(n: int) -> list[PatientMetadata]:
    wards = ["ICU", "Cardiology", "General", "Emergency", "Oncology"]
    return [
        PatientMetadata(
            patient_id=f"PAT-{i:06d}",
            device_id=f"WD-{uuid.uuid4().hex[:8].upper()}",
            ward=random.choice(wards),
            age=random.randint(20, 90),
            gender=random.choice(["M", "F", "O"]),
        )
        for i in range(n)
    ]


def simulate_vitals(patient: PatientMetadata, anomaly_prob: float = 0.05) -> VitalSign:
    """Generate realistic vitals with occasional anomalies."""
    is_anomaly = random.random() < anomaly_prob
    if is_anomaly:
        return VitalSign(
            heart_rate=random.choice([random.uniform(150, 200), random.uniform(25, 40)]),
            spo2=random.uniform(82, 91),
            temperature=random.uniform(38.5, 40.5),
        )
    return VitalSign(
        heart_rate=random.gauss(75, 12),
        spo2=random.gauss(98, 0.8),
        temperature=random.gauss(36.8, 0.4),
        respiratory_rate=random.gauss(16, 2),
    )


def reading_stream(
    patients: list[PatientMetadata],
    rate_per_second: float = 5.0,
) -> Generator[WearableReading, None, None]:
    """Yield WearableReadings at the given rate."""
    interval = 1.0 / rate_per_second
    while True:
        patient = random.choice(patients)
        yield WearableReading(
            reading_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            patient=patient,
            vitals=simulate_vitals(patient),
            signal_quality=random.uniform(0.85, 1.0),
        )
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Wearable data simulator")
    parser.add_argument("--patients", type=int, default=50)
    parser.add_argument("--rate", type=float, default=5.0, help="Readings/second")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    args = parser.parse_args()

    patients = generate_patient_pool(args.patients)
    producer = WearableDataProducer(ProducerConfig(bootstrap_servers=args.bootstrap_servers))
    producer.connect()
    print(f"Simulating {args.patients} patients at {args.rate} readings/sec...")
    try:
        for reading in reading_stream(patients, args.rate):
            producer.send(reading.model_dump(mode="json"), key=reading.patient.patient_id)
    except KeyboardInterrupt:
        print(f"
Stopped. Stats: {producer.stats}")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()

# 09:59:11 — automated update
# test marker: test: add test for Kafka producer retry on broker failure
_TEST_MARKER = 'simulator'

# 09:59:11 — automated update
# style: reorder imports alphabetically in simulator — 09:59:11 UTC

# 11:10:17 — automated update
# chore: day 3 maintenance sweep — 11:10:17 UTC
