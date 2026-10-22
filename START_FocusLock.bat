@echo off
cd /d "%~dp0"
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw focus_lock.py
) else (
    echo Python is not installed yet.
    echo Opening the download page. Install it and TICK "Add Python to PATH",
    echo then double-click this file again.
    start https://www.python.org/downloads/
    pause
)
