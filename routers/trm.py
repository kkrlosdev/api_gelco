from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from db.connection import get_connection_siesa
from utils.fetch_all import fetch_all

router = APIRouter(
    tags= ["Tasas representativas del mercado"]
)

@router.get("/tasas_representativas", summary="Consulta las tasas representativas para USD ($) y EUR")
def get_tasas_representativas(dias_atras: int):
    try:
        conn = get_connection_siesa()
        cursor = conn.cursor()
        cursor.execute("""
SELECT
    [F018_ID_MONEDA] AS 'moneda'
    ,[F018_TASA] AS 'tasa_representativa'
    ,CAST([F018_TS] AS DATE) AS 'fecha'
FROM
    [UnoEE_Gelco_Real].[dbo].[T018_MM_TASAS_CAMBIO]
WHERE
    (TRY_CAST(F018_TS AS DATE) >= TRY_CAST(DATEADD(DAY, -?, GETDATE()) AS DATE))
    AND F018_ID_MONEDA IN ('USD', 'EUR')
    AND F018_ID_CIA = 1
    ORDER BY [F018_ID_MONEDA], [F018_TS]
""", (dias_atras,))
        data = fetch_all(cursor)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail={'message': 'No se pudieron obtener las tasas representativas'})
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()