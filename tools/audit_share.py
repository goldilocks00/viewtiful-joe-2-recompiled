#!/usr/bin/env python3
"""Check staged paths and reachable Git history for unexpected shareable content.
This conservative format check does not replace reviewing the source and patches.
"""
from pathlib import Path, PurePosixPath
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {'.md', '.txt', '.py', '.sh', '.ini', '.json', '.patch', '.yml', '.yaml'}
NAMES = {'.gitignore', '.gitattributes', 'LICENSE', 'COPYING', 'NOTICE'}
LOCAL = {'iso', 'extracted', 'build', 'upstream'}


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def inspect_path(name):
    path = PurePosixPath(name)
    if path.parts[0] in LOCAL or (path.suffix.lower() not in ALLOWED and path.name not in NAMES):
        raise SystemExit(f'Unexpected tracked path: {name}')


def main():
    blobs = set()
    for entry in git('ls-files', '--stage', '-z').split(b'\0'):
        if not entry:
            continue
        metadata, name = entry.split(b'\t', 1)
        mode, oid, stage = metadata.split()
        inspect_path(name.decode())
        if mode not in (b'100644', b'100755') or stage != b'0':
            raise SystemExit('Unresolved entry, symlink or submodule in index')
        blobs.add(oid.decode())
    # Walk each tree so renamed or previously removed paths are checked as well.
    for commit in git('rev-list', '--all').splitlines():
        for entry in git('ls-tree', '-r', '-z', commit.decode()).split(b'\0'):
            if not entry:
                continue
            metadata, name = entry.split(b'\t', 1)
            mode, kind, oid = metadata.split()
            inspect_path(name.decode())
            if kind != b'blob' or mode not in (b'100644', b'100755'):
                raise SystemExit('Unexpected historical Git entry')
            blobs.add(oid.decode())
    for oid in blobs:
        size = int(git('cat-file', '-s', oid))
        if size > 1024 * 1024:
            raise SystemExit(f'Blob exceeds source-only size limit: {oid}')
        data = git('cat-file', 'blob', oid)
        if b'\0' in data:
            raise SystemExit(f'Binary blob: {oid}')
        data.decode('utf-8')
    print(f'PASS: index and reachable history; {len(blobs)} unique UTF-8 source/document blobs.')


if __name__ == '__main__':
    main()
