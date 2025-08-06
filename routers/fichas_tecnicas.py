from fastapi import APIRouter
from connection import get_connection_gi
from fastapi.responses import JSONResponse
from utils.fetch_all import fetch_all
from fastapi import HTTPException

router = APIRouter(
    tags=["Fichas técnicas"]
)

@router.get("/fichas_tecnicas", summary="Consulta todas las fichas técnicas y trae su versión más reciente. Datos de viscosidad, bloom y tamaño de grano.")
async def get_ft():
    try:
        conn = get_connection_gi()
        cursor = conn.cursor()

        init_query = """
IF OBJECT_ID('tempdb..#tabla') IS NOT NULL DROP TABLE #tabla;

CREATE TABLE #tabla (
    forCod VARCHAR(100),
    plaNum INT,
    [E37001-V37001] VARCHAR(200),
    [E37001-V01053] VARCHAR(200),
    [E37001-V37003] VARCHAR(200),
    [E37001-V34008] VARCHAR(200),
    [E06024-V37007] VARCHAR(200),
    [E06024-V37008] VARCHAR(200),
    [E06024-V37009] VARCHAR(200),
    [E06095-V37007] VARCHAR(200),
    [E06095-V37008] VARCHAR(200),
    [E06095-V37009] VARCHAR(200),
    [E06086-V37007] VARCHAR(200),
    [E06086-V37008] VARCHAR(200),
    [E06086-V37009] VARCHAR(200)
);

INSERT INTO #tabla
SELECT *
FROM (
    SELECT
        forCod,
        plaNum,
        eleCod + '-' + varCod AS columna_combinada,
        varVal
    FROM [iNova.Progel.iGeneration].dbo.nov_pla_det
    WHERE
        forCod = 'GI-005'
        AND plaFec >= TRY_CAST('2020-01-01' AS DATE)
        AND varCod IN ('V37001', 'V01053', 'V37003', 'V34008', 'V37007', 'V37008', 'V37009')
        AND eleCod IN ('E37001', 'E06095', 'E06086', 'E06024')
        AND adm_ciaId = 3
        AND estCod = 1
) AS src
PIVOT (
    MAX(varVal)
    FOR columna_combinada IN (
        [E37001-V37001], [E37001-V01053], [E37001-V37003], [E37001-V34008],
        [E06024-V37007], [E06024-V37008], [E06024-V37009],
        [E06095-V37007], [E06095-V37008], [E06095-V37009],
        [E06086-V37007], [E06086-V37008], [E06086-V37009]
    )
) AS pvt;
"""
        cursor.execute(init_query)

        select_query = """
SELECT r.*
FROM #tabla r
INNER JOIN (
    SELECT [E37001-V37001], MAX(plaNum) AS max_plaNum
    FROM #tabla
    WHERE [E37001-V37001] IS NOT NULL
    GROUP BY [E37001-V37001]
) AS sub
    ON r.[E37001-V37001] = sub.[E37001-V37001]
    AND r.plaNum = sub.max_plaNum;
    """
        cursor.execute(select_query)
        data = fetch_all(cursor)
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()