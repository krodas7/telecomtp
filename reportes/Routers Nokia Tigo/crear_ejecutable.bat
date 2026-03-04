@echo off
echo ============================================================
echo   GENERADOR DE EJECUTABLE - Exportador Reportes Routers
echo ============================================================
echo.

echo [1/4] Instalando PyInstaller...
pip install pyinstaller
echo.

echo [2/4] Limpiando compilaciones anteriores...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del /q *.spec
echo.

echo [3/4] Generando ejecutable...
pyinstaller --onefile ^
    --windowed ^
    --name="ExportadorRoutersNokia" ^
    --icon=NONE ^
    --add-data="plantillas;plantillas" ^
    --add-data="firebase_config.py;." ^
    --add-data="firebase-credentials.json;." ^
    --hidden-import=firebase_admin ^
    --hidden-import=reportlab ^
    --hidden-import=PIL ^
    exportador_gui.py

echo.
echo [4/4] Verificando resultado...
if exist "dist\ExportadorRoutersNokia.exe" (
    echo.
    echo ============================================================
    echo   EXITO! El ejecutable se creo correctamente
    echo ============================================================
    echo.
    echo Ubicacion: dist\ExportadorRoutersNokia.exe
    echo.
    echo IMPORTANTE: Copia la carpeta 'plantillas' junto al .exe
    echo.
) else (
    echo.
    echo ============================================================
    echo   ERROR: No se pudo crear el ejecutable
    echo ============================================================
    echo.
)

pause










