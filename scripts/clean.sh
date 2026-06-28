#!/bin/bash
echo "[*] Purgando artefactos de compilacion y caches locales..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".tox" -exec rm -rf {} +
echo "[+] Limpieza finalizada."
