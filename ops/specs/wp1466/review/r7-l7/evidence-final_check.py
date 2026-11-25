from pathlib import Path
import os, sys, json, hashlib, datetime, subprocess, shutil
R = Path.cwd(); O = R / 'out'
os.environ.update(PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(O/'tmp'), GIT_OPTIONAL_LOCKS='0')
print('UTC', datetime.datetime.now(datetime.timezone.utc).isoformat(), flush=True)
dst = O/'registry-negative'
(dst/'.claude').mkdir(parents=True, exist_ok=True)
shutil.copytree(O/'prototype/.claude/dev', dst/'.claude/dev', dirs_exist_ok=True)
p = dst/'.claude/dev/packet_loop_test.py'
original = p.read_text()
anchor = 'if __name__ == "__main__":'
assert original.count(anchor) == 1
p.write_text(original.replace(anchor, 'MUTANTS.update({"r1187_drop_doc_guard": ("a", "b", [])})\n\n' + anchor))
subprocess.run(['git', '-C', str(dst), 'init', '-q'], check=True)
subprocess.run(['git', '-C', str(dst), 'add', '.claude/dev'], check=True)
subprocess.run(['git', '-C', str(dst), '-c', 'user.name=Reviewer', '-c', 'user.email=review@example.invalid', '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-q', '-m', 'Local review fixture'], check=True)
commands = [
    ('REGISTRY_NEGATIVE', [sys.executable, '-B', str(O/'sc/so_dang_ky.py'), str(O/'base'), str(dst)]),
    ('N8_SAME_NEGATIVE', [sys.executable, '-B', str(O/'sc/do_pham_vi.py'), 'test', str(O/'base/.claude/dev/packet_loop_test.py'), str(p)])
]
for label, cmd in commands:
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(label, 'COMMAND', cmd, 'RC', r.returncode, r.stdout.strip(), r.stderr.strip()[-1000:], flush=True)
before = json.loads((O/'source-before.json').read_text())
after = {}
for root in [R/'cay-kho', R/'kho.git']:
    for p in sorted(root.rglob('*')):
        if p.is_symlink(): after[str(p.relative_to(R))] = ['link', os.readlink(p), p.lstat().st_mtime_ns]
        elif p.is_file(): after[str(p.relative_to(R))] = [hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size, p.stat().st_mtime_ns]
(O/'source-after.json').write_text(json.dumps(after, ensure_ascii=False))
delta = [p for p in before.keys() | after.keys() if before.get(p) != after.get(p)]
print('SOURCE_ENTRIES', len(before), len(after), 'SOURCE_DELTA', len(delta), delta[:20], flush=True)
for args in [['status', '--porcelain=v1', '--untracked-files=all'], ['rev-parse', 'HEAD', 'HEAD^{tree}']]:
    r = subprocess.run(['git', '-C', str(R/'cay-kho'), *args], capture_output=True, text=True)
    print('SOURCE_GIT', args, 'RC', r.returncode, repr(r.stdout), repr(r.stderr), flush=True)
print('SPEC_SHA256', hashlib.sha256((R/'cay-kho/ops/specs/wp1466.md').read_bytes()).hexdigest(), flush=True)
