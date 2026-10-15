#!/usr/bin/env python3
"""Optional Ubuntu 26.04 amd64 local SDK; does not install system packages.
Requires the host's runtime libraries and C preprocessor. See docs/build.md.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.request

root = Path(__file__).resolve().parents[1]
sdk = root / 'build/deps/root'
cache = root / 'build/deps/packages'
sdk.mkdir(parents=True, exist_ok=True)
cache.mkdir(parents=True, exist_ok=True)
manifest = json.loads((root / 'config/ubuntu-26.04-deps.json').read_text())

def fetch(item):
    destination = cache / item['file']
    if not destination.exists():
        with urllib.request.urlopen(item['url'], timeout=120) as source:
            data = source.read()
        if len(data) != item['size'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError('Download verification failed: ' + item['file'])
        destination.write_bytes(data)
    if hashlib.sha256(destination.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError('Cache verification failed: ' + str(destination))
    return destination

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    for package in pool.map(fetch, manifest):
        subprocess.run(['dpkg-deb', '-x', str(package), str(sdk)], check=True)

# Packages already installed on this Ubuntu host are not duplicated by APT's plan.
for link in list(sdk.rglob('*')):
    if link.is_symlink() and not link.exists():
        target = Path(os.readlink(link))
        host = target if target.is_absolute() else (Path('/') / link.relative_to(sdk)).parent / target
        if host.exists():
            link.unlink()
            link.symlink_to(host.resolve())
cc1 = sdk / 'usr/libexec/gcc/x86_64-linux-gnu/15/cc1'
if not cc1.exists():
    host_cc1 = Path('/usr/libexec/gcc/x86_64-linux-gnu/15/cc1')
    if not host_cc1.exists():
        raise RuntimeError('Host cpp-15-x86-64-linux-gnu package is required for this local SDK')
    cc1.symlink_to(host_cc1)
print('Local SDK ready:', sdk)
