# Entregable 2

## Alumno: Leonetti Lucas

Este entregable consta de los siguientes archivos:

### enfermedades_respiratorias.ipynb

Este archivo contiene el código de extracción de datos de la página del Ministerio de Salud de la Nación, en particular de la sección de Enfermedades Respiratorias. El código se encuentra en formato notebook de Jupyter, y se puede ejecutar en Google Colab o con la extension de jupyter en vscode o cualquier editor que soporte la extension.

El código se encuentra dividido en 3 secciones principales correspondientes a la *Entrega 1*:

1. Extracción de datos de la página web del Ministerio de Salud de la Nación.
2. Transformación de los datos extraídos.
3. Visualización de los datos transformados.
4. *Entrega 2* Carga de los datos en una tabla de Redshift.
5. consulta a la tabla de Redshift para verificar que los datos se hayan cargado correctamente.

### *Entrega 2*

Luego de la visualizacion se procede a la carga de los datos en una tabla de Redshift, para lo cual se utiliza la libreria (software ORM) SQLAlchemy para la conexión a la base de datos de Redshift. Se crea una tabla con los atributos de la tabla de datos de enfermedades respiratorias, y se cargan los datos en la misma. Finalmente se realiza una consulta a la tabla para verificar que los datos se hayan cargado correctamente.

### enfermedades_respiratorias.py

El mismo código se encuentra en formato de script de python, y se puede ejecutar en cualquier editor de texto o IDE que soporte python.

comando para ejecutar el script:

```bash
python3 enfermedades_respiratorias.py
```

### query_tabla_redshift.sql

Este archivo contiene el código de la query que se ejecuta en Redshift para crear la tabla con los atributos de la tabla de datos de enfermedades respiratorias.

### Captura de pantalla bases de datos en Dbeaver conectado a host de amazon Redshift

Este archivo contiene la captura de pantalla de la conexión a la base de datos de Redshift desde Dbeaver. Se puede ver la tabla creada con los datos de enfermedades respiratorias.

### Captura de pantalla de la tabla en Redshift ya cargada correspondiente a la entrega 2

Captura de pantalla de la tabla en resdhift con los datos de enfermedades respiratorias ya cargadas en la tabla
