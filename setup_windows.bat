@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found. Install Python 3.11+ and ensure it is on PATH.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating .venv...
    python -m venv .venv
    if errorlevel 1 goto fail
)

echo Installing project dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 goto fail
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto fail

if not exist ".env" (
    copy /Y ".env.example" ".env" >nul
    echo Created .env from .env.example.
    echo Edit .env and enter your MySQL password before starting the app.
)

echo.
echo Setup complete.
echo Next: run setup_database_windows.bat, then run_windows.bat.
pause
exit /b 0

:fail
echo.
echo Setup failed.
pause
exit /b 1
