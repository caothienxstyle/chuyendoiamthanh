@echo off
title Whisper Audio To Text
cd /d "%~dp0"

echo ==========================================
echo       WHISPER AUDIO TO TEXT
echo ==========================================
echo.

if not exist ".venv\Scripts\python.exe" (
    echo [1/2] Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo Cannot create Python virtual environment.
        echo Make sure Python 3 is installed.
        pause
        exit /b 1
    )
)

echo [2/2] Installing/checking packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo.
echo Starting Whisper...
echo Open http://127.0.0.1:5000 in your browser.
echo Close this window to stop the program.
echo.

".venv\Scripts\python.exe" app.py

pause
