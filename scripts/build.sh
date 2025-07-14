#!/bin/bash
# Sanal ortam oluştur
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Kullanım:"
echo "GUI: python src/gui_pyside.py"
echo "CLI: python src/cli.py --help" 