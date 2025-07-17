from fastapi import APIRouter
from dotenv import load_dotenv
from connection import get_connection_gi, get_connection_siesa
import os
import socket
import pyodbc
from utils.is_reachable import is_reachable

load_dotenv()

router = APIRouter(
    tags=["Diagnóstico de conexión y componentes de API."]
)

@router.get("/check_health", summary="Ejecuta diagnóstico de conexión, de red, y componentes.")
async def check_health():
    errors = []
    runned_tests = []
    # Diagnóstico de red
    try:
        ip_siesa = os.getenv("SERVER")
        ip_gi = os.getenv("SERVER_GI")

        # Si no existen las variables de entorno en el .env
        if not ip_siesa:
            errors.append("Falta variable de entorno 'SERVER'")
        runned_tests.append({'name': '¿Existe variable de entorno "SERVER" para Servidor SIESA?', "result": 'OK' if ip_siesa else 'Problemas detectados'})
        if not ip_gi:
            errors.append("Falta variable de entorno 'SERVER_GI'")
        runned_tests.append({'name': '¿Existe variable de entorno "SERVER_GI" para Servidor Gelcoinfo?', "result": 'OK' if ip_gi else 'Problemas detectados'})

        # Si no son alcanzables dentro de la red los servidores SQL.
        if ip_siesa and not is_reachable(ip_siesa):
            errors.append(f"No es alcanzable el servidor SIESA: {ip_siesa}")
        runned_tests.append({'name': '¿Es alcanzable el servidor SIESA?', 'result': 'OK' if ip_siesa and is_reachable(ip_siesa) else 'Problemas detectados'})
        if ip_gi and not is_reachable(ip_gi):
            errors.append(f'No es alcanzable el servidor de Gelcoinfo: {ip_gi}')
        runned_tests.append({'name': '¿Es alcanzable el servidor Gelcoinfo?', 'result': 'OK' if ip_gi and is_reachable(ip_gi) else 'Problemas detectados'})

        # Si las IP's son inválidas.
        ip_remote_gi = socket.gethostbyname(ip_gi) if ip_gi else None
        runned_tests.append({'name': '¿Es válida la IP de Gelcoinfo?', 'result': 'OK' if ip_remote_gi else 'Problemas detectados'})
        ip_remote_siesa = socket.gethostbyname(ip_siesa) if ip_siesa else None
        runned_tests.append({'name': '¿Es válida la IP de SIESA?', 'result': 'OK' if ip_remote_siesa else 'Problemas detectados'})

    except Exception as e:
        errors.append(f'No resuelve IP del servidor: {e}')

    # Diagnóstico de drivers
    try:
        drivers = [x for x in pyodbc.drivers()]  # Listar todos los drivers disponibles
        if not any("ODBC Driver 17 for SQL Server" in d for d in drivers):
            errors.append("Falta el driver 'ODBC Driver 17 for SQL Server'. Descargar desde https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server")
        runned_tests.append({
            'name': '¿Está instalado el driver "ODBC Driver 17 for SQL Server"?',
            'result': 'OK' if any("ODBC Driver 17 for SQL Server" in d for d in drivers) else 'Problemas detectados'
        })
    except Exception as e:
        errors.append(f"Error al obtener drivers: {e}")
        runned_tests.append({
            'name': '¿Se pudo obtener la lista de drivers ODBC?',
            'result': 'Problemas detectados'
        })

    # Diagnóstico de conexión a bases de datos
    try:
        conn_gi = get_connection_gi()
        conn_gi.close()
        runned_tests.append({
            'name': '¿Conexión exitosa a la base de datos Gelcoinfo?',
            'result': 'OK'
        })
    except Exception as e:
        errors.append(f"No se puede conectar a la base de datos Gelcoinfo: {e}")
        runned_tests.append({'name': '¿Conexión exitosa a la base de datos Gelcoinfo?', 'result': 'Problemas detectados'})

    try:
        conn_siesa = get_connection_siesa()
        conn_siesa.close()
        runned_tests.append({'name': '¿Conexión exitosa a la base de datos SIESA?', 'result': 'OK'})
    except Exception as e:
        errors.append(f"No se puede conectar a la base de datos SIESA: {e}")
        runned_tests.append({
            'name': '¿Conexión exitosa a la base de datos SIESA?',
            'result': 'Problemas detectados'
        })

    if errors:
        return {
            'status_environment': 'Problemas detectados',
            'details': errors,
            'runned_tests': runned_tests
        }

    return {
        'status_environment': 'OK',
        'runned_tests': runned_tests
    }