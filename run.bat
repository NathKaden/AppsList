@echo off
:: Se positionner dans le dossier du script bat
cd /d "%~dp0"

:: Verification de la presence de Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Erreur : Python n est pas trouve ou n est pas configure dans le PATH.
    pause
    exit /b 1
)

:: Creation du venv si inexistant
if not exist .venv (
    echo [1/2] Creation de l environnement virtuel venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo Erreur lors de la creation du venv.
        pause
        exit /b 1
    )
)

:: Installation des dependances si PyQt6 n est pas installe
if not exist ".venv\Lib\site-packages\PyQt6" (
    echo [2/2] Installation des dependances...
    .venv\Scripts\pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Erreur lors de l installation des dependances.
        pause
        exit /b 1
    )
)

echo Lancement de AppsList...
.venv\Scripts\python main.py
