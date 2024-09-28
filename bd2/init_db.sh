#!/bin/bash
# Esperar a que SQL Server esté listo
sleep 20
# Restaurar la base de datos desde el archivo .bak
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "YourStrong@Passw0rd" -Q "RESTORE DATABASE MovieLens FROM DISK = '/var/opt/mssql/backup/MovieLens.bak' WITH MOVE 'MovieLens' TO '/var/opt/mssql/data/MovieLens.mdf', MOVE 'MovieLens_log' TO '/var/opt/mssql/data/MovieLens_log.ldf'"
