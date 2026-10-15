#!/usr/bin/env python3
"""Create local runtime directories and initial profiles, preserving user settings."""
from pathlib import Path
import shutil


def prepare_user(root: Path) -> Path:
    user = root / 'build/user'
    for relative in ('Config', 'Cache/Shaders', 'Logs', 'Backup'):
        (user / relative).mkdir(parents=True, exist_ok=True)
    for source, destination in (('frontend.ini', 'config.ini'), ('GCPadNew.ini', 'Config/GCPadNew.ini')):
        target = user / destination
        if not target.exists():
            shutil.copyfile(root / 'config' / source, target)
    return user


if __name__ == '__main__':
    prepare_user(Path(__file__).resolve().parents[1])
