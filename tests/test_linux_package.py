"""Verify the portable SH really extracts, forwards arguments and cleans up."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

spec = importlib.util.spec_from_file_location('linux_packager', Path(__file__).parents[1] / 'packaging/package_linux.py')
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


@pytest.mark.skipif(sys.platform != 'linux' or sys.version_info < (3, 11) or not shutil.which('bash'), reason='Linux shell package')
@pytest.mark.parametrize('exit_code', [0, 7])
def test_portable_launcher_handles_spaces_exit_status_and_cleanup(tmp_path, exit_code):
    root = tmp_path / 'project with spaces'
    bundle = root / 'dist/linux-bundle/PDF-Muhely'
    bundle.mkdir(parents=True)
    executable = bundle / 'PDF-Muhely'
    executable.write_text(f'#!/bin/sh\nprintf "%s\\n" "$0" "$@"\nexit {exit_code}\n')
    executable.chmod(0o755)
    (root / 'pyproject.toml').write_text('[project]\nversion="0.1.0"\n')
    packager.package(root)
    result = subprocess.run(['bash', str(root / 'dist/PDF-Muhely-Linux-x64.sh'), 'argument with spaces'], capture_output=True, text=True)
    assert result.returncode == exit_code, result.stderr
    lines = result.stdout.splitlines()
    assert lines[1:] == ['argument with spaces']
    assert not Path(lines[0]).exists(), 'Temporary extracted bundle was left behind'
