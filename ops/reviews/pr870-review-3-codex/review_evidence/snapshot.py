import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

entries = {}
for root, directories, files in os.walk('.'):
    if root == '.':
        directories[:] = [d for d in directories if d != '.git']
    for name in files:
        path = Path(root) / name
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        entries[str(path)] = hashlib.sha256(data).hexdigest()
result = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
          'tree': subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], text=True).strip(),
          'status': subprocess.check_output(['git', 'status', '--porcelain', '--ignored'], text=True),
          'index_sha256': hashlib.sha256(Path('.git/index').read_bytes()).hexdigest(),
          'diff': subprocess.check_output(['git', 'diff', 'HEAD'], text=True), 'files': entries}
destination = Path(sys.argv[1])
if not destination.exists():
    destination.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True))
    print(f'INITIAL head={result["head"]} tree={result["tree"]} files={len(entries)} status={result["status"]!r} diff={result["diff"]!r} index_sha256={result["index_sha256"]}')
else:
    original = json.loads(destination.read_text())
    delta = [k for k in sorted(set(original['files']) | set(entries)) if original['files'].get(k) != entries.get(k)]
    print(f'FINAL head={result["head"]} tree={result["tree"]} files={len(entries)} status={result["status"]!r} changed_paths={delta}')
    print(f'whole_snapshot_equal={original == result} index_equal={original["index_sha256"] == result["index_sha256"]}')
    assert original == result
