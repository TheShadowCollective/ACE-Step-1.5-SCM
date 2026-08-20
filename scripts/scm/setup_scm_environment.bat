@echo off
setlocal

REM ============================================================
REM ACE-Step SCM Environment Setup
REM
REM Purpose:
REM   Build and validate the SCM modernization environment.
REM
REM Current validated target:
REM   Python      3.14.x
REM   PyTorch     2.13.0+cu130
REM   TorchVision 0.28.0+cu130
REM   TorchAudio  2.11.0+cu130
REM   TorchAO     0.18.x
REM   Transformers 5.x
REM
REM This script is intentionally separate from the upstream
REM .venv bootstrap until the SCM stack is fully validated.
REM ============================================================

cd /d "%~dp0..\.."

echo.
echo ========================================
echo ACE-Step SCM Environment Setup
echo ========================================
echo.
echo Project root:
echo %CD%
echo.

if not exist ".venv-scm\Scripts\python.exe" (
    echo [ERROR] .venv-scm was not found.
    echo.
    echo Expected:
    echo   %CD%\.venv-scm\Scripts\python.exe
    echo.
    exit /b 1
)

echo [OK] Found SCM virtual environment.
echo.

".venv-scm\Scripts\python.exe" --version
if errorlevel 1 (
    echo [ERROR] Could not run Python from .venv-scm.
    exit /b 1
)

echo.
echo [OK] SCM Python is available.
echo.

echo.
echo [SCM] Applying TorchAO PyTree Enum compatibility patch...
echo.

".venv-scm\Scripts\python.exe" "scripts\scm\patch_torchao_pytree_enums.py"
if errorlevel 1 (
    echo.
    echo [ERROR] TorchAO compatibility patch failed.
    exit /b 1
)

echo.
echo [OK] TorchAO compatibility patch complete.
echo.

echo.
echo [SCM] Applying vector-quantize meta compatibility patch...
echo.

".venv-scm\Scripts\python.exe" "scripts\scm\patch_vector_quantize_meta.py"
if errorlevel 1 (
    echo.
    echo [ERROR] vector-quantize compatibility patch failed.
    exit /b 1
)

echo.
echo [OK] vector-quantize compatibility patch complete.
echo.

".venv-scm\Scripts\python.exe" "scripts\scm\patch_pytorch_wavelets_resources.py"

if errorlevel 1 (
    echo.
    echo [ERROR] pytorch-wavelets compatibility patch failed.
    exit /b 1
)

echo.
echo [OK] pytorch-wavelets compatibility patch complete.
echo.

endlocal
exit /b 0
