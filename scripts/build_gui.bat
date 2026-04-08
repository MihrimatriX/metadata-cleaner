@echo off
REM Build GUI exe with PyInstaller
pyinstaller --noconfirm --onefile --add-data "ffmpeg;ffmpeg" --add-data "src;src" src/gui_pyside.py --name MetadataCleanerGUI
REM FFmpeg and src folder will be included in the same directory as the exe
REM Output: dist/MetadataCleanerGUI.exe 