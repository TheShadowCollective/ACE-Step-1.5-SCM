@echo off
setlocal

REM ============================================================
REM ACE-Step SCM API Server Launcher
REM
REM Uses the validated SCM environment:
REM   .venv-scm
REM
REM Flow:
REM   1. Locate ACE-Step project root
REM   2. Verify / patch SCM environment
REM   3. Launch acestep-api using .venv-scm explicitly
REM ============================================================

cd /d "%~dp0..\.."

echo.
echo ========================================
echo ACE-Step SCM API Server
echo ========================================
echo.
echo Project root:
echo %CD%
echo.

REM ------------------------------------------------------------
REM Verify SCM virtual environment
REM ------------------------------------------------------------

if not exist ".venv-scm\Scripts\python.exe" (
    echo [ERROR] SCM virtual environment not found.
    echo.
    echo Expected:
    echo   %CD%\.venv-scm\Scripts\python.exe
    echo.
    exit /b 1
)

echo [OK] Found .venv-scm
".venv-scm\Scripts\python.exe" --version
echo.

REM ------------------------------------------------------------
REM Apply validated SCM compatibility patches
REM ------------------------------------------------------------

call "scripts\scm\setup_scm_environment.bat"
if errorlevel 1 (
    echo.
    echo [ERROR] SCM environment setup failed.
    exit /b 1
)

REM ------------------------------------------------------------
REM API configuration
REM ------------------------------------------------------------

set HOST=127.0.0.1
set PORT=8001

echo.
echo ========================================
echo Starting ACE-Step SCM API
echo ========================================
echo API:
echo   http://%HOST%:%PORT%
echo.
echo Docs:
echo   http://%HOST%:%PORT%/docs
echo.
echo Environment:
echo   %CD%\.venv-scm
echo.

REM ------------------------------------------------------------
REM Launch API using the SCM Python environment explicitly
REM ------------------------------------------------------------

if not defined ACESTEP_CONFIG_PATH set "ACESTEP_CONFIG_PATH=acestep-v15-turbo"
if not defined ACESTEP_LM_MODEL_PATH set "ACESTEP_LM_MODEL_PATH=acestep-5Hz-lm-1.7B"

".venv-scm\Scripts\acestep-api.exe" ^
    --host %HOST% ^
    --port %PORT% ^
    --lm-model-path %ACESTEP_LM_MODEL_PATH%

set EXIT_CODE=%ERRORLEVEL%

echo.
echo ACE-Step SCM API exited with code %EXIT_CODE%.
echo.

endlocal
exit /b %EXIT_CODE%
