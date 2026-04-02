@echo off
chcp 65001 > nul
title Furniture NER Extractor
echo ========================================
echo   Furniture NER Extractor
echo ========================================
echo.
echo 1 - Run main.py (single URL)
echo 2 - Run database_builder.py (CSV to DB)
echo 3 - Run web_app.py (Web interface)
echo.
set /p choice="Select (1-3): "

if "%choice%"=="1" (
    python scripts/main.py
) else if "%choice%"=="2" (
    python scripts/database_builder.py
) else if "%choice%"=="3" (
    python scripts/web_app.py
) else (
    echo Invalid choice
    pause
)