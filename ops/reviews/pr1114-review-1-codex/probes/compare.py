import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
base = json.loads((root / 'evidence/base-case-ids.json').read_text())
head = json.loads((root / 'evidence/head-case-ids.json').read_text())
for key in base:
    missing = sorted(set(base[key]) - set(head[key]))
    added = sorted(set(head[key]) - set(base[key]))
    print(key, 'base=' + str(len(base[key])), 'head=' + str(len(head[key])),
          'missing=' + str(missing), 'added=' + str(added),
          'same_order=' + str(base[key] == head[key]))
    assert not missing and not added
for version in ('base', 'head'):
    log = (root / 'evidence' / (version + '.log')).read_text()
    assert 'CA: 52/52 dat' in log and 'DOT BIEN: 80/80 bi giet dung ly do' in log
    assert 'TONG: DAT' in log and 'BO QUA' not in log
print('BASE_PASS_SET_PRESERVED=PASS')
