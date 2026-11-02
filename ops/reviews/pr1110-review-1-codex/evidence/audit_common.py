import hashlib
import json
import os
import subprocess
from pathlib import Path

S = Path(__file__).resolve().parent
REPO = S / 'cay-kho'
SOURCE = S / 'nguon/review1075a'
E = S / 'evidence'
E.mkdir(exist_ok=True)
HEAD = 'e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d'
BASE = 'c6dd7b33b4f215809bf281ee1533bc1e8fa6920c'
ARCHIVE = 'ops/reviews/pr1075-review-1-codex'
RECEIPT = ARCHIVE + '-verdict.receipt.yaml'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_OPTIONAL_LOCKS='0',
           GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='core.abbrev', GIT_CONFIG_VALUE_0='7')

def run(args, cwd=REPO):
    return subprocess.run(args, cwd=cwd, env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def git(*args, cwd=REPO):
    p = run(['git', *args], cwd)
    if p.returncode:
        raise RuntimeError((args, p.returncode, p.stderr.decode()))
    return p.stdout

def sha(b):
    return hashlib.sha256(b).hexdigest()

def save(name, data):
    (E / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')

def snapshot():
    # Include .git as well as every working-tree file; no writes to reviewed repository.
    records = []
    for p in sorted(REPO.rglob('*')):
        if p.is_symlink():
            records.append([str(p.relative_to(REPO)), 'symlink', os.readlink(p)])
        elif p.is_file():
            b = p.read_bytes()
            records.append([str(p.relative_to(REPO)), len(b), sha(b)])
    return records
