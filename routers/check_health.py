from fastapi import APIRouter
from dotenv import load_dotenv
from connection import get_connection_gi, get_connection_siesa
import os
import socket
import pyodbc

load_dotenv()

router = APIRouter(
    tags=["Diagnóstico de conexión y componentes de API."]
)

@router.get("/check_health", summary="Ejecuta diagnóstico de conexión, de red, y componentes.")
async def check_health():
    errors = []
    # Diagnóstico de red
    try:
        ip_siesa = os.getenv("SERVER")
        ip_gi = os.getenv("SERVER_GI")
        if not ip_siesa:
            errors.append("Falta variable de entorno 'SERVER'")
        if not ip_gi:
            errors.append("Falta variable de entorno 'SERVER_GI'")
        ip_remote_gi = socket.gethostbyname(ip_gi) if ip_gi else None
        ip_remote_siesa = socket.gethostbyname(ip_siesa) if ip_siesa else None
    except Exception as e:
        errors.append(f'No resuelve IP del servidor: {e}')

    # Diagnóstico de drivers
    try:
        drivers = [x for x in pyodbc.drivers()] # Listar todos los drivers disponibles
        if not any("ODBC Driver 17 for SQL Server" in d for d in drivers):
            errors.append("Falta el driver 'ODBC Driver 17 for SQL Server'. Descargar desde https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server")
    except Exception as e:
        errors.append(f"Error al obtener drivers: {e}")

    # Diagnóstico de conexión
    try:
        conn_gi = get_connection_gi()
        conn_siesa = get_connection_siesa()
        conn_gi.close()
        conn_siesa.close()
    except Exception as e:
        errors.append(f"No se puede conectar a alguna base de datos: {e}")

    if errors:
        return {'message': 'Se encontraron errores en el entorno', 'status': 'Problemas detectados', 'details': errors}
    return {'message': 'Diagnóstico exitoso: Componentes de la API en orden', 'status': "OK"}