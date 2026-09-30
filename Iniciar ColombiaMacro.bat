@echo off
REM Doble clic para abrir ColombiaMacro en local.
REM Busca un puerto libre (omite 8765 y 8766) y abre el navegador.
REM Opciones: "Iniciar ColombiaMacro.bat" --actualizar   (descarga datos oficiales primero)
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 lanzar_local.py %*
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        python lanzar_local.py %*
    ) else (
        echo No se encontro Python. Instale Python 3.10+ desde https://www.python.org/downloads/
        echo y marque "Add python.exe to PATH" durante la instalacion.
    )
)
pause
