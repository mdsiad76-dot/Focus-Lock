@echo off
cd /d "%~dp0"
where python >nul 2>nul
if not %errorlevel%==0 (
    echo Python is not installed. Install it first from python.org and TICK "Add Python to PATH".
    start https://www.python.org/downloads/
    pause
    exit /b
)
python -m pip install pyinstaller
python -m PyInstaller --onefile --noconsole --name FocusLock focus_lock.py
echo.
echo Done! Your program is in the "dist" folder: dist\FocusLock.exe
pause
