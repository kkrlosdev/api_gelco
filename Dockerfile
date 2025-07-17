FROM python:3.12-slim

# 1. Instalar utilidades básicas y dependencias
RUN apt-get update && apt-get install -y \
    curl gnupg2 apt-transport-https software-properties-common iputils-ping \
    gcc g++ unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Agregar la clave pública de Microsoft correctamente
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /usr/share/keyrings/microsoft.gpg

# 3. Agregar el repositorio de Microsoft con la key GPG segura
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
    > /etc/apt/sources.list.d/mssql-release.list

# 4. Instalar el driver ODBC
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# 5. Actualizar pip
RUN pip install --upgrade pip

# 6. Set working dir
WORKDIR /api_gelco

# 7. Copiar y preparar la app
COPY . /api_gelco

# 8. Instalar requerimientos
RUN pip install --no-cache-dir -r requirements.txt

# 9. Ejecutar la API en modo producción
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--loop", "uvloop"]
