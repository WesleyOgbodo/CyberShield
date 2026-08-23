@echo off
setlocal
cd /d "%~dp0"

echo Checking Python...
.venv\Scripts\python.exe --version
if errorlevel 1 goto fail

echo.
echo Checking PyMySQL import...
.venv\Scripts\python.exe -c "import pymysql; print('PyMySQL import: OK')"
if errorlevel 1 goto fail

echo.
echo Checking Flask import...
.venv\Scripts\python.exe -c "from app import app; print('Flask application import: OK')"
if errorlevel 1 goto fail

echo.
echo All application-level checks passed.
pause
exit /b 0

:fail
echo.
echo A diagnostic check failed.
pause
exit /b 1
