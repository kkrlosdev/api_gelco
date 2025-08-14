from fastapi import APIRouter
from db.connection import get_connection_siesa
from fastapi import HTTPException
from utils.fetch_all import fetch_all
from fastapi.responses import JSONResponse

router = APIRouter(
    tags=["Ordenes de compra provenientes de SIESA"]
)

@router.get("/ordenes_compra", summary="Consulta todas las ordenes de compra de tipo OCM, OCA, OCQ, OCN de la cantidad de días atrás solicitada (por defecto, 30) y retorna información relevante.")
async def get_ordenes_compra(dias_atras: int = 30):
    try:
        conn = get_connection_siesa()
        cursor = conn.cursor()

        cursor.execute("""
SELECT
    J.f200_razon_social AS 'descripcion_solicitante',
    ES.f420_consec_docto AS 'numero_solicitud',
    EC.f420_consec_docto AS 'numero_orden',
    EC.f420_id_tipo_docto AS 'tipo_documento',
    EC.f420_fecha AS 'fecha_orden',
    G.F054_DESCRIPCION AS 'estado_documento',
    I.f120_referencia AS 'referencia',
    I.f120_descripcion AS 'descripcion',
    DC.f421_id_unidad_medida AS 'unidad_medida',
    TRY_CAST(DC.f421_cant_pedida AS DECIMAL(10,2)) AS 'cantidad_ordenada',
    EC.f420_id_moneda_docto AS 'moneda',
    DC.f421_precio_unitario AS 'precio_unitario',
    DC.f421_vlr_bruto AS 'valor_bruto',
    DC.f421_vlr_imp AS 'valor_impuestos',
    DC.f421_vlr_neto AS 'valor_neto',
    D.f284_descripcion AS 'centro_de_costo',
    EC.f420_notas AS 'motivo',
    E.F107_DESCRIPCION AS 'descripcion_proyecto',
    F.f200_razon_social AS 'razon_social',
    DC.f421_hora_entrega AS 'fecha_real_de_entrada',
    DC.f421_fecha_entrega AS 'fecha_entrega'
FROM
    UnoEE_Gelco_Real.dbo.t420_cm_oc_docto ES
    JOIN UnoEE_Gelco_Real.dbo.t421_cm_oc_movto DS
        ON ES.f420_id_cia = DS.f421_id_cia
		AND DS.f421_rowid_oc_docto = ES.f420_rowid

    JOIN UnoEE_Gelco_Real.dbo.t421_cm_oc_movto DC
        ON DS.f421_id_cia = DC.f421_id_cia
		AND DS.f421_rowid = DC.f421_rowid_oc_movto

    JOIN UnoEE_Gelco_Real.dbo.t420_cm_oc_docto EC
        ON EC.f420_id_cia = DC.f421_id_cia
		AND DC.f421_rowid_oc_docto = EC.f420_rowid

    LEFT JOIN t200_mm_terceros J 
        ON ISNULL(ES.f420_rowid_tercero_solicit, EC.f420_rowid_tercero_solicit) = J.f200_rowid

    LEFT JOIN t284_co_ccosto D 
        ON DC.f421_rowid_ccosto_movto = D.f284_rowid

    LEFT JOIN T107_MC_PROYECTOS E 
        ON DC.f421_id_proyecto = E.F107_ID

    LEFT JOIN t200_mm_terceros F 
        ON EC.f420_rowid_tercero_prov = F.f200_rowid

    LEFT JOIN T054_MM_ESTADOS G 
        ON EC.f420_ind_estado = G.F054_ID 
		AND EC.f420_id_grupo_clase_docto = G.F054_ID_GRUPO_CLASE_DOCTO

    LEFT JOIN T121_MC_ITEMS_EXTENSIONES H 
        ON H.f121_rowid = DC.f421_rowid_item_ext
    LEFT JOIN t120_mc_items I 
        ON H.f121_rowid_item = I.f120_rowid
WHERE
    EC.f420_id_tipo_docto IN ('OCN', 'OCM', 'OCA', 'OCQ')
    AND TRY_CAST(EC.f420_fecha_ts_creacion AS DATE) >= GETDATE() - ?
    AND EC.f420_id_cia = 1
ORDER BY
    EC.f420_fecha_ts_creacion DESC;
""", (dias_atras,))
    
        data = fetch_all(cursor)
        return JSONResponse(content=data, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()