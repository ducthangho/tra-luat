import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1] / 'cay-kho'
head = 'f37b5195978f1fe35b9cb55b6f79a2e09d165af0'
source = 'a34b9a38cda2669f9a90958c69bb6f2faa0f4353'
def blob(oid, path):
    return subprocess.check_output(['git', '-C', str(root), 'show', oid + ':' + path])
def sha(data):
    return hashlib.sha256(data).hexdigest()

for n in (1, 2):
    folder = f'ops/reviews/wp1037-g1-codex-luot{n}'
    for target, original in [('PROMPT.md', f'luot{n}-PROMPT.md'), ('VERDICT.md', f'luot{n}-VERDICT-codex.md'), ('run/run.json', f'luot{n}-run.json')]:
        path = folder + '/' + target
        actual = (root / path).read_bytes()
        raw = blob(source, 'ops/handoff/wp1037-g1-claude/' + original)
        print(f'ROUND {n} {target} bytes={len(actual)} sha256={sha(actual)} SOURCE_EQUAL={raw == actual} HEAD_EQUAL={blob(head, path) == actual}')
    flat = f'ops/reviews/wp1037-g1-codex-luot{n}-verdict.md'
    actual = (root / flat).read_bytes()
    print(f'ROUND {n} FLAT bytes={len(actual)} sha256={sha(actual)} DIRECTORY_EQUAL={actual == (root / folder / "VERDICT.md").read_bytes()} SOURCE_EQUAL={actual == blob(source, "ops/handoff/wp1037-g1-claude/" + f"luot{n}-VERDICT-codex.md")} HEAD_EQUAL={actual == blob(head, flat)}')
    run = json.loads((root / folder / 'run/run.json').read_text())
    checkpoint = json.loads((root / folder / 'run/checkpoint.json').read_text())
    for name, hash_key, bytes_key in [('stdout.log', 'stdout_sha256', 'stdout_byte'), ('stderr.log', 'stderr_sha256', 'stderr_byte'), ('checkpoint.json', 'checkpoint_sha256', None)]:
        actual = (root / folder / 'run' / name).read_bytes()
        print(f'ROUND {n} {name} hash_match={sha(actual) == run[hash_key]} bytes={len(actual)} declared_bytes={run.get(bytes_key)} bytes_match={not bytes_key or len(actual) == run[bytes_key]}')
    print('ROUND', n, 'CHECKPOINT', json.dumps(checkpoint, ensure_ascii=False, sort_keys=True))

for folder in ['ops/reviews/wp1037-g1-codex-luot1', 'ops/reviews/wp1037-g1-codex-luot2', 'ops/land/pr1041-wp1037-provenance']:
    directory = root / folder
    entries = {}
    for line in (directory / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        name = name.lstrip('*')
        normalized = Path(name).as_posix().removeprefix('./')
        print('MANIFEST', folder, normalized, 'OK' if sha((directory / name).read_bytes()) == digest else 'MISMATCH')
        entries[normalized] = digest
    files = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file() and p.name != 'SHA256SUMS'}
    print('MANIFEST_SET', folder, 'entries', len(entries), 'files', len(files), 'MISSING', sorted(files - entries.keys()), 'EXTRA', sorted(entries.keys() - files))

prefix = 'ops/handoff/wp1037-g1-claude/'
names = subprocess.check_output(['git', '-C', str(root), 'ls-tree', '-r', '--name-only', source, '--', prefix], text=True).splitlines()
print('SOURCE_DIRECTORY_FILES', names)
manifest = blob(source, prefix + 'SHA256SUMS').decode()
for line in manifest.splitlines():
    digest, name = line.split(maxsplit=1)
    print('SOURCE_MANIFEST', name, sha(blob(source, prefix + name.removeprefix('./'))) == digest)
