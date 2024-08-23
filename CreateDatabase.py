import psycopg2
import pandas as pd
from psycopg2 import sql
from psycopg2.extras import execute_values

# Conéctate al servidor PostgreSQL (a la base de datos 'postgres' por defecto)
def conect(user, password, host = "localhost", port = "5432"):
    try:
        conn = psycopg2.connect(
            user=user,
            password=password,
            host= host,
            port= port
        )
        conn.autocommit = True 
    except Exception as e:
        print(f"Error al conectarse al servidor PostgreSQL: {e}")
        exit()
    # Crear un cursor
    return conn 

def createDataBase(name: str, user:str, password:str, host:str, port:str):
    conn = conect(user, password, host, port)
    cursor = conn.cursor()
    # Crear la base de datos
    try:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(name)))
        print(f"Base de datos '{name}' creada exitosamente.")
    except Exception as e:
        print(e)

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()


def conect_db(dbname:str, user:str, password: str, host: str = "localhost", port: str = "5432"):
    conn = psycopg2.connect(
    dbname= dbname,
    user= user,
    password= password,
    host= host,
    port= port
    )
    return conn

def infer_sql_type(dtype):
    """Inferir el tipo de dato SQL a partir del tipo de dato de pandas."""
    if pd.api.types.is_integer_dtype(dtype):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(dtype):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "TIMESTAMP"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    else:
        return "TEXT"

def insert_db(csv_file: str, table_name: str, db_name:str, user: str, password: str, host:str, port: str):
    # Leer el archivo CSV
    df = pd.read_csv(csv_file)

    conn = conect_db(db_name, user, password)
    cursor = conn.cursor()

    columns = df.columns
    dtypes = df.dtypes

    # Crear la consulta SQL para la creación de la tabla
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    
    for column, dtype in zip(columns, dtypes):
        sql_type = infer_sql_type(dtype)
        if column.lower() == "responseid":
            create_table_query += f"{column} {sql_type} PRIMARY KEY, "
        else:
            create_table_query += f"{column} {sql_type}, "

    # Elimina la última coma y cierra la definición de la tabla
    create_table_query = create_table_query.rstrip(', ') + ')'

    cursor.execute(create_table_query)
    conn.commit()

    # Insertar los datos en la tabla
    # Generar la consulta SQL para la inserción de los datos
    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES %s"

    data_to_insert = []

    for row in df.itertuples(index=False, name=None):
        responseid = row[columns.get_loc("responseId")]
        
        # Comprobar si el responseid ya existe en la base de datos
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE responseid = %s", (responseid,))
        if cursor.fetchone() is None:
            data_to_insert.append(row)

    if data_to_insert:
        # Utilizar el método `execute_values` de psycopg2 para insertar los datos en bloque
        execute_values(cursor, insert_query, data_to_insert)

    # Confirmar los cambios
    conn.commit()

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

    print(f"Datos del archivo {csv_file} insertados exitosamente en la tabla {table_name}.")
