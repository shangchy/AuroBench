@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
if errorlevel 1 (
    echo.
    echo Deployment finished with errors. See messages above.
) else (
    echo.
    echo Deployment completed successfully.
)
pause
