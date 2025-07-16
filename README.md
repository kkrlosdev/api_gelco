# API Gelcoinfo

## DOCUMENTACIÓN AUTOMÁTICA

Ir a [`/docs`](http://localhost:8192/docs) para acceder a la documentación Swagger UI generada automáticamente por FastAPI.

---

## Endpoints disponibles

### `GET /check_health`
Verifica el estado de conexión, componentes y funcionamiento general de la API.

### `GET /fichas_tecnicas`
Consulta bloom, viscosidad y tamaño de grano de todas las fichas técnicas en su versión más reciente.

### `GET /ordenes_compra`
Retorna todas las órdenes de compra del sistema SIESA con tipo OCM, OCA, OCQ y OCN, generadas en los últimos 30 días, retorna la información relevante.

### `GET /listas/lista={genCod}`
Ejecuta dinámicamente el código de una lista proveniente de Gelcoinfo y retorna su resultado.

---
## 🐳 Docker

Para levantar la API con Docker Compose:

```bash
docker compose up --build -d
```
