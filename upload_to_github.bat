@echo off
REM Upload learning-checkin to GitHub
REM Run this script from D:\workspace\learning-checkin

echo ========================================
echo Learning Check-in Skill - GitHub Upload
echo ========================================
echo.

cd /d D:\workspace\learning-checkin

echo Checking git status...
git status

echo.
echo ========================================
echo Instructions:
echo 1. If this is a new repository, create one at:
echo    https://github.com/daizongyu/learning-checkin
echo 2. Run these commands:
echo.
echo    git init
echo    git add .
echo    git commit -m "Initial commit: Learning Check-in Skill v1.0.0"
echo    git branch -M main
echo    git remote add origin https://github.com/daizongyu/learning-checkin.git
echo    git push -u origin main
echo.
echo ========================================
echo.

pause