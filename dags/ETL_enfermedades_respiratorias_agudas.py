from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from procesamiento import extraccion_datos, transformacion_datos, carga_datos_redshift


default_args = {
    'owner': 'lucasleonetti',
    'start_date': datetime(2024, 1,10),
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'email_on_failure': False,
    'email_on_retry': False,
}

# Definir el DAG
with DAG(
    default_args=default_args,
    dag_id='ETL_enfermedades_respiratorias_agudas',
    description='DAG para extraer, transformar y cargar los datos de las enfermedades respiratorias agudas',
    tags = ['enfermedades_respiratorias', 'ETL', 'API', 'Redshift'],
    schedule_interval='@daily', # ejecutar cada día
    max_active_runs=1, # ejecutar solo un DAG a la vez
    ) as dag:

# Definir los operadores

    extraccion_datos_operator = PythonOperator(
        task_id='extraccion_datos',
        python_callable=extraccion_datos,
        provide_context=True, # permite pasar contexto a la función extraccion_datos
        dag=dag
    )   

    transformacion_datos_operator = PythonOperator(
        task_id='transformacion_datos',
        python_callable=transformacion_datos,
        provide_context=True, # permite pasar contexto a la función transformacion_datos
        depends_on_past=True,
        dag=dag
    )

    carga_datos_redshift_operator = PythonOperator(
        task_id='carga_datos_redshift',
        python_callable=carga_datos_redshift,
        provide_context=True, # permite pasar contexto a la función carga_datos_redshift
        depends_on_past=True,
        dag=dag
    )

# Definir 
extraccion_datos_operator >> transformacion_datos_operator
transformacion_datos_operator >> carga_datos_redshift_operator