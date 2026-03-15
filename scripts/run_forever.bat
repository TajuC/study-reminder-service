@echo off
chcp 65001 >nul 2>&1
title Study Reminder Service

cd /d "%~dp0\.."

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:loop
echo [%date% %time%] Starting reminder service...
python -m app.main
echo [%date% %time%] Service exited. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto loop
