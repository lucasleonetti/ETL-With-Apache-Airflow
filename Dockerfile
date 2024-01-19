FROM apache/airflow:2.8.0

USER airflow

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
