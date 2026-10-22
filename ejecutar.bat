@echo off
cd /d "%~dp0"
echo ========================================================
echo  Iniciando Lanzador Central de Tkinter en Python...
echo ========================================================
python launcher.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar. Presiona cualquier tecla para salir.
    pause
)
