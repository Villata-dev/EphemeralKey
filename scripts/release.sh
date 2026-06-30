#!/bin/bash
# Script de empaquetado y versionado
VERSION=$1
if [ -z "$VERSION" ]; then
  echo "Uso: ./release.sh [version]"
  exit 1
fi
echo "[*] Limpiando caches..."
./scripts/clean.sh
echo "[*] Generando tag de version $VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"
echo "[+] Proceso completado. Ejecute 'git push origin main --tags' para finalizar."
