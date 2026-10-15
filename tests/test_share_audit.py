"""Regression tests for excluding local game content from Git sharing."""
import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('audit_share', Path(__file__).resolve().parents[1] / 'tools/audit_share.py')
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ShareAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        previous = audit.ROOT
        self.addCleanup(setattr, audit, 'ROOT', previous)
        audit.ROOT = self.root
        self.git('init', '-q')

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], stderr=subprocess.STDOUT)

    def add(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        self.git('add', path)

    def test_source_text_accepted(self):
        self.add('README.md', b'Experimental project\n')
        with contextlib.redirect_stdout(io.StringIO()):
            audit.main()

    def test_binary_disguised_as_text_rejected(self):
        self.add('config/data.json', b'game\0data')
        with self.assertRaisesRegex(SystemExit, 'Binary blob'):
            audit.main()

    def test_deleted_game_file_still_rejected_in_history(self):
        self.add('extracted/file.txt', b'fixture only')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@localhost', 'commit', '-qm', 'fixture')
        self.git('rm', '-q', 'extracted/file.txt')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@localhost', 'commit', '-qm', 'remove fixture')
        with self.assertRaisesRegex(SystemExit, 'Unexpected tracked path'):
            audit.main()


if __name__ == '__main__':
    unittest.main()
