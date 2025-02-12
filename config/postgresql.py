import psycopg2
import os

def get_postgres_connection_customer():
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST_CUSTOMER"),
            port=os.getenv("POSTGRES_PORT_CUSTOMER"),
            user=os.getenv("POSTGRES_USER_CUSTOMER"),
            password=os.getenv("POSTGRES_PASSWORD_CUSTOMER"),
            database=os.getenv("POSTGRES_DB_CUSTOMER")
        )
        print("Conexión exitosa a PostgreSQL")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

def get_postgres_connection_payments():
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST_PAYMENTS"),
            port=os.getenv("POSTGRES_PORT_PAYMENTS"),
            user=os.getenv("POSTGRES_USER_PAYMENTS"),
            password=os.getenv("POSTGRES_PASSWORD_PAYMENTS"),
            database=os.getenv("POSTGRES_DB_PAYMENTS")
        )
        print("Successful connection to PostgreSQL")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

