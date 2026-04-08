@echo off
cd /d "%~dp0.."
python src\cli.py %*
if errorlevel 1 py -3 src\cli.py %*
