FROM apache/airflow:2.8.0
USER airflow

COPY requirements.txt .
COPY thresholds.json /app/thresholds.json
RUN pip install -r requirements.txt
