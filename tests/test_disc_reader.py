import sys
import tempfile
import struct
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from inspect_disc import Disc

class DiscReaderTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'test.ciso'
    def tearDown(self):
        self.temp.cleanup()
    def write_ciso(self, payload=b'abcdWXYZ', flags=b'\1\0\1'):
        header=b'CISO'+struct.pack('<I',4)+flags
        self.path.write_bytes(header.ljust(0x8000,b'\0')+payload)
    def test_sparse_cross_block_read(self):
        self.write_ciso();d=Disc(self.path)
        try:
            self.assertEqual(d.read(2,8),b'cd\0\0\0\0WX')
            self.assertEqual(d.read(0,12),b'abcd\0\0\0\0WXYZ')
            with self.assertRaises(ValueError):d.read(d.limit-1,2)
        finally:d.file.close()
    def test_truncated_payload_rejected(self):
        self.write_ciso(payload=b'abcd')
        with self.assertRaises(ValueError):Disc(self.path)
    def test_invalid_map_rejected(self):
        self.write_ciso(flags=b'\2')
        with self.assertRaises(ValueError):Disc(self.path)
    def test_trailing_bytes_reported_not_mapped(self):
        self.write_ciso(payload=b'abcdWXYZtrailer');d=Disc(self.path)
        try:
            self.assertEqual(d.trailing_bytes,7)
            self.assertEqual(d.read(8,4),b'WXYZ')
        finally:d.file.close()
    def test_raw_image_read_and_bounds(self):
        self.path.write_bytes(b'0123456789');d=Disc(self.path)
        try:
            self.assertEqual(d.read(3,4),b'3456')
            with self.assertRaises(ValueError):d.read(-1,2)
            with self.assertRaises(ValueError):d.read(9,2)
        finally:d.file.close()

if __name__=='__main__':unittest.main()
