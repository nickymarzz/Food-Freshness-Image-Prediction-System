@echo off
setlocal
title Food Freshness Prediction System - Docker Setup

echo ======================================================================
echo Food Freshness Prediction System - Docker Setup & Launch
echo ======================================================================

cd /d "%~dp0\.."

:: Verify Docker is running
echo.
echo [1/4] Checking Docker daemon status...
docker info >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker is not running or not found in PATH.
    echo Please start Docker Desktop and run this script again.
    echo.
    pause
    exit /b 1
)
echo [OK] Docker daemon is running.

:: Stop existing container if present
echo.
echo [2/4] Removing existing 'freshness-app' container (if any)...
docker stop freshness-app >nul 2>&1
docker rm freshness-app >nul 2>&1

:: Build Docker image
echo.
echo [3/4] Building Docker image 'food-freshness-system:latest'...
docker build -t food-freshness-system:latest .

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Docker build failed.
    pause
    exit /b %ERRORLEVEL%
)

:: Run container mapped to localhost:7860
echo.
echo [4/4] Starting container 'freshness-app' on port 7860...
docker run -d -p 7860:7860 --name freshness-app food-freshness-system:latest

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Container 'freshness-app' is running!
    echo Access the Web Application at: http://localhost:7860
    echo.
    echo Useful Docker commands:
    echo   View logs:   docker logs -f freshness-app
    echo   Stop app:    docker stop freshness-app
    echo ======================================================================
) else (
    echo.
    echo [ERROR] Failed to start Docker container.
)

echo.
pause
