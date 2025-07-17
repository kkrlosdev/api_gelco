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

### 🔧 Variables de entorno requeridas

| Variable      | Descripción                                                             |
|---------------|--------------------------------------------------------------------------|
| `USER`        | Usuario de la base de datos principal                                    |
| `PASSWORD`    | Contraseña del usuario de la base de datos                               |
| `SERVER`      | IP del servidor SQL de SIESA                                             |
| `SERVER_GI`   | IP del servidor SQL de Gelcoinfo                                         |
| `DATABASE`    | Nombre de la base de datos de SIESA                                      |
| `DATABASE_GI` | Nombre de la base de datos de Gelcoinfo                                  |
| `HOST_IP`     | IP del host (fuera del contenedor) accesible desde el contenedor Docker |
