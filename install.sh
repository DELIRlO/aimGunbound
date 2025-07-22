#!/bin/bash
echo "=== Instalador do Gunbound 2025 Aimbot ==="
echo "Instalando dependências..."

# Atualiza o sistema
sudo apt-get update

# Instala Tesseract OCR
sudo apt-get install -y tesseract-ocr

# Instala dependências Python
pip install -r docs/requirements.txt

echo "Instalação concluída!"
echo "Para executar: cd src && python main.py"
