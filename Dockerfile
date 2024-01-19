FROM apache/airflow:2.8.0
USER airflow

COPY . .
RUN pip install -r requirements.txt
