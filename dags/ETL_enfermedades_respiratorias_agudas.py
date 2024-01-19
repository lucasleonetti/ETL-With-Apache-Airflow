from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from procesamiento import extraccion_datos, transformacion_datos, carga_datos_redshift

# Definir el DAG
with DAG(
    dag_id='enfermedades_respiratorias_agudas',
    owner='Lucas Leonetti',
    description='DAG para extraer, transformar y cargar los datos de las enfermedades respiratorias agudas',
    start_date=datetime(2023, 10,31),
    schedule_interval='0 0 * * *'  # Ejecuta el DAG cada día a la medianoche
    ) as dag:

# Definir los operadores

    extraccion_datos_operator = PythonOperator(
        task_id='extraccion_datos',
        python_callable=extraccion_datos,
        dag=dag
    )   

    transformacion_datos_operator = PythonOperator(
        task_id='transformacion_datos',
        python_callable=transformacion_datos,
        depends_on_past=True,
        dag=dag
    )

    carga_datos_redshift_operator = PythonOperator(
        task_id='carga_datos_redshift',
        python_callable=carga_datos_redshift,
        depends_on_past=True,
        dag=dag
    )

# Definir las dependencias
extraccion_datos_operator >> transformacion_datos_operator
transformacion_datos_operator >> carga_datos_redshift_operator