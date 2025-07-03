from fastapi import FastAPI, HTTPException
from utils import fetch_all
from connection import get_connection_siesa, get_connection_gi
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.get("/")
async def main():
    return {"message": "Servidor corriendo en: http://127.0.0.1:8000"}

@app.get("/ordenes_compra")
async def get_ordenes_compra():
    try:
        conn = get_connection_siesa()
        c = conn.cursor()

        c.execute("""
SELECT
	A.f420_usuario_creacion AS 'descripcion_solicitante',
	A.f420_consec_docto AS 'numero_solicitud',
	A.f420_id_tipo_docto AS 'tipo_documento',
	A.f420_consec_docto AS 'numero_orden',
	A.f420_fecha AS 'fecha_orden',
	G.F054_DESCRIPCION AS 'estado_documento',
	C.f120_referencia AS 'referencia',
	C.f120_descripcion AS 'descripcion',
	B.f421_id_unidad_medida AS 'unidad_medida',
	TRY_CAST(B.f421_cant_pedida AS DECIMAL(10,2)) AS 'cantidad_ordenada',
	A.f420_id_moneda_docto AS 'moneda',
	B.f421_precio_unitario AS 'precio_unitario',
	B.f421_vlr_bruto AS 'valor_bruto',
	B.f421_vlr_imp AS 'valor_impuestos',
	B.f421_vlr_neto AS 'valor_neto',
	D.f284_descripcion AS 'centro_de_costo',
	A.f420_notas AS 'motivo',
	E.F107_DESCRIPCION AS 'descripcion_proyecto',
	F.f200_razon_social AS 'razon_social',
	B.f421_hora_entrega AS 'fecha_real_de_entrada',
	B.f421_fecha_entrega AS 'fecha_entrega'
FROM
	UnoEE_Gelco_Real.dbo.t420_cm_oc_docto A
	LEFT JOIN UnoEE_Gelco_Real.dbo.t421_cm_oc_movto B ON A.f420_rowid = B.f421_rowid_oc_docto
	LEFT JOIN t120_mc_items C ON B.f421_rowid_item_ext = C.f120_rowid
	LEFT JOIN t284_co_ccosto D ON B.f421_rowid_ccosto_movto = D.f284_rowid
	LEFT JOIN T107_MC_PROYECTOS E ON B.f421_id_proyecto = E.F107_ID
	LEFT JOIN t200_mm_terceros F ON A.f420_rowid_tercero_prov = F.f200_rowid
	LEFT JOIN T054_MM_ESTADOS G ON A.f420_ind_estado = G.F054_ID AND A.f420_id_grupo_clase_docto = G.F054_ID_GRUPO_CLASE_DOCTO
WHERE
	A.f420_id_tipo_docto IN ('OCN', 'OCM', 'OCA', 'OCQ')
    AND TRY_CAST(A.f420_fecha_ts_creacion AS DATE) >= GETDATE() - 30
ORDER BY
	A.f420_fecha_ts_creacion DESC
""")
    
        data = fetch_all(c)
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        c.close()
        conn.close()

@app.get("/fichas_tecnicas")
async def get_ft():
    try:
        conn = get_connection_gi()
        cursor = conn.cursor()

        query = """
        DECLARE @json NVARCHAR(MAX)
        SET @json = (
            SELECT
                *
            FROM (
                SELECT
                    forCod,
                    plaNum,
                    eleCod,
                    varCod,
                    varVal
                FROM
                    [iNova.Progel.iGeneration].dbo.nov_pla_det
                WHERE
                    forCod = 'GI-005'
                    AND plaFec >= TRY_CAST('2020-01-01' AS DATE)
                    AND varCod IN ('V37001', 'V01053', 'V34008', 'V37007', 'V37008', 'V37009')
                    AND eleCod IN ('E37001', 'E06095', 'E06086', 'E06024')
                    AND adm_ciaId = 3
                    AND estCod = 1
            ) AS src
            PIVOT (
                MAX(varVal)
                FOR varCod IN ([V37001], [V01053], [V34008], [V37007], [V37008], [V37009])
            ) AS pvt
            ORDER BY plaNum
            FOR JSON AUTO
        )
        SELECT @json AS output
        """

        cursor.execute(query)
        row = cursor.fetchone()
        data = json.loads(row[0])
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True       # Solo para desarrollo
    )
