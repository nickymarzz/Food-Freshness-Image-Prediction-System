@echo off
setlocal
title Food Freshness Prediction System - FastAPI Backend

echo ======================================================================
echo Starting Food Freshness FastAPI REST API on localhost...
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
set API_HOST=127.0.0.1
set API_PORT=8000

echo.
echo [INFO] API Endpoint: http://localhost:%API_PORT%
echo [INFO] OpenAPI Docs: http://localhost:%API_PORT%/docs
echo [INFO] Health Check: http://localhost:%API_PORT%/health
echo.

python -m uvicorn src.api.main:app --host %API_HOST% --port %API_PORT% --reload

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] API failed to start or exited with an error.
    pause
)
