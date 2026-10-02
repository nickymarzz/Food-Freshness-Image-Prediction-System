@echo off
setlocal
title Food Freshness Prediction System - Training Pipeline

echo ======================================================================
echo Food Freshness Prediction System - End-to-End Training Pipeline
echo ======================================================================

cd /d "%~dp0\.."

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] Virtual environment 'venv' not found. Using system Python...
)

echo.
echo [INFO] Starting training pipeline execution:
echo        1. Data Ingestion & Integrity Validation
echo        2. Data Transformation & Seeded Stratified Splitting
echo        3. Freshness Baseline Model Training (MobileNetV2)
echo        4. Produce Category Taxonomy Classifier Training
echo        5. Freshness Quantitative Evaluation & ROC Curves
echo        6. Category Taxonomy Evaluation & Error Analysis
echo.

python -m src.pipeline.training_pipeline

if %ERRORLEVEL% equ 0 (
    echo.
    echo ======================================================================
    echo [SUCCESS] Training pipeline completed successfully!
    echo Models saved to:    artifacts\models\
    echo Results saved to:   artifacts\results\
    echo ======================================================================
) else (
    echo.
    echo [ERROR] Training pipeline encountered an error (Code: %ERRORLEVEL%).
)

echo.
pause
