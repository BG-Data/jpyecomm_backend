import psycopg2
from psycopg2 import OperationalError

def create_conn():
    conn = None
    try:
        conn = psycopg2.connect(
            database="ecomm_db",
            user="user",
            password="test",
            host="url",
            port="5432", # change this to your port number
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return conn

connection = create_conn()

