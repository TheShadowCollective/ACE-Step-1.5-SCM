@echo off
setlocal

if not defined SCM_VENV set "SCM_VENV=.venv-scm"

REM ============================================================
REM ACE-Step SCM Environment Bootstrap
REM
REM Creates the validated SCM virtual environment:
REM   .venv-scm
REM
REM Validated baseline:
REM   Python 3.14.x
REM   Torch 2.13.0 + CUDA 13.0
REM   Transformers 5.15.1
REM ============================================================

cd /d "%~dp0\..\.."

echo.
echo ========================================
echo ACE-Step SCM Environment Bootstrap
echo ========================================
echo.
echo Project root:
echo   %CD%
echo.

REM ------------------------------------------------------------
REM Locate validated Python 3.14 interpreter
REM ------------------------------------------------------------

py -3.14 --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python 3.14 was not found by the Windows Python launcher.
    echo.
    echo Install Python 3.14 x64 and make sure the "py" launcher is available.
    exit /b 1
)

for /f "tokens=2" %%V in ('py -3.14 --version 2^>^&1') do set PYTHON_VERSION=%%V

echo Detected validated Python:
echo   %PYTHON_VERSION%
echo.

echo %PYTHON_VERSION% | findstr /B "3.14." >nul
if errorlevel 1 (
    echo [ERROR] Python launcher did not return a Python 3.14 interpreter.
    exit /b 1
)

echo [OK] Python 3.14.x detected.
echo.

REM ------------------------------------------------------------
REM Create SCM virtual environment if needed
REM ------------------------------------------------------------

if exist "%SCM_VENV%\Scripts\python.exe" (
    echo [OK] Existing %SCM_VENV% found.
) else (
    echo Creating %SCM_VENV%...
    py -3.14 -m venv "%SCM_VENV%"

    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to create %SCM_VENV%.
        exit /b 1
    )

    echo [OK] Created %SCM_VENV%.
)

echo.
"%SCM_VENV%\Scripts\python.exe" --version
if errorlevel 1 (
    echo.
    echo [ERROR] Could not run Python from %SCM_VENV%.
    exit /b 1
)

echo.
echo [OK] SCM virtual environment is ready.
echo.

REM ------------------------------------------------------------
REM Upgrade packaging tools
REM ------------------------------------------------------------

echo.
echo ========================================
echo Upgrading packaging tools
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to upgrade pip/setuptools/wheel.
    exit /b 1
)

echo.
echo [OK] Packaging tools are ready.
echo.

REM ------------------------------------------------------------
REM Install validated PyTorch CUDA 13 stack
REM ------------------------------------------------------------

echo.
echo ========================================
echo Installing PyTorch CUDA 13 stack
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -m pip install ^
    --index-url https://download.pytorch.org/whl/cu130 ^
    torch==2.13.0+cu130 ^
    torchvision==0.28.0+cu130 ^
    torchaudio==2.11.0+cu130

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install validated PyTorch CUDA 13 stack.
    exit /b 1
)

echo.
echo [OK] PyTorch CUDA 13 stack installed.
echo.

REM ------------------------------------------------------------
REM Install validated SCM inference stack
REM ------------------------------------------------------------

echo.
echo ========================================
echo Installing validated SCM inference stack
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -m pip install ^
    transformers==5.15.1 ^
    diffusers==0.39.0 ^
    accelerate==1.14.0 ^
    safetensors==0.8.0 ^
    torchao==0.18.0 ^
    vector-quantize-pytorch==1.31.1 ^
    pytorch-wavelets==1.3.0 ^
    PyWavelets==1.9.0

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install validated SCM inference stack.
    exit /b 1
)

echo.
echo [OK] Validated SCM inference stack installed.
echo.

REM ------------------------------------------------------------
REM Install local nano-vllm
REM ------------------------------------------------------------

echo.
echo ========================================
echo Installing local nano-vllm
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -m pip install -e "acestep\third_parts\nano-vllm"

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install local nano-vllm.
    exit /b 1
)

echo.
echo [OK] Local nano-vllm installed.
echo.

REM ------------------------------------------------------------
REM Install ACE-Step from local clone
REM ------------------------------------------------------------

echo.
echo ========================================
echo Installing local ACE-Step
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -m pip install -e .

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install local ACE-Step.
    exit /b 1
)

echo.
echo [OK] Local ACE-Step installed.
echo.

REM ------------------------------------------------------------
REM Apply validated SCM compatibility patches
REM ------------------------------------------------------------

echo.
echo ========================================
echo Applying SCM compatibility patches
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" "scripts\scm\patch_torchao_pytree_enums.py"

if errorlevel 1 (
    echo.
    echo [ERROR] TorchAO compatibility patch failed.
    exit /b 1
)

"%SCM_VENV%\Scripts\python.exe" "scripts\scm\patch_vector_quantize_meta.py"

if errorlevel 1 (
    echo.
    echo [ERROR] vector-quantize compatibility patch failed.
    exit /b 1
)

echo.
echo [OK] SCM compatibility patches applied.
echo.

"%SCM_VENV%\Scripts\python.exe" "scripts\scm\patch_pytorch_wavelets_resources.py"

if errorlevel 1 (
    echo.
    echo [ERROR] pytorch-wavelets compatibility patch failed.
    exit /b 1
)

echo.
echo [OK] pytorch-wavelets compatibility patch complete.
echo.

REM ------------------------------------------------------------
REM Validate installed SCM stack
REM ------------------------------------------------------------

echo.
echo ========================================
echo Validating SCM environment
echo ========================================
echo.

"%SCM_VENV%\Scripts\python.exe" -c "import torch, transformers, diffusers, torchao, accelerate, safetensors, importlib.metadata as md; print('Python stack OK'); print('torch:', torch.__version__); print('CUDA:', torch.version.cuda); print('GPU available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NONE'); print('transformers:', transformers.__version__); print('diffusers:', diffusers.__version__); print('torchao:', torchao.__version__); print('vector-quantize-pytorch:', md.version('vector-quantize-pytorch')); print('accelerate:', accelerate.__version__); print('safetensors:', safetensors.__version__)"

if errorlevel 1 (
    echo.
    echo [ERROR] SCM environment validation failed.
    exit /b 1
)

echo.
echo ========================================
echo SCM bootstrap completed successfully
echo ========================================
echo.
echo Environment:
echo   %CD%\%SCM_VENV%
echo.

endlocal
exit /b 0
