# Proyecto de Enfermedades Respiratorias Agudas

Este proyecto realiza la extracción, transformación y carga (ETL) de datos de enfermedades respiratorias agudas del Ministerio de Salud de la Nación.

## Estructura del Proyecto

El proyecto consta de los siguientes archivos y directorios:

- `enfermedades_respiratorias.ipynb`: Este archivo Jupyter Notebook contiene el código para la extracción de datos, transformación y visualización. El mismo código se encuentra en el archivo `procesamiento.py` pero es presentado de igual manera en un Jupyter Notebook para facilitar la visualización de los resultados.

- `procesamiento.py`: Este archivo Python contiene las funciones utilizadas para la extracción, transformación y carga de los datos.

- `dags/ETL_enfermedades_respiratorias_agudas.py`: Este archivo define el DAG (Directed Acyclic Graph) para Apache Airflow, que automatiza y programa la ejecución de las tareas de ETL.

- `requirements.txt`: Este archivo lista las dependencias de Python necesarias para ejecutar el proyecto.

## Cómo ejecutar el proyecto

1. Instala las dependencias de Python con pip:

```sh
pip install -r requirements.txt
```
