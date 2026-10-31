from datetime import datetime
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import yaml

root = Path(__file__).resolve().parents[1] / 'cay-kho'
sys.path.insert(0, str(root / 'ops'))
spec = importlib.util.spec_from_file_location('review_lease_publish', root / 'ops/lease_publish.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
source = 'a34b9a38cda2669f9a90958c69bb6f2faa0f4353'
raw = subprocess.check_output(['git', '-C', str(root), 'show', source + ':ops/leases/wp1037-r1-g1-claude.yaml'])
snapshot = (root / 'ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt').read_bytes()
lease = yaml.safe_load(raw)
print('LEASE_SOURCE_EQUAL', raw == snapshot, 'sha256', hashlib.sha256(raw).hexdigest())
for stamp in ['2026-10-30T17:37:00Z', '2026-10-30T17:41:02Z', '2026-10-30T17:53:00Z', '2026-10-30T18:07:34Z', '2026-10-30T18:08:52Z']:
    print('CLASSIFY', stamp, module._phan_loai_lease(lease, bay_gio=datetime.fromisoformat(stamp)))
print('SHORTENING', lease['lease_sua_lan_cuoi'], lease['lease_until'], lease['lease_expires_at_utc'])
log = (root / 'ops/land/pr1041-wp1037-provenance/ai-dang-giu-sau-rut-han/luc-do.txt').read_text()
print('AFTER_EXPIRY_LOG_SHA256', hashlib.sha256(log.encode()).hexdigest())
print('AFTER_EXPIRY_LOG_BEGIN\n' + log + 'AFTER_EXPIRY_LOG_END')
for n in ['wp1037-r1-g1-claude', 'wp1021-r2-g1-claude']:
    ref = 'refs/remotes/origin/ops/' + n.removesuffix('-claude') + '-lease'
    oid = subprocess.check_output(['git', '-C', str(root), 'rev-parse', ref], text=True).strip()
    data = yaml.safe_load(subprocess.check_output(['git', '-C', str(root), 'show', oid + ':ops/leases/' + n + '.yaml']))
    print('LOG_SUBJECT', n, 'ref_oid', oid, 'expires', data['lease_expires_at_utc'], 'AT_180734', module._phan_loai_lease(data, bay_gio=datetime.fromisoformat('2026-10-30T18:07:34Z')))
refs = subprocess.check_output(['git', '-C', str(root), 'for-each-ref', '--format=%(refname) %(objectname) %(symref)', 'refs/remotes/origin'], text=True).splitlines()
real = [r for r in refs if not r.startswith('refs/remotes/origin/HEAD ')]
print('OFFLINE_REF_NAMES', len(real), 'PLUS_HEAD_ALIAS', len(refs) - len(real))
print('REMOTE_SERVER_REF_SET_AT_180734', 'KHONG_DO_DUOC_OFFLINE: log chi luu summary 708/708, khong luu danh sach ten/OID may chu')
print('SPEC_SHA256', hashlib.sha256(subprocess.check_output(['git', '-C', str(root), 'show', source + ':ops/specs/wp1037.md'])).hexdigest())
