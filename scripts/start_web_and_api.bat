@echo off
setlocal
title Food Freshness Prediction System - Dual Launcher

echo ======================================================================
echo Launching Food Freshness Services (API + Web Dashboard)...
echo ======================================================================

cd /d "%~dp0\.."

echo.
echo [1/2] Spawning FastAPI REST API in a new window (http://localhost:8000)...
start "Food Freshness API (localhost:8000)" cmd /k "%~dp0start_api.bat"

:: Brief delay to allow API to initialize
timeout /t 2 /nobreak >nul

echo [2/2] Spawning Gradio Web Dashboard in a new window (http://localhost:7860)...
start "Food Freshness Web Dashboard (localhost:7860)" cmd /k "%~dp0start_web.bat"

echo.
echo ======================================================================
echo Both services have been launched!
echo - Web Dashboard: http://localhost:7860
echo - FastAPI REST:  http://localhost:8000
echo - API Docs:      http://localhost:8000/docs
echo ======================================================================
echo.
