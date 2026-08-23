@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "MYSQL_EXE=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe"

if not exist "%MYSQL_EXE%" (
    for /f "delims=" %%M in ('where mysql 2^>nul') do if not defined MYSQL_EXE_PATH set "MYSQL_EXE_PATH=%%M"
    if defined MYSQL_EXE_PATH set "MYSQL_EXE=%MYSQL_EXE_PATH%"
)

if not exist "%MYSQL_EXE%" (
    echo ERROR: mysql.exe was not found.
    echo Expected location:
    echo %MYSQL_EXE%
    echo.
    echo Your Flask application does not require mysql.exe to be in PATH,
    echo but this setup script needs the MySQL command-line client to import schema.sql.
    pause
    exit /b 1
)

if not exist "database\schema.sql" (
    echo ERROR: database\schema.sql was not found.
    pause
    exit /b 1
)

echo Using MySQL client:
echo %MYSQL_EXE%
echo.
echo Importing database\schema.sql...
echo Enter your MySQL root password when prompted.
echo.

"%MYSQL_EXE%" -u root -p < "database\schema.sql"
set "EXITCODE=%ERRORLEVEL%"

if not "%EXITCODE%"=="0" (
    echo.
    echo ERROR: Database import failed. Exit code: %EXITCODE%
    pause
    exit /b %EXITCODE%
)

echo.
echo Database schema imported successfully.
echo.
echo Verify in MySQL with:
echo   SHOW DATABASES;
echo   USE integrated_cybersecurity;
echo   SHOW TABLES;
echo.
pause
endlocal
