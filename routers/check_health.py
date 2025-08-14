from fastapi import APIRouter
from dotenv import load_dotenv
from db.connection import get_connection_gi, get_connection_siesa
from utils.is_reachable import is_reachable
from utils.is_valid_ip import is_valid
import os
import pyodbc

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
        ip_host = os.getenv("HOST_IP")

        # Si no existen las variables de entorno en el .env
        if not ip_siesa:
            errors.append("Falta variable de entorno 'SERVER'")
        runned_tests.append({'name': '¿Existe variable de entorno "SERVER" para Servidor SIESA?', "result": 'OK' if ip_siesa else 'Problemas detectados'})
        if not ip_gi:
            errors.append("Falta variable de entorno 'SERVER_GI'")
        runned_tests.append({'name': '¿Existe variable de entorno "SERVER_GI" para Servidor Gelcoinfo?', "result": 'OK' if ip_gi else 'Problemas detectados'})
        if not ip_host:
            errors.append("Falta variable de entorno 'HOST_IP'")
        runned_tests.append({'name': '¿Existe variable de entorno "HOST_IP"?', "result": 'OK' if ip_host else 'Problemas detectados'})
    except Exception as e:
        errors.append("No se pueden obtener las variables de entorno, crear el archivo .env")

    try:
        # Si no son alcanzables dentro de la red los servidores SQL.
        if ip_siesa and not is_reachable(ip_siesa):
            errors.append(f"No es alcanzable el servidor SIESA: {ip_siesa}")
        runned_tests.append({'name': '¿Es alcanzable el servidor SIESA?', 'result': 'OK' if ip_siesa and is_reachable(ip_siesa) else 'Problemas detectados'})
        if ip_gi and not is_reachable(ip_gi):
            errors.append(f'No es alcanzable el servidor de Gelcoinfo: {ip_gi}')
        runned_tests.append({'name': '¿Es alcanzable el servidor Gelcoinfo?', 'result': 'OK' if ip_gi and is_reachable(ip_gi) else 'Problemas detectados'})
    except Exception as e:
        errors.append(f"No se pudo verificar la conectividad de red: {e}")

    try:
        # Si las IP's son inválidas.
        if not is_valid(ip_gi):
            errors.append('Es inválida la IP proporcionada para servidor SQL de Gelcoinfo')
        runned_tests.append({'name': '¿Es válida la IP de Gelcoinfo?', 'result': 'OK' if is_valid(ip_gi) else 'Problemas detectados'})

        if not is_valid(ip_siesa):
            errors.append('Es inválida la IP proporcionada para servidor SQL de SIESA')
        runned_tests.append({'name': '¿Es válida la IP de SIESA?', 'result': 'OK' if is_valid(ip_siesa) else 'Problemas detectados'})
    except Exception as e:
        errors.append(f'Comuníquese con TI, el código está maldito. Esto no pudo haber sucedido: {e}')

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