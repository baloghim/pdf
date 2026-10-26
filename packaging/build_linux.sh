#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
[[ "$(uname -s)" == Linux && "$(uname -m)" == x86_64 ]] || { echo 'Linux x86_64 build required' >&2; exit 1; }
command -v nfpm >/dev/null || { echo 'Install nfpm v2.41.3 to build DEB/RPM packages.' >&2; exit 1; }
python3 -m venv .venv-build-linux
.venv-build-linux/bin/python -m pip install -e '.[test]' pyinstaller==6.19.0
QT_QPA_PLATFORM=offscreen .venv-build-linux/bin/python -m pytest -q
.venv-build-linux/bin/python -m PyInstaller --noconfirm --clean --windowed \
    --name PDF-Muhely --paths . --distpath dist/linux-bundle packaging/launcher.py
QT_QPA_PLATFORM=offscreen dist/linux-bundle/PDF-Muhely/PDF-Muhely --smoke-test
.venv-build-linux/bin/python packaging/package_linux.py
nfpm package --config build/linux-nfpm.yaml --packager deb --target dist/PDF-Muhely-Linux-x64.deb
nfpm package --config build/linux-nfpm.yaml --packager rpm --target dist/PDF-Muhely-Linux-x64.rpm
# Exercise the actual self-extracting SH, not just the unarchived executable.
QT_QPA_PLATFORM=offscreen bash dist/PDF-Muhely-Linux-x64.sh --smoke-test
