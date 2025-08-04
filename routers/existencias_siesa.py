from fastapi import APIRouter
from connection import get_connection_siesa
from fastapi.responses import JSONResponse
from utils.fetch_all import fetch_all

router = APIRouter(
    tags=["Existencias de productos en bodegas de SIESA."]
)

@router.get("/exi_siesa_rpto", summary="Obtiene existencias de repuestos y materiales en bodegas de SIESA, temporalmente bodega general 'AG001' y cuya existencia sea mayor que 0. Sucursal: Barranquilla")
async def get_existencias_siesa():
    try:
        conn = get_connection_siesa()
        c = conn.cursor()

        c.execute("""
    SELECT
        f120_id_cia Empresa, 
        f120_rowid rep_rowid, 
        RTRIM(cast(f120_id as varchar(15))) rep_codi, 
        t120_mc_items.f120_referencia,
        UPPER(RTRIM(SUBSTRING(f120_descripcion, 1, 40))) Descripcion,
        f150_id bod_codi,
        f401_id_ubicacion_aux rep_ubic,
        f120_id_tipo_inv_serv rep_tipr,
        ISNULL(f401_cant_existencia_1, 0) Existencia, 
        (ISNULL(f401_cant_comprometida_1,0) + ISNULL(f401_cant_salida_sin_conf_1, 0)) rep_cres, 
        (ISNULL(f401_cant_existencia_1,0) - (ISNULL(f401_cant_comprometida_1, 0) + ISNULL(f401_cant_salida_sin_conf_1, 0))) rep_cdis,
        f401_rowid_bodega bod_nrid,
        f150_id_co coe_bode,
        f121_id_ext1_detalle rep_ext1,
        f121_id_ext2_detalle rep_ext2
    FROM
        UnoEE_Gelco_Real.dbo.t120_mc_items WITH (NOLOCK)
        LEFT OUTER JOIN UnoEE_Gelco_Real.dbo.t121_mc_items_extensiones WITH (NOLOCK) ON f120_id_cia = f121_id_cia AND f120_rowid = f121_rowid_item
        LEFT OUTER JOIN UnoEE_Gelco_Real.dbo.t401_cm_existencia_lote WITH (NOLOCK) ON f121_id_cia = f401_id_cia AND f121_rowid = f401_rowid_item_ext
        LEFT OUTER JOIN UnoEE_Gelco_Real.dbo.t150_mc_bodegas WITH (NOLOCK) ON f401_id_cia = f150_id_cia AND f401_rowid_bodega = f150_rowid
    WHERE
        f120_id_cia = '1'
        AND f150_id = 'AG001'
        AND f401_cant_existencia_1 > 0
        """)
        data = fetch_all(c)
        if not data:
            return JSONResponse(status_code=204, content=None)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'No se pudo resolver la petición', 'detail': str(e)})
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()