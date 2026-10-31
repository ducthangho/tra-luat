import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

sandbox = Path(__file__).resolve().parent.parent
repo = sandbox / 'cay-kho'
evidence = sandbox / 'review_evidence'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def run(args):
    p = subprocess.run(args, cwd=repo, env=env, capture_output=True)
    return {'command': args, 'rc': p.returncode, 'stdout': p.stdout.decode('utf-8', 'replace'), 'stderr': p.stderr.decode('utf-8', 'replace')}

def snapshot():
    files = {}
    for folder, dirs, names in os.walk(repo):
        dirs[:] = sorted(d for d in dirs if d != '.git')
        for name in sorted(names):
            path = Path(folder) / name
            rel = path.relative_to(repo).as_posix()
            if path.is_symlink():
                files[rel] = {'symlink': os.readlink(path)}
            else:
                files[rel] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'mode': path.stat().st_mode & 0o777}
    return {'head': run(['git', 'rev-parse', 'HEAD']), 'tree': run(['git', 'rev-parse', 'HEAD^{tree}']), 'status': run(['git', 'status', '--porcelain=v1', '--untracked-files=all', '--ignored']), 'index': run(['git', 'ls-files', '--stage']), 'diff': run(['git', 'diff', '--binary', 'HEAD']), 'files': files}

before = snapshot()
(evidence / 'snapshot-before.json').write_text(json.dumps(before, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
checks = [
    ('doctrine-scan', ['python3', '.claude/dev/packet_loop.py', 'doctrine-scan', '--root', '.']),
    ('adr-song', ['python3', '.claude/dev/packet_loop.py', 'adr-song', '--root', '.']),
    ('doc-claims-check', ['python3', 'scripts/tl.py', 'doc-claims-check', '--json']),
]

def check(item):
    name, args = item
    result = run(args)
    (evidence / (name + '.stdout')).write_text(result['stdout'], encoding='utf-8')
    (evidence / (name + '.stderr')).write_text(result['stderr'], encoding='utf-8')
    (evidence / (name + '.rc')).write_text(str(result['rc']) + '\n', encoding='utf-8')
    record = {'name': name, **result, 'cwd': str(repo), 'env': {'PYTHONDONTWRITEBYTECODE': '1'}}
    if name == 'doc-claims-check':
        data = json.loads(result['stdout'])
        summary = {k: data[k] for k in ['ok', 'files_scanned', 'claims_flagged', 'flags', 'advisory_count', 'layers_skipped']}
    else:
        summary = result['stdout'].strip()
    return record, {'name': name, 'rc': result['rc'], 'stderr': result['stderr'], 'summary': summary}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(check, checks))
(evidence / 'checks.json').write_text(json.dumps([r[0] for r in results], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
after = snapshot()
(evidence / 'snapshot-after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
report = {'environment': {'platform': platform.platform(), 'python': sys.version.split()[0], 'pwsh': shutil.which('pwsh'), 'powershell': shutil.which('powershell')}, 'checks': [r[1] for r in results], 'snapshots_equal': before == after, 'files_hashed': len(before['files']), 'head': after['head']['stdout'].strip(), 'tree': after['tree']['stdout'].strip(), 'status': after['status']['stdout']}
(evidence / 'summary.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
