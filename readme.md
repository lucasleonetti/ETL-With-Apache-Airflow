# Proyecto de Enfermedades Respiratorias Agudas

Este proyecto realiza la extracción, transformación y carga (ETL) de datos de enfermedades respiratorias agudas del Ministerio de Salud de la Nación Argentina.

## Estructura del Proyecto

El proyecto consta de los siguientes archivos y directorios:

- `dags/procesamiento.py`: Este archivo Python contiene las funciones utilizadas para la extracción, transformación y carga de los datos.

- `dags/ETL_enfermedades_respiratorias_agudas.py`: Este archivo define el DAG (Directed Acyclic Graph) para Apache Airflow, que automatiza y programa la ejecución de las tareas de ETL.

- `requirements.txt`: Este archivo lista las dependencias de Python necesarias para ejecutar el proyecto.

- `screenshots/`: Este directorio contiene capturas de pantalla de la ejecución en distintas etapas del proceso.

- `docker-compose.yml`: Este archivo define los servicios de Docker necesarios para ejecutar el proyecto.

- `Dockerfile`: Este archivo define la imagen de Docker que se utilizará para ejecutar enuestro proyecto en un contenedor de Docker.  

- `airflow.cfg`: Este archivo contiene la configuración de Apache Airflow. Como definir el executor, el directorio de almacenamiento de los logs, el directorio de almacenamiento de los DAGs, entre otros.

- `thresholds.json`: Este archivo contiene los umbrales criticos para el envio de emails.

## Variables de entorno

En el caso de que quieras ejecutar el proyecto en tu computadora, deberás definir las siguientes variables de entorno creando en el directorio raíz del proyecto un archivo `.env` el cual contendra las credenciales de acceso a tu base de datos y del controlador de envio de emails para las alertas, la direccion de email del destinatario que recibira la alerta. El archivo `.env` deberá tener el siguiente formato:

```bash
# .env
POSTGRES_USER=ejemplo-user
POSTGRES_PASSWORD=ejemplo-password
POSTGRES_DB=ejemplo-db
POSTGRES_HOST=ejemplo-host
POSTGRES_PORT=5432
EMAIL=ejemplo-email
PASSWORD_EMAIL=ejemplo-password
DESTINATARIO_EMAIL=ejemplo-destinatario-email
```

## Flujo de trabajo

El flujo de trabajo del proyecto es el siguiente:

1. El DAG `ETL_enfermedades_respiratorias_agudas` se ejecuta diariamente a las 00:00 hs.
2. La tarea `extraccion_datos` extrae los datos de enfermedades respiratorias agudas del Ministerio de Salud de la Nación Argentina.
3. La tarea `transformacion_datos` transforma los datos extraídos.
4. La tarea `carga_datos_redshift` carga los datos transformados en una base de datos de Amazon Redshift.
5. En el caso de que los datos sobrepasen un umbral critico (en nuestro caso, la cantidad de casos de enfermedades respiratorias agudas), se envía un email a los destinatarios especificados en la tarea `enviar_email` con un reporte de la cantidad de casos de enfermedades respiratorias agudas.

## Cómo ejecutar el proyecto

1. Clonar el repositorio

2. ejecutar `docker compose build` en la raíz del proyecto para construir la imagen de nuestro proyecto en Docker e instalar las dependencias de Python

3. ejecutar `docker compose up airflow-init` en la raíz del proyecto

4. ejecutar `docker compose up` en la raíz del proyecto

5. Abrir el navegador en `localhost:8080` y activar el DAG `ETL_enfermedades_respiratorias_agudas`

6. Ejecutar el DAG
