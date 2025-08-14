import pyodbc
from db.config import SERVER, DATABASE, USER, PASSWORD, SERVER_GI, DATABASE_GI

def get_connection_siesa():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"UID={USER};"
            f"PWD={PASSWORD};"
        )
        return conn
    except Exception as e:
        return None

def get_connection_gi():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER_GI};"
            f"DATABASE={DATABASE_GI};"
            f"UID={USER};"
            f"PWD={PASSWORD};"
        )
        return conn
    except Exception as e:
        return None
