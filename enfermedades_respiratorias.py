import requests
import pandas as pd

# llama a la API y obtengo los datos
def get_enfermedades_respiratorias_agudas_data():
    url = "http://datos.salud.gob.ar/dataset/c553d917-36f4-4063-ac02-1686a9120e1c/resource/26c85a05-d4e3-4124-b7d2-e087a6cc5f24/download/vigilancia-de-infecciones-respiratorias-agudas.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return "Error al obtener los datos de la API"
    

# obtengo los datos de la API
data = get_enfermedades_respiratorias_agudas_data()

# creo un dataframe con los datos
er_df = pd.DataFrame(data)

# muestro los 50 primeros registros del dataframe
print(er_df.head(50))

import missingno as msno

# analizo los datos faltantes con la libreria missingno
print(msno.matrix(er_df))

# agrupo los datos por provincia, evento y anio y muestra la cantidad de casos (primeros 50)

df_grouped = er_df.groupby(['provincia_nombre', 'evento_nombre', 'anio']).size().reset_index(name='cantidad_casos')
df_grouped = df_grouped.sort_values('provincia_nombre', ascending=False)
df_grouped.head(50)

    
import matplotlib.pyplot as plt

# filtro los datos por provincia en este caso 'Neuquen'
df_neuquen = df_grouped[df_grouped['provincia_nombre'] == 'Neuquen']

# grafico la cantidad de casos por evento y año en Neuquen
df_neuquen.pivot(index='evento_nombre', columns='anio', values='cantidad_casos').plot(kind='bar', figsize=(10, 6))
plt.xlabel('Evento')
plt.ylabel('Numero de Casos')
plt.title('Numero de Casos por Evento y Año en Neuquen')
print(plt.show())


# filtro los datos por provincia en este caso 'Cordoba'
df_neuquen = df_grouped[df_grouped['provincia_nombre'] == 'Cordoba']

# grafico la cantidad de casos por evento y año en Cordoba
df_neuquen.pivot(index='evento_nombre', columns='anio', values='cantidad_casos').plot(kind='bar', figsize=(10, 6))
plt.xlabel('Evento')
plt.ylabel('Numero de Casos')
plt.title('Numero de Casos por Evento y Año en Neuquen')
print(plt.show())

# Entregable numero 2
# Carga de datos a Amazon Redshift

import os
from sqlalchemy import create_engine, text


# importo las variables de entorno
REDSHIFT_HOST = os.environ["HOST"]
REDSHIFT_USER = os.environ["USER"]
REDSHIFT_PASSWORD = os.environ["PASSWORD"]
REDSHIFT_PORT = os.environ["PORT"]
REDSHIFT_DB = os.environ["DBNAME"]

# conecto a la base de datos
conn = create_engine(f"postgresql://{REDSHIFT_USER}:{REDSHIFT_PASSWORD}@{REDSHIFT_HOST}:{REDSHIFT_PORT}/{REDSHIFT_DB}")

# verificamos la conexion
try:
    with conn.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Conexión exitosa:", result.scalar() == 1)
except Exception as e:
    print("Error al conectar a la base de datos:", e)

# subo el dataframe a la base de datos en redshift en lotes de 1000 registros debido al tamaño del dataframe (+- 66.000 registros)
er_df.to_sql(name='seguimiento_enfermedades_respiratorias', con=conn, schema='lucasleone95_coderhouse', if_exists='replace', index=False, chunksize=1000)

# consulto la base de datos
def run_query(sql):
    result = conn.connect().execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

query_consult = """SELECT * FROM seguimiento_enfermedades_respiratorias LIMIT 10;"""

print(run_query(query_consult))