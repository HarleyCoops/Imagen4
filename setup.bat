@echo off
REM Imagen4 Setup Script for Windows

echo ======================================================
echo           Imagen4 CLI Setup Helper Script
echo ======================================================

REM Check if Python is installed
echo.
echo Checking Python installation...
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python not found. Please install Python 3.7 or higher.
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%V in ('python -c "import sys; print(sys.version.split()[0])"') do set PYTHON_VERSION=%%V
for /f "tokens=1,2 delims=." %%a in ("%PYTHON_VERSION%") do (
    set PYTHON_MAJOR=%%a
    set PYTHON_MINOR=%%b
)

if %PYTHON_MAJOR% LSS 3 (
    echo Python 3.7 or higher is required. Found: %PYTHON_VERSION%
    exit /b 1
) else (
    if %PYTHON_MAJOR% EQU 3 (
        if %PYTHON_MINOR% LSS 7 (
            echo Python 3.7 or higher is required. Found: %PYTHON_VERSION%
            exit /b 1
        )
    )
)

echo Python %PYTHON_VERSION% found.

REM Check if gcloud is installed
echo.
echo Checking Google Cloud SDK installation...
where gcloud >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Google Cloud SDK (gcloud) not found.
    echo Please install the Google Cloud SDK from: https://cloud.google.com/sdk/docs/install
    exit /b 1
)

echo Google Cloud SDK found.

REM Check if virtual environment should be created
echo.
set /p CREATE_VENV=Do you want to create a virtual environment? (recommended) [Y/n]: 
if not defined CREATE_VENV set CREATE_VENV=Y

if /i "%CREATE_VENV%"=="Y" (
    echo.
    echo Creating virtual environment...
    
    REM Check if venv module is available
    python -c "import venv" >nul 2>&1
    if %ERRORLEVEL% neq 0 (
        echo Python venv module not found. Please install it first.
        exit /b 1
    )
    
    REM Create and activate virtual environment
    python -m venv venv
    
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
        echo Virtual environment created and activated.
    ) else (
        echo Failed to create virtual environment.
        exit /b 1
    )
)

REM Run the Python setup script
echo.
echo Running setup script...
python setup.py

REM Check if setup was successful
if %ERRORLEVEL% equ 0 (
    echo.
    echo Setup completed successfully!
    
    REM Load environment variables from .env file if it exists
    if exist ".env" (
        echo.
        echo Loading environment variables from .env file...
        for /f "tokens=*" %%a in (.env) do set %%a
        echo Environment variables loaded.
    )
    
    echo.
    echo You can now run the Imagen4 CLI:
    echo python imagen4_cli.py --prompt "Your creative prompt here"
) else (
    echo.
    echo Setup failed. Please check the error messages above.
    exit /b 1
)

echo.
pause

