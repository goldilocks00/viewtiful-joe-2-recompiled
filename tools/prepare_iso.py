#!/usr/bin/env python3
"""Create a local raw GameCube image from CISO. Never overwrite an existing file.
Absent CISO blocks become zeros: this is not a restored bit-perfect original dump.
"""
import argparse
from pathlib import Path
from inspect_disc import Disc, u32

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('source', type=Path)
parser.add_argument('destination', type=Path)
args = parser.parse_args()
disc = Disc(args.source)
try:
    if disc.kind != 'CISO' or u32(disc.read(0, 0x20), 0x1c) != 0xc2339f3d:
        raise ValueError('Expected a GameCube CISO')
    # Dolphin DiscIO/DiscUtils.h MINI_DVD_SIZE. This is a normalized working copy.
    length = 1459978240
    if length > disc.limit:
        raise ValueError('CISO address range is too small')
    with args.destination.open('xb') as target:
        for offset in range(0, length, 8 * 1024 * 1024):
            target.write(disc.read(offset, min(8 * 1024 * 1024, length - offset)))
    print(f'Created {args.destination} ({length} bytes); source unchanged')
finally:
    disc.file.close()
