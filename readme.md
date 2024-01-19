# Proyecto de Enfermedades Respiratorias Agudas

Este proyecto realiza la extracción, transformación y carga (ETL) de datos de enfermedades respiratorias agudas del Ministerio de Salud de la Nación.

## Estructura del Proyecto

El proyecto consta de los siguientes archivos y directorios:

- `procesamiento.py`: Este archivo Python contiene las funciones utilizadas para la extracción, transformación y carga de los datos.

- `dags/ETL_enfermedades_respiratorias_agudas.py`: Este archivo define el DAG (Directed Acyclic Graph) para Apache Airflow, que automatiza y programa la ejecución de las tareas de ETL.

- `requirements.txt`: Este archivo lista las dependencias de Python necesarias para ejecutar el proyecto.

## Cómo ejecutar el proyecto

1. Clonar el repositorio

2. ejecutar `docker-compose airflow-init` en la raíz del proyecto

3. ejecutar `docker-compose up` en la raíz del proyecto

4. Abrir el navegador en `localhost:8080` y activar el DAG `ETL_enfermedades_respiratorias_agudas`

5. Ejecutar el DAG
