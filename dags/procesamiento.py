from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import logging
import smtplib
import requests
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine, text
import requests
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt

# llama a la API y obtengo los datos
def extraccion_datos(**kwargs):
    url = "http://datos.salud.gob.ar/dataset/c553d917-36f4-4063-ac02-1686a9120e1c/resource/26c85a05-d4e3-4124-b7d2-e087a6cc5f24/download/vigilancia-de-infecciones-respiratorias-agudas.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("Datos obtenidos correctamente")
        data_frame= pd.DataFrame(data) # convierto los datos en un dataframe
    else:
        return "Error al obtener los datos de la API"
    
    # guardo los datos en un xcom para poder utilizarlos en el siguiente paso
    kwargs['ti'].xcom_push(key='datos', value=data_frame)

def transformacion_datos(**kwargs):
    # obtengo los datos del xcom
    er_df = kwargs['ti'].xcom_pull(key='datos', task_ids='extraccion_datos')
    
    # agrupo los datos por provincia, evento y anio y muestra la cantidad de casos (primeros 50)
    df_grouped = er_df.groupby(['provincia_nombre', 'evento_nombre', 'anio']).size().reset_index(name='cantidad_casos')
    df_grouped = df_grouped.sort_values('provincia_nombre', ascending=False)

    # guardo los datos transformados en un xcom para poder utilizarlos en el siguiente paso
    kwargs['ti'].xcom_push(key='datos_transformados', value=df_grouped)

def carga_datos_redshift(**kwargs):
    
    # importo las variables de entorno
    REDSHIFT_HOST = os.getenv("HOST")
    REDSHIFT_USER = os.getenv("USER")
    REDSHIFT_PASSWORD = os.getenv("PASSWORD")
    REDSHIFT_PORT = os.getenv("PORT")
    REDSHIFT_DB = os.getenv("DBNAME")

    # conecto a la base de datos
    conn = create_engine(f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}")

    # verificamos la conexion
    try:
        with conn.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión exitosa:", result.scalar() == 1)
    except Exception as e:
        print("Error al conectar a la base de datos:", e)

    # obtengo los datos transformados del xcom
    df_transformado = kwargs['ti'].xcom_pull(key='datos_transformados', task_ids='transformacion_datos')

    # Obtener el valor máximo de la "cantidad_casos" para cada "provincia_nombre" en la tabla "eventos_provinciales"
    with conn.connect() as connection:
        result = connection.execute(text("SELECT provincia_nombre, MAX(cantidad_casos) FROM lucasleone95_coderhouse.eventos_provinciales GROUP BY provincia_nombre"))
        max_casos_por_provincia = {row['provincia_nombre']: row['max'] for row in result}

    # Filtrar el DataFrame para solo incluir los datos nuevos que superen el valor máximo de "cantidad_casos" para cada "provincia_nombre"
    for provincia, max_casos in max_casos_por_provincia.items():
        df_transformado = df_transformado[(df_transformado['provincia_nombre'] != provincia) | (df_transformado['cantidad_casos'] > max_casos)]

    # subo el dataframe a la base de datos en redshift con los datos transformados
    df_transformado.to_sql(name='eventos_provinciales', con=conn, schema='lucasleone95_coderhouse', if_exists='append', index=False)

    # Luego de subir los datos a la base de datos, verificamos los thresholds y enviamos un email si se supera
    procesar_datos()

def leer_threshold():
    with open("../thresholds.json", "r") as file:
        threshold = json.load(file)
    return threshold

def enviar_alerta_por_email(asunto,mensaje,destinatario):
    
    mi_correo = os.getenv("EMAIL")
    mi_password = os.getenv("PASSWORD_EMAIL")
    
    # Crear el objeto mensaje
    msg = MIMEMultipart()
    msg['From'] = mi_correo
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Agregar el mensaje al cuerpo del correo
    msg.attach(MIMEText(mensaje, 'plain'))
    
    # Crear el servidor
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mi_correo, mi_password)
    text = msg.as_string()
    server.sendmail(mi_correo, destinatario, text)
    server.quit() 
    
def procesar_datos():
     # importo las variables de entorno
    REDSHIFT_HOST = os.getenv("HOST")
    REDSHIFT_USER = os.getenv("USER")
    REDSHIFT_PASSWORD = os.getenv("PASSWORD")
    REDSHIFT_PORT = os.getenv("PORT")
    REDSHIFT_DB = os.getenv("DBNAME")

    # conecto a la base de datos
    conn = create_engine(f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}")
    
    # Creo un cursor para ejecutar la consulta
    cursor = conn.cursor()
    
    # consulta SQL que obtiene la cantidad de casos por anio
    query = """
    SELECT SUM(cantidad_casos) FROM eventos_provinciales
    """
    
    # ejecuto la consulta
    cursor.execute(query)
    suma_datos = cursor.fetchone()[0]
    
    # Luego de obtener la suma, verificamos los thresholds y enviamos un email si se supera
    threshold = leer_threshold()
    if suma_datos > threshold['maxCasosPorAnio']:
        destinatario = os.getenv("DESTINATARIO_EMAIL")
        enviar_alerta_por_email("Alerta de procesamiento:", "El número de casos sobrepasó el umbral de los 20.000 casos de enfermedades respiratorias agudas en Argentina", destinatario)
        logging.info("Sobrepaso de umbral, Se envió un email de alerta")
                                
    