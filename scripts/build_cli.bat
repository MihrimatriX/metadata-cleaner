@echo off
REM PyInstaller ile CLI exe üretimi
pyinstaller --noconfirm --onefile --add-data "ffmpeg;ffmpeg" --add-data "src;src" src/cli.py --name metadata-cleaner
REM FFmpeg ve src klasörü exe ile aynı dizinde olacak şekilde eklenir
REM Çıktı: dist/metadata-cleaner.exe 