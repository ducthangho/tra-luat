"""Gỡ riêng từng chốt chưa có trong m73–m82, chạy tất cả ca CA sẵn có."""
import importlib.util
import json
from pathlib import Path

ROOT = Path('/tmp/wp960-mutations')
PRODUCT = ROOT / 'ops/bien_nhan_v2.py'
SOURCE = PRODUCT.read_text()
MUTATIONS = [
    ('r1-moc-khong-doi-oid40',
     'if not moc or not _HEX40.match(moc):', 'if not moc:'),
    ('r2-luot-bien-nhan-khac-thieu',
     'if luot_nay is None or any(lu is None for _, lu in sau):', 'if luot_nay is None:'),
    ('r3-merge-base-loi-thanh-vi-pham',
     '                        if rc != 0:\n                            chua.setdefault(k, f"{ten}: `{duong}` — `merge-base` rc={rc} cho `{x}`")\n                            continue\n', ''),
    ('r4-run-json-thieu-surface-thanh-vi-pham',
     '        if not s_that:\n            sf_chua.append(f"{ten}: `{rj}` không đọc được `execution_surface` — L-SURFACE không áp")\n            continue\n', ''),
    ('r5-moc-blame-hong-thanh-vi-pham',
     '    if them is None:\n        return None\n', '    if them is None:\n        return False\n'),
    ('r6-chi-so-origin-HEAD',
     'for ref in ("refs/remotes/origin/HEAD", "refs/remotes/origin/master", "refs/heads/master"):',
     'for ref in ("refs/remotes/origin/HEAD",):'),
]

def load():
    s = importlib.util.spec_from_file_location('tests', ROOT / 'ops/bien_nhan_v2_test.py')
    t = importlib.util.module_from_spec(s); s.loader.exec_module(t)
    return t

try:
    for name, old, new in MUTATIONS:
        assert SOURCE.count(old) == 1, (name, SOURCE.count(old))
        PRODUCT.write_text(SOURCE.replace(old, new))
        t = load()
        red = []; passed = 0
        print('BEGIN', name, flush=True)
        for fn in t.CA:
            status, details = t._chay_1(fn)
            if status == 'qua': passed += 1
            else: red.append([fn.__name__, status, details])
        print('RESULT', name, json.dumps({'passed': passed, 'total': len(t.CA), 'red': red}, ensure_ascii=False), flush=True)
finally:
    PRODUCT.write_text(SOURCE)
