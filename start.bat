@echo off
chcp 65001 >nul
title NOTARIUS
cd /d "%~dp0"

echo ============================================================
echo    NOTARIUS - starting the local app...
echo    A browser window will open at http://127.0.0.1:8788
echo    To STOP: close this window (or press Ctrl+C).
echo ============================================================
echo.

rem  Prefer the Windows "py" launcher; fall back to "python".
where py >nul 2>&1
if %errorlevel%==0 (
    py -m notarius web
    goto :ended
)
where python >nul 2>&1
if %errorlevel%==0 (
    python -m notarius web
    goto :ended
)

echo    Python was not found on this computer.
echo    Install it once from:  https://www.python.org/downloads/
echo    (on the first screen tick "Add Python to PATH"), then run this again.
echo.
pause
exit /b 1

:ended
rem  If the app could not start (e.g. wrong folder), keep the window open.
if errorlevel 1 (
    echo.
    echo    Could not start. Make sure this file is inside the NOTARIUS folder
    echo    (the one that contains the "notarius" subfolder).
    echo.
    pause
)
