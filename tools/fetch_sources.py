#!/usr/bin/env python3
"""Fetch the pinned public tool sources. Never fetch game data."""
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
lock = json.loads((root / 'config/sources.lock.json').read_text())
target = root / 'upstream/ModernGekko-Template'
if not target.exists():
    subprocess.run(['git','clone','https://github.com/ExpansionPak/ModernGekko-Template.git',str(target)],check=True)
revision = subprocess.check_output(['git','-C',str(target),'rev-parse','HEAD'],text=True).strip()
if revision != lock['template']:
    if subprocess.check_output(['git','-C',str(target),'status','--porcelain'],text=True).strip():
        raise RuntimeError('Sources have local changes; refusing to change their revision')
    subprocess.run(['git','-C',str(target),'fetch','origin',lock['template']],check=True)
    subprocess.run(['git','-C',str(target),'checkout','--detach',lock['template']],check=True)
subprocess.run(['git','-C',str(target),'submodule','update','--init','--recursive'],check=True)
modern = target / 'lib/ModernGekko'
patches = [
    (modern, 'moderngekko-build-jobs.patch'),
    (modern, 'moderngekko-enable-egl-option.patch'),
    (modern / 'vendor/dolphin', 'recompcore-headless-shader-progress.patch'),
    (modern / 'vendor/dolphin', 'recompcore-pad-trace.patch'),
    (modern / 'vendor/dolphin', 'recompcore-tutorial-entry-trace.patch'),
]
for repository, filename in patches:
    patch = root / 'patches' / filename
    reverse = subprocess.run(['git', '-C', str(repository), 'apply', '--reverse', '--check', str(patch)], capture_output=True)
    if reverse.returncode != 0:
        subprocess.run(['git', '-C', str(repository), 'apply', '--check', str(patch)], check=True)
        subprocess.run(['git', '-C', str(repository), 'apply', str(patch)], check=True)
print('Pinned sources ready; build and Linux runtime patches applied')
