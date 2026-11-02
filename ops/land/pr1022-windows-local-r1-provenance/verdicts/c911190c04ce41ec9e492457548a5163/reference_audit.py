import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
OUT = ROOT / 'evidence'
GATES = [
    'ops/lease_publish.py', '.claude/dev/packet_loop.py', '.claude/dev/launcher.py',
    '.claude/dev/gate_lifecycle.py', '.github/workflows/ci.yml', '.github/workflows/ops-publish-lease.yml',
]
TOKENS = r'KHOA\.txt|do-luong\.csv|list_devices|không đo local|0057|WINDOWS-LOCAL-MAY-CHU-KHO'
COMMANDS = [
    (['git', 'rev-parse', '--verify', '1cc847d^{commit}'], 0),
    (['git', 'rev-parse', '--verify', 'e9967f0^{commit}'], 0),
    (['git', 'show', '-s', '--format=%H %s', '96667715996d41bc45e70a64fbaa8996de20f6a0'], 0),
    (['git', 'log', '--all', '--format=%H %s', '--extended-regexp', '--grep=(#1020|#1010|#1014|#1017|#1006)'], 0),
    (['git', 'diff', 'd8d5571e7c1669360eba672f2547d14081039b9b^1',
      'd8d5571e7c1669360eba672f2547d14081039b9b', '--', '.claude/dev/packet_loop_test.py'], 0),
    (['rg', '-n', TOKENS, *GATES], 1),
    (['rg', '-n', '--hidden', '-g', '!.git/**', '-g', '*.py', '-g', '*.yml', '-g', '*.yaml', '-g', '*.ps1',
      '-g', '*.sh', '-g', '*.cmd', '-g', '*.bat', '-g', '!**/reviews/**',
      r'KHOA\.txt|do-luong\.csv|list_devices|không đo local', '.'], 1),
    (['rg', '-n', '-e', '^def t192_S8', '-e', '^def t27_', '-e', '^def c91_',
      '-e', '^def c93_', '-e', '^def c96_', '-e', '^def _r929_xoa_blob',
      'ops/lease_publish_test.py', 'ops/bien_nhan_v2_test.py', '.claude/dev/packet_loop_test.py',
      '.claude/dev/launcher_test.py'], 0),
    (['git', 'remote', 'get-url', 'origin'], 0),
    (['git', 'config', '--get', 'core.abbrev'], 0),
    (['python3', '--version'], 0),
    (['git', '--version'], 0),
    (['uname', '-sr'], 0),
]
results = []
for command, expected in COMMANDS:
    p = subprocess.run(command, cwd=REPO, capture_output=True,
                       env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0', 'PYTHONDONTWRITEBYTECODE': '1'})
    result = {'command': command, 'cwd': str(REPO), 'rc': p.returncode,
              'stdout': p.stdout.decode('utf-8', errors='replace'),
              'stderr': p.stderr.decode('utf-8', errors='replace')}
    results.append(result)
    assert p.returncode == expected, result
(OUT / 'reference-audit.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'commands_recorded': len(results), 'gate_search_rc': results[5]['rc'],
                  'gate_hits': results[5]['stdout'].splitlines(),
                  'broader_code_search_rc': results[6]['rc'],
                  'broader_code_hits': results[6]['stdout'].splitlines(),
                  'commit_refs_verified': [results[0]['stdout'].strip(), results[1]['stdout'].strip()],
                  'origin': results[8]['stdout'].strip()}, ensure_ascii=False))
