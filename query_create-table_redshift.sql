
CREATE TABLE seguimiento_enfermedades_respiratorias (
    departamento_id INTEGER NOT NULL,
    departamento_nombre VARCHAR(100),
    provincia_id INTEGER NOT NULL,
    provincia_nombre VARCHAR(100),
    anio VARCHAR(4),
    semanas_epidemiologicas INTEGER,
    evento_nombre VARCHAR(100),
    grupo_edad_id INTEGER,
    grupo_edad_desc VARCHAR(100),
    cantidad_de_casos VARCHAR(100),
);
