@echo off
REM PyInstaller ile GUI exe üretimi
pyinstaller --noconfirm --onefile --add-data "ffmpeg;ffmpeg" --add-data "src;src" src/gui_pyside.py --name MetadataCleanerGUI
REM FFmpeg ve src klasörü exe ile aynı dizinde olacak şekilde eklenir
REM Çıktı: dist/MetadataCleanerGUI.exe 