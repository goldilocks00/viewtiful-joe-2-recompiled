#!/usr/bin/env python3
"""Read-only GameCube ISO/CISO reconnaissance; emits metadata, never game payloads.

Format references: Dolphin DiscIO/CISOBlob.{h,cpp}, FileSystemGCWii.cpp.
CISO hashes describe the container, not a pristine raw disc.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct


def u32(data, offset=0):
    return struct.unpack_from('>I', data, offset)[0]


class Disc:
    def __init__(self, path):
        self.file = path.open('rb')
        try:
            self._initialize(path)
        except Exception:
            self.file.close()
            raise

    def _initialize(self, path):
        self.size = path.stat().st_size
        self.mapping = None
        self.trailing_bytes = 0
        self.kind = 'ISO/GCM'
        header = self.file.read(0x8000)
        if header[:4] == b'CISO':
            if len(header) != 0x8000:
                raise ValueError('Truncated CISO header')
            self.kind = 'CISO'
            self.block = struct.unpack_from('<I', header, 4)[0]
            if not 0 < self.block <= 128 * 1024 * 1024:
                raise ValueError('Invalid CISO block size')
            self.mapping = []
            physical = 0
            for flag in header[8:]:
                if flag not in (0, 1):
                    raise ValueError('Invalid CISO block flag')
                self.mapping.append(physical if flag else None)
                physical += flag
            self.trailing_bytes = self.size - (0x8000 + physical * self.block)
            if self.trailing_bytes < 0:
                raise ValueError('CISO payload length disagrees with block map')
        self.limit = len(self.mapping) * self.block if self.mapping else self.size

    def read(self, offset, length):
        if offset < 0 or length < 0 or offset + length > self.limit:
            raise ValueError('Read outside image')
        if self.mapping is None:
            self.file.seek(offset)
            data = self.file.read(length)
            if len(data) != length:
                raise ValueError('Truncated image')
            return data
        result = bytearray()
        while length:
            logical, within = divmod(offset, self.block)
            take = min(length, self.block - within)
            physical = self.mapping[logical]
            if physical is None:
                result.extend(bytes(take))
            else:
                self.file.seek(0x8000 + physical * self.block + within)
                part = self.file.read(take)
                if len(part) != take:
                    raise ValueError('Truncated CISO block')
                result.extend(part)
            offset += take
            length -= take
        return bytes(result)


def inspect(path):
    disc = Disc(path)
    try:
        h = disc.read(0, 0x440)
        if u32(h, 0x1c) != 0xc2339f3d:
            raise ValueError('Not a GameCube disc')
        disc.limit = min(disc.limit, 1459978240)
        dol, fst_offset, fst_size = struct.unpack_from('>III', h, 0x420)
        if not 12 <= fst_size <= 128 * 1024 * 1024:
            raise ValueError('Invalid FST size')
        fst = disc.read(fst_offset, fst_size)
        count = u32(fst, 8)
        if fst[0] != 1 or not 1 <= count <= fst_size // 12:
            raise ValueError('Invalid FST root')
        entries = []
        stack = [(0, count, '')]
        for i in range(1, count):
            while i >= stack[-1][1]:
                stack.pop()
            name_type, offset, size = struct.unpack_from('>III', fst, 12 * i)
            name_offset = 12 * count + (name_type & 0xffffff)
            if not 12 * count <= name_offset < len(fst):
                raise ValueError('Invalid FST name offset')
            end = fst.find(b'\0', name_offset)
            if end < 0:
                raise ValueError('Unterminated FST name')
            name = fst[name_offset:end].decode('shift_jis', errors='replace')
            full = stack[-1][2] + name
            if name_type >> 24:
                if offset != stack[-1][0] or not i < size <= stack[-1][1]:
                    raise ValueError('Invalid FST directory')
                entries.append({'path': full + '/', 'directory': True})
                stack.append((i, size, full + '/'))
            else:
                if offset + size > disc.limit:
                    raise ValueError('FST file outside image')
                entries.append({'path': full, 'offset': offset, 'size': size})
        dh = disc.read(dol, 0x100)
        sections = []
        for i in range(18):
            offset, address, size = u32(dh, 4*i), u32(dh, 0x48+4*i), u32(dh, 0x90+4*i)
            if size:
                if size > 32 * 1024 * 1024:
                    raise ValueError('DOL section exceeds GameCube memory scale')
                if offset < 0x100:
                    raise ValueError('DOL section overlaps header')
                disc.read(dol + offset, size)
                sections.append({'name': f'text{i}' if i < 7 else f'data{i-7}', 'offset': offset, 'address': address, 'size': size})
        hashes = {name: hashlib.new(name) for name in ('md5', 'sha1', 'sha256')}
        with path.open('rb') as source:
            for chunk in iter(lambda: source.read(8*1024*1024), b''):
                for digest in hashes.values():
                    digest.update(chunk)
        return {'file': path.name, 'format': disc.kind, 'size': disc.size, 'trailing_bytes': disc.trailing_bytes,
                'hashes': {name: digest.hexdigest() for name, digest in hashes.items()},
                'title': h[0x20:0x400].split(b'\0')[0].decode('ascii', errors='replace'),
                'game_id': h[:6].decode('ascii'), 'disc_number': h[6], 'revision': h[7],
                'dol_offset': dol, 'entry_point': u32(dh, 0xe0),
                'bss_address': u32(dh, 0xd8), 'bss_size': u32(dh, 0xdc),
                'sections': sections, 'fst_offset': fst_offset, 'fst_size': fst_size,
                'entries': entries}
    finally:
        disc.file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.image), indent=2, ensure_ascii=False))
