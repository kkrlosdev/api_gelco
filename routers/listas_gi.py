from fastapi import APIRouter
from db.connection import get_connection_gi
from utils.fetch_one import fetch_one
from fastapi import HTTPException
from utils.sql_runner import execute_dynamic_sql

router = APIRouter(
    prefix="/listas",
    tags=["Listas de Gelcoinfo"]
)

@router.get("/{genCod}", summary="Ejecuta dinámicamente el código de una lista de Gelcoinfo y retorna su resultado.")
async def get_lista(genCod: str):
    try:
        conn = get_connection_gi()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM for_gen WHERE genCod = ?", genCod)
        record = fetch_one(cursor)

        if not record:
            raise HTTPException(status_code=404, detail="genCod no encontrado")

        dynamic_query = record['genUsrStr2']
        result = execute_dynamic_sql(cursor, dynamic_query)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()