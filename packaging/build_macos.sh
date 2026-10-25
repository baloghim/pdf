#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "A macOS .app csomagot macOS rendszeren kell összeállítani." >&2
    exit 1
fi
python3 -m venv .venv-build
.venv-build/bin/python -m pip install -e '.[test]' 'pyinstaller==6.19.0'
.venv-build/bin/python -m pytest -q
.venv-build/bin/python -m PyInstaller --noconfirm --clean --windowed \
    --name 'PDF Muhely' --osx-bundle-identifier hu.baloghim.pdfmuhely \
    --paths . packaging/launcher.py
# Test the bundled executable and its Qt plugins without opening a persistent window.
QT_QPA_PLATFORM=offscreen 'dist/PDF Muhely.app/Contents/MacOS/PDF Muhely' --smoke-test
/usr/bin/ditto -c -k --sequesterRsrc --keepParent \
    'dist/PDF Muhely.app' "dist/PDF-Muhely-macOS-$(uname -m).zip"
echo "Elkészült: dist/PDF Muhely.app"
