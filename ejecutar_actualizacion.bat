@echo off
echo ========================================
echo    ACTUALIZACION AUTOMATICA - ARCA
echo ========================================
echo.
echo Servidor: 138.197.17.131
echo.

REM Verificar si PuTTY está instalado
where pscp >nul 2>nul
if %errorlevel% neq 0 (
    echo ERROR: PuTTY no esta instalado
    echo Descargar desde: https://www.putty.org/
    pause
    exit /b 1
)

echo [1/4] Subiendo script de actualizacion...
pscp -P 22 actualizar_servidor_automatico.sh root@138.197.17.131:/tmp/

if %errorlevel% neq 0 (
    echo ERROR: No se pudo subir el archivo
    pause
    exit /b 1
)

echo [2/4] Conectando al servidor...
echo.
echo INSTRUCCIONES:
echo 1. Se abrira una ventana de SSH
echo 2. Ejecuta estos comandos:
echo.
echo    cd /tmp
echo    chmod +x actualizar_servidor_automatico.sh
echo    ./actualizar_servidor_automatico.sh
echo.
echo 3. Espera a que termine la actualizacion
echo 4. Cierra la ventana cuando termine
echo.
pause

echo [3/4] Abriendo conexion SSH...
putty -ssh root@138.197.17.131

echo [4/4] Actualizacion completada!
echo.
echo Verificar en: https://construccionesarca.net
echo.
pause







