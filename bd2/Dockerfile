# Usa la imagen oficial de SQL Server
FROM mcr.microsoft.com/mssql/server:2022-latest

# Establece las variables de entorno para aceptar la licencia y la contraseña de SA
ENV ACCEPT_EULA=Y
ENV MSSQL_SA_PASSWORD=YourStrong@Passw0rd

# Cambia al usuario root para instalar los paquetes necesarios
USER root

# Actualiza los paquetes dentro del contenedor
RUN apt-get update && apt-get install -y \
    mssql-tools \
    unixodbc-dev \
    wget && \
    rm -rf /var/lib/apt/lists/*

# Crea la carpeta de backup en el contenedor
RUN mkdir -p /var/opt/mssql/backup

# Descarga el archivo .bak desde GitHub
RUN wget https://github.com/nealsteve95/backupMovieLens/raw/main/MovieLens.bak -O /var/opt/mssql/backup/MovieLens.bak

# Cambia de nuevo al usuario mssql
USER mssql

# Expone el puerto 1433 (puerto de SQL Server)
EXPOSE 1433

# Comando de inicio para el contenedor
CMD /opt/mssql/bin/sqlservr
