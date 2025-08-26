@echo off
REM Script para configurar respaldo automático diario en Windows
REM Ejecutar como Administrador

echo ========================================
echo  CONFIGURADOR DE RESPALDO AUTOMATICO
echo ========================================
echo.

REM Obtener ruta del proyecto
set PROJECT_PATH=%~dp0..
cd /d "%PROJECT_PATH%"

echo Ruta del proyecto: %PROJECT_PATH%
echo.

REM Crear directorio de scripts si no existe
if not exist "scripts" mkdir scripts
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

REM Crear script de respaldo para Windows
echo Creando script de respaldo para Windows...

(
echo @echo off
echo REM Script de respaldo automático para Windows
echo echo Iniciando respaldo automático...
echo echo Fecha: %date% %time%
echo.
echo cd /d "%PROJECT_PATH%"
echo python scripts/backup_automatico.py --compress --retention 30
echo.
echo if errorlevel 1 ^(
echo     echo Error en el respaldo
echo     exit /b 1
echo ^) else ^(
echo     echo Respaldo completado exitosamente
echo     exit /b 0
echo ^)
) > "scripts\backup_windows.bat"

echo Script de respaldo creado: scripts\backup_windows.bat
echo.

REM Crear tarea programada en Windows Task Scheduler
echo Configurando tarea programada en Windows Task Scheduler...
echo.

REM Crear archivo XML para la tarea
(
echo ^<?xml version="1.0" encoding="UTF-16"?^>
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^>
echo   ^<Triggers^>
echo     ^<TimeTrigger^>
echo       ^<Repetition^>
echo         ^<Interval^>P1D^</Interval^>
echo         ^<StopAtDurationEnd^>false^</StopAtDurationEnd^>
echo       ^</Repetition^>
echo       ^<StartBoundary^>2025-01-01T02:00:00^</StartBoundary^>
echo       ^<Enabled^>true^</Enabled^>
echo     ^</TimeTrigger^>
echo   ^</Triggers^>
echo   ^<Principals^>
echo     ^<Principal id="Author"^>
echo       ^<LogonType^>InteractiveToken^</LogonType^>
echo       ^<RunLevel^>HighestAvailable^</RunLevel^>
echo     ^</Principal^>
echo   ^</Principals^>
echo   ^<Settings^>
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^>
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^>
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^>
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^>
echo     ^<StartWhenAvailable^>false^</StartWhenAvailable^>
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^>
echo     ^<IdleSettings^>
echo       ^<StopOnIdleEnd^>false^</StopOnIdleEnd^>
echo       ^<RestartOnIdle^>false^</RestartOnIdle^>
echo     ^</IdleSettings^>
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^>
echo     ^<Enabled^>true^</Enabled^>
echo     ^<Hidden^>false^</Hidden^>
echo     ^<RunOnlyIfIdle^>false^</RunOnlyIfIdle^>
echo     ^<WakeToRun^>false^</WakeToRun^>
echo     ^<ExecutionTimeLimit^>PT1H^</ExecutionTimeLimit^>
echo     ^<Priority^>7^</Priority^>
echo   ^</Settings^>
echo   ^<Actions Context="Author"^>
echo     ^<Exec^>
echo       ^<Command^>%PROJECT_PATH%\scripts\backup_windows.bat^</Command^>
echo       ^<WorkingDirectory^>%PROJECT_PATH%^</WorkingDirectory^>
echo     ^</Exec^>
echo   ^</Actions^>
echo ^</Task^>
) > "scripts\backup_task.xml"

echo Archivo XML de tarea creado: scripts\backup_task.xml
echo.

REM Instrucciones para el usuario
echo ========================================
echo  INSTRUCCIONES PARA CONFIGURAR LA TAREA
echo ========================================
echo.
echo Para configurar el respaldo automático:
echo.
echo 1. Abrir "Programador de tareas" como Administrador
echo    - Presionar Win + R
echo    - Escribir: taskschd.msc
echo    - Presionar Enter
echo.
echo 2. En el panel derecho, hacer clic en "Importar tarea..."
echo.
echo 3. Seleccionar el archivo: %PROJECT_PATH%\scripts\backup_task.xml
echo.
echo 4. Configurar la cuenta de usuario que ejecutará la tarea
echo.
echo 5. La tarea se ejecutará automáticamente todos los días a las 2:00 AM
echo.
echo ========================================
echo.

REM Probar el script de respaldo
echo ¿Desea probar el script de respaldo ahora? ^(S/N^)
set /p TEST_BACKUP=

if /i "%TEST_BACKUP%"=="S" (
    echo.
    echo Probando script de respaldo...
    echo.
    call scripts\backup_windows.bat
    echo.
    echo Prueba completada.
) else (
    echo.
    echo Puede probar el script manualmente ejecutando:
    echo   scripts\backup_windows.bat
)

echo.
echo ========================================
echo  CONFIGURACION COMPLETADA
echo ========================================
echo.
echo El sistema de respaldo automático está configurado.
echo Revise la carpeta 'backups' para ver los respaldos creados.
echo.
pause
