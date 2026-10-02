@echo off
setlocal
title Food Freshness Prediction System - Web Application

echo ======================================================================
echo Starting Food Freshness Prediction Web Dashboard on localhost...
echo ======================================================================

:: Change directory to project root
cd /d "%~dp0\.."

:: Check and activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment 'venv' not found. Using system Python...
)

:: Set host to localhost explicitly
set WEB_HOST=127.0.0.1
set WEB_PORT=7860
set GRADIO_SERVER_NAME=127.0.0.1
set GRADIO_SERVER_PORT=7860

echo.
echo [INFO] Web Application URL: http://localhost:%WEB_PORT%
echo.

python -m src.app.app

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Web application failed to start or exited with an error.
    pause
)
