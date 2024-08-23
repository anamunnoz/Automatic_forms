import pandas as pd
import psycopg2

# Parámetros de conexión
host = "localhost"          # Por ejemplo: "localhost"
dbname = "FormDB"      # Nombre de la base de datos
user = "postgres"       # Usuario de la base de datos
password = "postgres"  # Contraseña del usuario
port = "5432"             # Puerto por defecto de PostgreSQL

# Conectarse a la base de datos
conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
cur = conn.cursor()
try:
    cur.execute("""
    CREATE TABLE FORMULARIO ();
    """)
    conn.commit()
except:
    pass
# Ejecutar el comando COPY para insertar los datos del CSV
with open("respuestas.csv", 'r') as f:
    cur.copy_expert("COPY FORMULARIO FROM STDIN WITH CSV HEADER", f)

# Confirmar los cambios y cerrar la conexión
conn.commit()
cur.close()
conn.close()

