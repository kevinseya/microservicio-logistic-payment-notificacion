import mysql.connector
import os

def get_mysql_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            port=os.getenv("MYSQL_PORT"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        print("Conexión exitosa a MySQL")
        return connection
    except mysql.connector.Error as e:
        print(f"Error de conexión a MySQL: {e}")
        raise
