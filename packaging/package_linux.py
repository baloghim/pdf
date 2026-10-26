"""Create nfpm metadata and a self-extracting, non-installing Linux launcher."""
import json
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def package(root=ROOT):
    import tomllib  # Linux packaging uses Python 3.12, Windows LTSB uses 3.10.
    bundle = root / 'dist/linux-bundle/PDF-Muhely'
    if not (bundle / 'PDF-Muhely').is_file():
        raise FileNotFoundError('Build the Linux application first')
    version = tomllib.loads((root / 'pyproject.toml').read_text())['project']['version']
    config = {
        'name': 'pdf-muhely', 'arch': 'amd64', 'platform': 'linux',
        'version': version, 'maintainer': 'baloghim <baloghim@users.noreply.github.com>',
        'description': 'PDF-ek összefűzése és kettévágása grafikus felületen.',
        'homepage': 'https://github.com/baloghim/pdf',
        'contents': [
            {'src': str(bundle), 'dst': '/opt/pdf-muhely', 'type': 'tree'},
            {'src': str(root / 'packaging/pdf-muhely.desktop'),
             'dst': '/usr/share/applications/pdf-muhely.desktop'},
            {'src': '/opt/pdf-muhely/PDF-Muhely', 'dst': '/usr/bin/pdf-muhely', 'type': 'symlink'},
        ],
        'overrides': {
            'deb': {'depends': ['libc6 (>= 2.35)', 'libstdc++6', 'libgcc-s1', 'libx11-xcb1', 'libxcb-sync1', 'libgl1', 'libegl1', 'libglib2.0-0',
                                'libfontconfig1', 'libdbus-1-3', 'libxkbcommon0',
                                'libxkbcommon-x11-0', 'libxcb-cursor0', 'libxcb-icccm4',
                                'libxcb-image0', 'libxcb-keysyms1', 'libxcb-render-util0',
                                'libxcb-xinerama0', 'libxcb-randr0', 'libxcb-shape0',
                                'libxcb-xfixes0', 'libsm6', 'libice6']},
            'rpm': {'depends': ['glibc >= 2.35', 'libstdc++.so.6()(64bit)', 'libgcc_s.so.1()(64bit)', 'libX11-xcb.so.1()(64bit)', 'libxcb-sync.so.1()(64bit)', 'libGL.so.1()(64bit)',
                                'libEGL.so.1()(64bit)', 'libglib-2.0.so.0()(64bit)',
                                'libfontconfig.so.1()(64bit)', 'libdbus-1.so.3()(64bit)',
                                'libxkbcommon.so.0()(64bit)', 'libxkbcommon-x11.so.0()(64bit)',
                                'libxcb-cursor.so.0()(64bit)', 'libxcb-icccm.so.4()(64bit)',
                                'libxcb-image.so.0()(64bit)', 'libxcb-keysyms.so.1()(64bit)',
                                'libxcb-render-util.so.0()(64bit)', 'libxcb-xinerama.so.0()(64bit)',
                                'libxcb-randr.so.0()(64bit)', 'libxcb-shape.so.0()(64bit)',
                                'libxcb-xfixes.so.0()(64bit)', 'libSM.so.6()(64bit)',
                                'libICE.so.6()(64bit)']},
        },
    }
    (root / 'build').mkdir(exist_ok=True)
    # JSON is valid YAML, avoiding an extra build-only Python dependency.
    (root / 'build/linux-nfpm.yaml').write_text(json.dumps(config, ensure_ascii=False, indent=2))
    header = '''#!/bin/sh
# PDF Muhely portable Linux x86_64 application. No system installation.
set -eu
bundle_dir=$(mktemp -d "${TMPDIR:-/tmp}/pdf-muhely.XXXXXXXX")
trap 'rm -rf -- "$bundle_dir"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
tail -n +PAYLOAD_LINE "$0" | tar -xz -C "$bundle_dir"
"$bundle_dir/PDF-Muhely/PDF-Muhely" "$@"
exit $?
'''
    header = header.replace('PAYLOAD_LINE', str(header.count('\n') + 1))
    asset = root / 'dist/PDF-Muhely-Linux-x64.sh'
    with asset.open('wb') as output:
        output.write(header.encode())
        with tarfile.open(fileobj=output, mode='w:gz') as archive:
            archive.add(bundle, arcname='PDF-Muhely')
    asset.chmod(0o755)


if __name__ == '__main__':
    package()
