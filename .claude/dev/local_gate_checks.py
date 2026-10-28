"""Behavior checks for the standalone runner. No network or repository writes."""
import importlib.util
import json
import os
import signal
import time
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

    def test_receipt_invariants_rejected(self):
        self.assertEqual(self.run_gate(), 0)
        path = self.out / 'receipt.json'
        original = json.loads(path.read_text())
        mutations = [('approval', True), ('full_ci_equivalence', True),
                     ('checkout_unchanged', 'false'), ('tree', 'invalid'),
                     ('schema_version', True)]
        for key, value in mutations:
            with self.subTest(field=key):
                edited = dict(original, **{key: value})
                path.write_text(json.dumps(edited))
                with self.assertRaises(ValueError):
                    gate.verify(self.out, self.head, self.plan)
        path.write_text(json.dumps(original))
        for value in ([False], [1]):
            edited = json.loads(json.dumps(original))
            edited['steps'][0]['positive_matches'] = value
            path.write_text(json.dumps(edited))
            with self.assertRaises(ValueError):
                gate.verify(self.out, self.head, self.plan)

    def test_symlinked_artifacts_rejected(self):
        self.assertEqual(self.run_gate(), 0)
        for name in ('receipt.json', 'runner.py', 'plan.json', 'probe.log'):
            with self.subTest(artifact=name):
                path = self.out / name
                saved = self.base / ('saved-' + name)
                path.rename(saved)
                path.symlink_to(saved)
                with self.assertRaises(ValueError):
                    gate.verify(self.out, self.head, self.plan)
                path.unlink()
                saved.rename(path)

    def test_ignored_writes_invalidate_checkout(self):
        (self.root / '.gitignore').write_text('ignored/\n')
        self.git('add', '.gitignore')
        self.git('-c', 'user.name=test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'ignore fixture')
        self.head = self.git('rev-parse', 'HEAD').strip()
        self.make_plan('from pathlib import Path; Path("ignored").mkdir(); '
                       'Path("ignored/file").write_text("changed"); print("POSITIVE")')
        self.assertEqual(self.run_gate(), 1)
        self.assertIs(json.loads((self.out / 'receipt.json').read_text())['checkout_unchanged'], False)

    def test_caller_git_override_is_not_inherited(self):
        from unittest.mock import patch
        with patch.dict(os.environ, GIT_DIR=str(self.base / 'missing-git-dir')):
            self.assertEqual(self.run_gate(), 0)

    def process_alive(self, pid):
        path = Path('/proc') / str(pid) / 'stat'
        return path.exists() and path.read_text().rsplit(')', 1)[1].split()[0] != 'Z'

    def test_timeout_reaps_detached_grandchild(self):
        pidfile = self.base / 'grandchild.pid'
        child = (f'from pathlib import Path; import os,time; '
                 f'Path({str(pidfile)!r}).write_text(str(os.getpid())); time.sleep(60)')
        self.make_plan('import subprocess,sys,time; '
                       f'subprocess.Popen([sys.executable,"-c",{child!r}],start_new_session=True); '
                       'time.sleep(60)', timeout=1)
        self.assertEqual(self.run_gate(), 1)
        pid = int(pidfile.read_text())
        try:
            self.assertFalse(self.process_alive(pid))
            row = json.loads((self.out / 'receipt.json').read_text())['steps'][0]
            self.assertEqual(row['state'], 'not_measured')
            self.assertIs(row['cleanup_complete'], True)
        finally:
            if self.process_alive(pid):
                os.kill(pid, signal.SIGKILL)

    def test_sigterm_records_interruption_and_reaps_child(self):
        pidfile = self.base / 'child.pid'
        self.make_plan(f'import os,time; from pathlib import Path; '
                       f'Path({str(pidfile)!r}).write_text(str(os.getpid())); time.sleep(60)')
        command = [sys.executable, '-B', str(RUNNER), 'run', '--root', str(self.root),
                   '--out', str(self.out), '--plan', str(self.plan), '--expected-head', self.head]
        runner = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        pid = None
        try:
            deadline = time.monotonic() + 5
            while not pidfile.exists() and runner.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(pidfile.exists())
            pid = int(pidfile.read_text())
            runner.terminate()
            self.assertEqual(runner.wait(timeout=12), 1)
            receipt = json.loads((self.out / 'receipt.json').read_text())
            self.assertTrue(receipt['finished_at'])
            self.assertEqual(receipt['steps'][0]['state'], 'not_measured')
            self.assertIs(receipt['steps'][0]['cleanup_complete'], True)
            self.assertFalse(self.process_alive(pid))
        finally:
            if runner.poll() is None:
                runner.kill()
                runner.wait()
            if pid and self.process_alive(pid):
                os.kill(pid, signal.SIGKILL)

    def test_explicit_worker_tuning_and_isolated_temp(self):
        self.make_plan('import os,sys; from pathlib import Path; '
                       'assert os.environ["CI_DANG_KY_WORKERS"] == "2"; '
                       'assert not sys.stdin.read(); '
                       'assert Path(os.environ["TMPDIR"]).parent == Path(' + repr(str(self.out)) + '); '
                       'print("POSITIVE")')
        plan = json.loads(self.plan.read_text())
        plan['steps'][0]['env'] = {'CI_DANG_KY_WORKERS': '2'}
        self.plan.write_text(json.dumps(plan))
        self.assertEqual(self.run_gate(), 0)
        self.assertEqual(gate.verify(self.out, self.head, self.plan), 0)
        self.assertFalse(list(self.out.glob('probe-*/')))

    def test_receipt_temp_symlink_is_not_followed(self):
        self.out.mkdir()
        victim = self.base / 'victim'
        victim.write_text('untouched')
        (self.out / 'receipt.tmp').symlink_to(victim)
        gate.write_receipt(self.out, {'value': 'new'})
        self.assertEqual(victim.read_text(), 'untouched')
        self.assertEqual(json.loads((self.out / 'receipt.json').read_text()), {'value': 'new'})
        self.assertEqual(list(self.out.glob('receipt.*.tmp')), [])

    def test_both_plans_run_behavior_checks(self):
        for name in ('local_gate_plan.json', 'local_gate_linux_suites.json'):
            plan = gate.read_plan(RUNNER.with_name(name))
            self.assertTrue(any('.claude/dev/local_gate_checks.py' in step['argv']
                                for step in plan['steps']))

    def test_nested_git_config_can_override_abbreviation(self):
        self.make_plan('import subprocess,tempfile; '
                       't=tempfile.TemporaryDirectory(); '
                       'subprocess.run(["git","init","-q",t.name],check=True); '
                       'subprocess.run(["git","-C",t.name,"config","core.abbrev","8"],check=True); '
                       'assert subprocess.check_output(["git","-C",t.name,"config","core.abbrev"],text=True).strip()=="8"; '
                       'print("POSITIVE")')
        self.assertEqual(self.run_gate(), 0)

    def test_scratch_clone_keeps_ignored_writes_outside_source(self):
        (self.root / '.gitignore').write_text('ignored/\n')
        (self.root / 'probe.py').write_text(
            'from pathlib import Path\nimport subprocess\n'
            'Path("ignored").mkdir(); Path("ignored/state").write_text("fixture")\n'
            'subprocess.run(["git","config","core.abbrev","8"],check=True)\n'
            'assert subprocess.check_output(["git","config","core.abbrev"],text=True).strip()=="8"\n'
            'print("POSITIVE")\n')
        self.git('add', '.')
        self.git('-c', 'user.name=test', '-c', 'user.email=test@example.invalid',
                 '-c', 'commit.gpgsign=false', 'commit', '-qm', 'scratch fixture')
        self.head = self.git('rev-parse', 'HEAD').strip()
        self.assertEqual(gate.scratch_run(self.root, [sys.executable, '-B', 'probe.py']), 0)
        self.assertFalse((self.root / 'ignored').exists())
        self.assertEqual(gate.identity(self.root)['head'], self.head)


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(RunnerChecks))
    passed = result.wasSuccessful() and result.testsRun > 0 and not result.skipped
    if passed:
        print(f'LOCAL_GATE_CHECKS_PASS {result.testsRun}/{result.testsRun}')
    raise SystemExit(0 if passed else 1)
