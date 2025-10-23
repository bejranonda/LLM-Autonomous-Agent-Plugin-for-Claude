@echo off
REM Plugin Validation Script for Windows
REM Usage: validate-plugin.bat [options]

setlocal

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    exit /b 1
)

REM Check if plugin validator exists
if not exist "lib\plugin_validator.py" (
    echo ERROR: Plugin validator not found at lib\plugin_validator.py
    echo Please run this script from the plugin root directory
    exit /b 1
)

REM Check if PyYAML is installed
python -c "import yaml" >nul 2>&1
if errorlevel 1 (
    echo Installing PyYAML dependency...
    pip install PyYAML
    if errorlevel 1 (
        echo ERROR: Failed to install PyYAML
        echo Please run: pip install PyYAML
        exit /b 1
    )
)

REM Run validation with all arguments passed to this script
echo.
echo ========================================
echo  Autonomous Agent Plugin Validation
echo ========================================
echo.

python lib\plugin_validator.py %*

REM Check exit code
if errorlevel 2 (
    echo.
    echo Validation FAILED due to errors
    exit /b 2
) else if errorlevel 1 (
    echo.
    echo Validation COMPLETED with issues found
    exit /b 1
) else (
    echo.
    echo Validation PASSED successfully
    exit /b 0
)