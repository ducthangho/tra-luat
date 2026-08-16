@echo off
setlocal
chcp 65001 >nul 2>&1
title tra-luat - don nhanh remote da merge

rem ============================================================================
rem  Vo boc double-click cho don-nhanh.ps1.
rem  Vi sao can: Windows KHONG chay .ps1 khi double-click (mo trong editor), va
rem  ExecutionPolicy co the chan script. Tep .cmd nay go ca hai.
rem
rem  DA TRA GIA 16-08-2026: ban dau chi giao .ps1 kem cau lenh `.\scripts\
rem  don-nhanh.ps1`. May nguoi dung o che do AllSigned nen CHAN ngay:
rem  "is not digitally signed. You cannot run this script on the current system."
rem  Nguoi viet kiem script tren pwsh Linux, noi ExecutionPolicy mac dinh la
rem  Unrestricted - dung lop loi "chay duoc o day khac chay duoc o do" ma kho
rem  nay da ghi nhieu lan. Va khuon nay DA CO SAN trong kho o deploy-package.cmd
rem  lan tl-setup.cmd; bo qua mot loi giai da viet san la dat hon la khong biet.
rem
rem  Double-click                -> CHI IN se xoa gi (mac dinh AN TOAN, khong xoa)
rem  don-nhanh.cmd -Xoa          -> xoa that
rem  don-nhanh.cmd -GiuThem a,b  -> giu them nhanh a va b
rem  Moi doi so deu chuyen thang cho don-nhanh.ps1.
rem
rem  rc: 0 = xong (hoac dry-run) | 1 = con nhanh sot sau khi xoa
rem      3 = khong phai kho git / git that bai | 12 = thieu git
rem ============================================================================

set "HERE=%~dp0"
set "PS1=%HERE%don-nhanh.ps1"

if not exist "%PS1%" (
  echo   [LOI] Khong thay "%PS1%"
  echo         Tep .cmd nay phai nam CUNG thu muc scripts\ voi don-nhanh.ps1.
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
rem Chi pause khi KHONG co doi so - tuc duong double-click, de cua so khong bien mat.
rem Chay tu terminal/CI co doi so thi tra rc ngay, khong treo cho.
if "%~1"=="" (
  echo.
  echo   rc=%RC%
  pause
)
exit /b %RC%
