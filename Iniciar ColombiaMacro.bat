@echo off
REM Doble clic para abrir ColombiaMacro en este computador.
REM Busca un puerto libre (omite 8765, 8766 y los ocupados) y abre el navegador.
REM Para descargar datos oficiales antes de abrir: "Iniciar ColombiaMacro.bat" --actualizar
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 scripts\lanzar_local.py %*
    goto :fin
)
where python >nul 2>nul
if %errorlevel%==0 (
    python scripts\lanzar_local.py %*
    goto :fin
)
echo No se encontro Python. Instale Python 3.10 o superior desde https://www.python.org/downloads/
echo y marque "Add python.exe to PATH" durante la instalacion.
:fin
pause
