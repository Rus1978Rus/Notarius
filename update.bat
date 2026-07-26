@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title NOTARIUS updater

echo ============================================================
echo    NOTARIUS - update to the latest version from GitHub
echo ============================================================
echo.
echo    Before updating: STOP the app if it is running
echo    (press Ctrl+C in the black window where it runs).
echo.
echo    Press any key to download and install the latest version...
pause >nul

set "URL=https://github.com/Rus1978Rus/Notarius/archive/refs/heads/main.zip"
set "ZIP=%TEMP%\notarius_update.zip"
set "OUT=%TEMP%\notarius_update"

echo.
echo [1/3] Downloading...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { Invoke-WebRequest -Uri '%URL%' -OutFile '%ZIP%' -UseBasicParsing } catch { Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 goto :fail

echo [2/3] Extracting...
if exist "%OUT%" rmdir /s /q "%OUT%"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { Expand-Archive -Path '%ZIP%' -DestinationPath '%OUT%' -Force } catch { Write-Host $_.Exception.Message; exit 1 }"
if errorlevel 1 goto :fail

echo [3/3] Installing over this folder...
rem  Copy the fresh files over the folder this script lives in.
rem  Exclude this running script itself to avoid overwriting it mid-run.
robocopy "%OUT%\Notarius-main" "%~dp0." /E /XF "%~nx0" /NFL /NDL /NJH /NJS /NC /NS >nul
if errorlevel 8 goto :fail

del "%ZIP%" >nul 2>&1
rmdir /s /q "%OUT%" >nul 2>&1

echo.
echo ============================================================
echo    Done - you are now on the latest version.
echo    Start the app again with:   py -m notarius web
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo    Update FAILED. Check your internet connection and try again.
echo    Or download the ZIP by hand from:
echo    https://github.com/Rus1978Rus/Notarius  (Code - Download ZIP)
echo.
pause
exit /b 1
