@echo off
echo ========================================
echo    CONFIGURACION DE GIT PARA ARCA
echo ========================================
echo.

echo Verificando instalacion de Git...
git --version
if %errorlevel% neq 0 (
    echo ERROR: Git no esta instalado o no esta en el PATH
    echo Por favor, reinicia la terminal y ejecuta este script nuevamente
    pause
    exit /b 1
)

echo.
echo Git encontrado! Configurando repositorio...
echo.

echo 1. Inicializando repositorio Git...
git init

echo.
echo 2. Configurando usuario Git...
git config user.name "ARCA Construccion"
git config user.email "admin@arca-construccion.com"

echo.
echo 3. Agregando archivos al repositorio...
git add .

echo.
echo 4. Haciendo primer commit...
git commit -m "Version inicial del Sistema ARCA Construccion"

echo.
echo 5. Creando rama main...
git branch -M main

echo.
echo 6. Configurando rama por defecto...
git config --global init.defaultBranch main

echo.
echo ========================================
echo    CONFIGURACION COMPLETADA!
echo ========================================
echo.
echo Para conectar con un repositorio remoto:
echo git remote add origin <URL-DEL-REPOSITORIO>
echo git push -u origin main
echo.
echo Para hacer commits futuros:
echo git add .
echo git commit -m "Descripcion de los cambios"
echo git push origin main
echo.
pause
