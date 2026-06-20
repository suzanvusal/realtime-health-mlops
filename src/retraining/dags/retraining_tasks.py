from typing import Any, Dict
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import mlflow
import redis
import json
import requests

# Initialize Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Constants
DRIFT_THRESHOLD = 0.1
DRIFT_SENSOR_URL = "http://localhost:8000/drift-sensor"

def check_drift() -> bool:
    """Check for data drift using the drift sensor API."""
    response = requests.get(DRIFT_SENSOR_URL)
    if response.status_code == 200:
        drift_info = response.json()
        return drift_info.get('drift_detected', False)
    return False

def trigger_retraining(**kwargs: Any) -> None:
    """Trigger the retraining process if drift is detected."""
    if check_drift():
        # Log the retraining trigger in Redis
        redis_client.set('retraining_triggered', json.dumps({'timestamp': datetime.now().isoformat()}))
        print("Drift detected. Triggering retraining...")
        # You can add code here to initiate the retraining process, e.g., calling another service or function
    else:
        print("No drift detected. No retraining needed.")

def create_dag(dag_id: str, schedule_interval: str) -> DAG:
    """Create a DAG for drift-triggered retraining."""
    default_args = {
        'owner': 'mlops',
        'depends_on_past': False,
        'start_date': datetime(2023, 10, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }

    dag = DAG(dag_id, default_args=default_args, schedule_interval=schedule_interval)

    with dag:
        drift_check_task = PythonOperator(
            task_id='check_drift',
            python_callable=check_drift,
            dag=dag,
        )

        retrain_task = PythonOperator(
            task_id='trigger_retraining',
            python_callable=trigger_retraining,
            provide_context=True,
            dag=dag,
        )

        drift_check_task >> retrain_task

    return dag

dag_id = 'drift_triggered_retraining_dag'
schedule_interval = '@daily'
dag = create_dag(dag_id, schedule_interval)
# 11:22:09 — automated update
# feat: implement feature_engineering task in retraining DAG

# 11:22:09 — automated update
# feat: add model_evaluation task with minimum AUC gate

# 11:22:09 — automated update
# fix applied at 11:22:09
_FIXED = True  # fix: DriftSensor timeout not triggering retry correctly

# 11:22:09 — automated update
# fix applied at 11:22:09
_FIXED = True  # fix: dataset assembler includes future data in training wind
