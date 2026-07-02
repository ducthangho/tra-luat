@echo off
REM tl-setup.cmd - bam dup de chay setup tra-luat + gws (Windows).
REM Goi PowerShell voi ExecutionPolicy Bypass (khong doi chinh sach he thong).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tl-setup.ps1" %*
echo.
pause
