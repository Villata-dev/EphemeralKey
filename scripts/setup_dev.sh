#!/bin/bash
echo "[*] Configurando entorno de desarrollo para EphemeralKey..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install tox mkdocs
echo "[+] Entorno listo."
