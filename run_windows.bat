@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo ================================================================
echo Integrated Cybersecurity System
echo ================================================================

if not exist ".venv\Scripts\python.exe" (
    echo ERROR: .venv was not found.
    echo Run setup_windows.bat first.
    pause
    exit /b 1
)

if not exist ".env" (
    echo ERROR: .env was not found.
    echo Create it from .env.example and configure MySQL first.
    pause
    exit /b 1
)

echo Starting server...
echo Open http://127.0.0.1:5000 in your browser.
echo DO NOT close this window while using the application.
echo.

.venv\Scripts\python.exe server.py
set "EXITCODE=%ERRORLEVEL%"

echo.
echo ================================================================
echo Server process ended. Exit code: %EXITCODE%
echo ================================================================
echo.
echo If you did NOT press CTRL+C, copy the messages above and send them
echo to your project developer/tutor before trying anything else.
echo.
pause
endlocal
exit /b %EXITCODE%
