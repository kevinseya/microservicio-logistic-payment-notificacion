import psycopg2
import os

def get_postgres_connection():
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            database=os.getenv("POSTGRES_DB")
        )
        print("Conexión exitosa a PostgreSQL")
        return connection
    except psycopg2.Error as e:
        print(f"Error de conexión a PostgreSQL: {e}")
        raise
