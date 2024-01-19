import requests
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import os
from sqlalchemy import create_engine, text

# llama a la API y obtengo los datos
def extraccion_datos():
    url = "http://datos.salud.gob.ar/dataset/c553d917-36f4-4063-ac02-1686a9120e1c/resource/26c85a05-d4e3-4124-b7d2-e087a6cc5f24/download/vigilancia-de-infecciones-respiratorias-agudas.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error al obtener los datos de la API"
    
def visualizacion_datos():
    # obtengo los datos de la API
    data = extraccion_datos()

    # creo un dataframe con los datos
    er_df = pd.DataFrame(data)

    # muestro los 50 primeros registros del dataframe
    print(er_df.head(50))
    
    return er_df
 
# Guardo el dataframe para analizarlo en el siguiente paso
er_df = visualizacion_datos()
# analizo los datos faltantes con la libreria missingno
print(msno.matrix(er_df))

def transformacion_datos():
    # agrupo los datos por provincia, evento y anio y muestra la cantidad de casos (primeros 50)
    df_grouped = er_df.groupby(['provincia_nombre', 'evento_nombre', 'anio']).size().reset_index(name='cantidad_casos')
    df_grouped = df_grouped.sort_values('provincia_nombre', ascending=False)

    # retorno el dataframe agrupado y ordenado
    return df_grouped

def carga_datos_redshift():
    
    # importo las variables de entorno
    REDSHIFT_HOST = os.getenv["HOST"]
    REDSHIFT_USER = os.getenv["USER"]
    REDSHIFT_PASSWORD = os.getenv["PASSWORD"]
    REDSHIFT_PORT = os.getenv["PORT"]
    REDSHIFT_DB = os.getenv["DBNAME"]

    # conecto a la base de datos
    conn = create_engine(f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}")

    # verificamos la conexion
    try:
        with conn.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Conexión exitosa:", result.scalar() == 1)
    except Exception as e:
        print("Error al conectar a la base de datos:", e)

    # almacenamos el dataframe con los datos transformados en una variable
    df_transformado = transformacion_datos()

    # subo el dataframe a la base de datos en redshift con los datos transformados
    df_transformado.to_sql(name='eventos_provinciales', con=conn, schema='lucasleone95_coderhouse', if_exists='append', index=False)

    # consulto la base de datos para verificar que se haya subido correctamente
    def run_query(sql):
        result = conn.connect().execute((text(sql)))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

    query_consult = """SELECT * FROM eventos_provinciales LIMIT 10;"""

    print(run_query(query_consult))



