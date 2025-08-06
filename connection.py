import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection_siesa():
    try:
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        SERVER = os.getenv("SERVER")
        DATABASE = os.getenv("DATABASE")
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
        USER = os.getenv("USER")
        PASSWORD = os.getenv("PASSWORD")
        SERVER_GI = os.getenv("SERVER_GI")
        DATABASE_GI = os.getenv("DATABASE_GI")
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER_GI};"
            f"DATABASE={DATABASE_GI};"
            f"UID={USER};"
            f"PWD={PASSWORD};"
        )
    except Exception as e:
        return conn
