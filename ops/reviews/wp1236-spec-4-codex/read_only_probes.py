"""Read existing data/import existing modules only; no generated attack fixtures."""
from pathlib import Path
import importlib.util
import json
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent / 'repo'
sys.path.insert(0, str(ROOT))

def watch():
    return sorted(n for n in sys.modules if n.startswith(('kiem_ho_so_land', 'land_evidence_nguon')))

print('A22 baseline:', watch())
import ops.kiem_ho_so_land
print('A22 after ordinary package import:', watch())
print('Actually loaded:', 'ops.kiem_ho_so_land' in sys.modules)
spec = importlib.util.spec_from_file_location('kiem_ho_so_land_canon', ROOT / 'ops/kiem_ho_so_land.py')
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)
print('Dynamic loader has working checker:', callable(checker._url_hop_le))
print('A22 after dynamic file import:', watch())

p = ROOT / 'ops/land/pr1130-wp1122-provenance/readback-duyet-issuecomment-6635057729.json'
r = json.loads(p.read_text())
d = yaml.safe_load((ROOT / 'ops/land/pr1130-wp1122-land-evidence.yaml').read_text())
expected = 'https://github.com/ducthangho/tra-luat/pull/1130#issuecomment-6635057729'
conditions = {
    'html_url': r['html_url'] == expected,
    'user.login': r['user']['login'] == 'ducthangho',
    'author_association': r['author_association'] == 'OWNER',
    'body_contains_merge_sha': d['merge_commit'] in r['body'],
}
print('Existing readback:', p.relative_to(ROOT))
print('R4 four readback conditions:', conditions)
print('Existing readback body:', r['body'])

for i,line in enumerate((ROOT / '.claude/dev/packet_loop.py').read_text().splitlines(), 1):
    if line.startswith('CHECK_BAT_BUOC ='):
        print('Required checks:', i, line)
