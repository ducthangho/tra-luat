@echo off
setlocal
chcp 65001 >nul 2>&1
title tra-luat - dong goi + deploy Package

rem ============================================================================
rem  Vo boc double-click cho deploy-package.ps1.
rem  Vi sao can: Windows KHONG chay .ps1 khi double-click (mo trong editor), va
rem  ExecutionPolicy mac dinh co the chan script. Tep .cmd nay go ca hai.
rem
rem  Double-click            -> build + verify, KHONG day (mac dinh AN TOAN)
rem  deploy-package.cmd -Pull -Push     -> lay ban moi nhat roi deploy
rem  Moi doi so deu chuyen thang cho deploy-package.ps1 (-Push -NoTest
rem  -ForceOlder -Out ... -Python ...)
rem
rem  rc: 0 = xong | 1 = gate do | 2 = build/verify hong | 3 = day hong
rem      (gom CHAN THUT LUI)
rem ============================================================================

set "HERE=%~dp0"
set "PS1=%HERE%deploy-package.ps1"

if not exist "%PS1%" (
  echo   [LOI] Khong thay "%PS1%"
  echo         Tep .cmd nay phai nam CUNG thu muc scripts\ voi deploy-package.ps1.
  set "RC=2"
  goto :finish
)

rem Uu tien PowerShell 7+ ^(pwsh^): script duoc kiem tren 7.4.6.
set "PSEXE="
where pwsh >nul 2>&1 && set "PSEXE=pwsh"
if not defined PSEXE (
  where powershell >nul 2>&1 && set "PSEXE=powershell"
  if defined PSEXE (
    echo   [LUU Y] Khong thay pwsh ^(PowerShell 7+^) - dung Windows PowerShell 5.1.
    echo           Script duoc kiem tren 7.4.6; 5.1 chua kiem. Gap loi la thu:
    echo               winget install --id Microsoft.PowerShell
  )
)
if not defined PSEXE (
  echo   [LOI] Khong thay pwsh lan powershell trong PATH.
  set "RC=2"
  goto :finish
)

rem -ExecutionPolicy Bypass: chi ap dung cho TIEN TRINH nay, khong doi cai dat may.
"%PSEXE%" -NoProfile -ExecutionPolicy Bypass -File "%PS1%" %*
set "RC=%ERRORLEVEL%"

:finish
rem Chi pause khi KHONG co doi so - tuc la duong double-click, de cua so khong bien mat.
rem Chay tu terminal/CI co doi so thi tra rc ngay, khong treo cho.
if "%~1"=="" (
  echo.
  echo   rc=%RC%
  pause
)
exit /b %RC%
