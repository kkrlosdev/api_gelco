from fastapi import FastAPI
from routers import listas_gi, fichas_tecnicas, ordenes_compra, check_health
from dotenv import load_dotenv
import os

load_dotenv()

local_ip = os.getenv("HOST_IP")

app = FastAPI(
    title="API Gelco",
    description="Endpoints de utilidades de SIESA y Gelcoinfo."
)

@app.get("/", tags=["Root"], summary="Ejecuta diagnóstico de conexión y muestra estado de la API.")
async def main():
    from routers.check_health import check_health
    result = await check_health()
    return {
            "message": f"Servidor corriendo en: http://{local_ip}:8192",
            "ip_local": local_ip,
            "status_environment": result["status_environment"],
            "details": result["details"] if result["status_environment"] != "OK" else []
        }

app.include_router(ordenes_compra.router)
app.include_router(listas_gi.router)
app.include_router(fichas_tecnicas.router)
app.include_router(check_health.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, # En producción cambiar a el objeto app
        host="0.0.0.0",
        port=8000,
        #reload=True       # Solo para desarrollo
    )
