@echo off
cd /d "%~dp0.."
python src\gui_pyside.py
if errorlevel 1 py -3 src\gui_pyside.py
