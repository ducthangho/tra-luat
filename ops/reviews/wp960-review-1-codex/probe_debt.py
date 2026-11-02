import importlib.util
import json
from collections import Counter
from pathlib import Path

root = Path('/tmp/wp960-review-copy')
s = importlib.util.spec_from_file_location('b', root / 'ops/bien_nhan_v2.py')
b = importlib.util.module_from_spec(s); s.loader.exec_module(b)
loi, tk = b.kiem(root, no_cau_lich_su=frozenset())
print('empty-debt', json.dumps({'rc': b._ma_thoat(loi, tk), 'errors': len(loi),
    'rules': dict(Counter(x.split(']')[0] + ']' for x in loi)),
    'unknown': tk['chua_do'], 'set_equal': set(tk['vi_pham_cau']) == b.NO_CAU_LICH_SU}, ensure_ascii=False))
source = (root / 'ops/bien_nhan_v2.py').read_text()
start = source.index('NO_CAU_LICH_SU: frozenset = frozenset({')
frozen = source[start:source.index('\n})', start) + 3]
import subprocess
r = subprocess.run(['python3', str(root / 'ops/bien_nhan_v2.py'), '--root', str(root), '--sinh-no-cau-lich-su'],
                   capture_output=True, text=True)
print('generate', json.dumps({'rc': r.returncode, 'exact_block_equal': r.stdout.strip() == frozen,
                             'stderr': r.stderr.strip()}, ensure_ascii=False))
Path('/tmp/claude-0/rv/wp960-review-1-codex/generated-debt.txt').write_text(r.stdout)

base = Path('/tmp/wp960-base')
s = importlib.util.spec_from_file_location('base', base / 'ops/bien_nhan_v2.py')
old = importlib.util.module_from_spec(s); s.loader.exec_module(old)
print('base-before', json.dumps({'has_new_rules': hasattr(old, '_kiem_cau_lich_su'),
                                'has_debt': hasattr(old, 'NO_CAU_LICH_SU'),
    'new_cases_found': __import__('re').findall(r'^def c(?:69|70|71|72|73|74|75|76)_', (base / 'ops/bien_nhan_v2_test.py').read_text(), __import__('re').M)}))
head_code = (root / 'ops/bien_nhan_v2.py').read_text()
(base / 'ops/bien_nhan_v2.py').write_text(head_code)
try:
    s = importlib.util.spec_from_file_location('new_on_base', base / 'ops/bien_nhan_v2.py')
    nb = importlib.util.module_from_spec(s); s.loader.exec_module(nb)
    for label, debt in [('default', None), ('empty', frozenset())]:
        errors, stats = nb.kiem(base, no_cau_lich_su=debt)
        print('base-with-head-code-' + label, json.dumps({'rc': nb._ma_thoat(errors, stats),
          'errors': len(errors), 'debt': stats['no_cau'], 'unknown': stats['chua_do'],
          'violations': len(stats['vi_pham_cau']),
          'set_equal_head': set(stats['vi_pham_cau']) == b.NO_CAU_LICH_SU}, ensure_ascii=False))
finally:
    # Chỉ bản sao base bị đổi; khôi phục bằng blob exact base.
    (base / 'ops/bien_nhan_v2.py').write_bytes(subprocess.check_output(['git', '-C', str(base), 'show', 'HEAD:ops/bien_nhan_v2.py']))
