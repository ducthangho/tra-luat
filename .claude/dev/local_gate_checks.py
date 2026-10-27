"""Behavior checks for the standalone runner. No network or repository writes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).with_name('local_gate.py')
spec = importlib.util.spec_from_file_location('local_gate', RUNNER)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class RunnerChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.git('init', '-q')
        (self.root / 'probe.py').write_text('print("POSITIVE")\n')
        self.git('add', '.')
        self.git('-c', 'user.name=test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'fixture')
        self.head = self.git('rev-parse', 'HEAD').strip()
        self.plan = self.base / 'plan.json'
        self.out = self.base / 'evidence'
        self.make_plan()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args], text=True)

    def make_plan(self, code=None, timeout=5):
        argv = ['{python}', '-B', 'probe.py'] if code is None else ['{python}', '-c', code]
        self.plan.write_text(json.dumps({'schema_version': 1, 'steps': [
            {'id': 'probe', 'argv': argv, 'positive': ['^POSITIVE$'], 'timeout_seconds': timeout}]}))

    def run_gate(self):
        return gate.execute(self.root, self.out, self.plan, self.head)

    def test_success_and_tampered_log(self):
        self.assertEqual(self.run_gate(), 0)
        self.assertEqual(gate.verify(self.out, self.head, self.plan), 0)
        (self.out / 'probe.log').write_text('POSITIVE\ntampered\n')
        with self.assertRaises(ValueError):
            gate.verify(self.out, self.head, self.plan)

    def test_zero_exit_without_positive_is_failure(self):
        self.make_plan('pass')
        self.assertEqual(self.run_gate(), 1)

    def test_nonzero_with_positive_is_failure(self):
        self.make_plan('print("POSITIVE"); raise SystemExit(7)')
        self.assertEqual(self.run_gate(), 1)

    def test_timeout_is_not_measured(self):
        self.make_plan('import time; time.sleep(30)', timeout=1)
        self.assertEqual(self.run_gate(), 1)
        r = json.loads((self.out / 'receipt.json').read_text())
        self.assertEqual(r['steps'][0]['state'], 'not_measured')

    def test_dirty_tree_and_wrong_head_refused(self):
        with self.assertRaises(ValueError):
            gate.execute(self.root, self.out, self.plan, '0' * 40)
        (self.root / 'probe.py').write_text('pass')
        with self.assertRaises(ValueError):
            self.run_gate()

    def test_reuse_output_refused(self):
        self.assertEqual(self.run_gate(), 0)
        with self.assertRaises(FileExistsError):
            self.run_gate()

    def test_missing_step_cannot_verify(self):
        self.assertEqual(self.run_gate(), 0)
        r = json.loads((self.out / 'receipt.json').read_text())
        r['steps'] = []
        (self.out / 'receipt.json').write_text(json.dumps(r))
        with self.assertRaises(ValueError):
            gate.verify(self.out, self.head, self.plan)

    def test_rewritten_plan_not_trusted(self):
        self.assertEqual(self.run_gate(), 0)
        (self.out / 'plan.json').write_text('{}')
        with self.assertRaises((ValueError, KeyError)):
            gate.verify(self.out, self.head, self.plan)

    def test_output_inside_checkout_refused(self):
        with self.assertRaises(ValueError):
            gate.execute(self.root, self.root / 'logs', self.plan, self.head)

    def test_partial_run_cannot_verify(self):
        plan = json.loads(self.plan.read_text())
        other = dict(plan['steps'][0], id='other')
        plan['steps'].append(other)
        self.plan.write_text(json.dumps(plan))
        self.assertEqual(gate.execute(self.root, self.out, self.plan, self.head, 'probe'), 1)
        with self.assertRaises(ValueError):
            gate.verify(self.out, self.head, self.plan)

    def test_test_editing_checkout_invalidates_receipt(self):
        self.make_plan('from pathlib import Path; Path("probe.py").write_text("pass"); print("POSITIVE")')
        self.assertEqual(self.run_gate(), 1)
        with self.assertRaises(ValueError):
            gate.verify(self.out, self.head, self.plan)


if __name__ == '__main__':
    unittest.main()
