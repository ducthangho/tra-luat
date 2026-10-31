from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import yaml

root = Path(__file__).resolve().parents[1] / 'cay-kho'
head = 'f37b5195978f1fe35b9cb55b6f79a2e09d165af0'
merge = 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93'
source = 'a34b9a38cda2669f9a90958c69bb6f2faa0f4353'
lease = yaml.safe_load((root / 'ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt').read_text())
def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()
for n in (1, 2):
    base = f'ops/reviews/wp1037-g1-codex-luot{n}'
    r = yaml.safe_load((root / (base + '-verdict.receipt.yaml')).read_text())
    run = json.loads((root / base / 'run/run.json').read_text())
    v = (root / r['verdict_path']).read_bytes()
    lines = v.decode().splitlines()
    print('ROUND', n, 'RECEIPT_KEY_SET', sorted(r))
    for k, expected in [('schema_version', 2), ('kind', 'review_delivery_receipt'), ('target_pull_request', 1041), ('land_merge_commit', merge), ('role', 'reviewer'), ('provider', 'codex'), ('executor_provider', 'claude'), ('cross_provider', True), ('review_class', 'sensitive'), ('effective_review_class', 'sensitive'), ('independent_from_executor_session', True), ('so_dem_theo', 'finding'), ('nguon_tep', 'ban_sao_nguyen_byte_cua_tep_goc_trong_kho')]:
        print('ROUND', n, 'FIELD', k, repr(r.get(k)), 'MATCH', r.get(k) == expected)
    for k in ['packet_id', 'packet_issue', 'revision', 'generation', 'lease_id']:
        print('ROUND', n, 'LEASE_FIELD', k, repr(r.get(k)), 'MATCH', r.get(k) == lease[k])
    normalized = lines[0].split(':', 1)[1].strip().replace('request_changes', 'changes_requested')
    counts = Counter(re.findall(r'^- \[(P[0-3])\]', v.decode(), flags=re.M))
    print('ROUND', n, 'VERDICT', lines[0], 'NORMALIZED_MATCH', r['verdict'] == normalized, 'COUNTS', {f'P{i}': counts[f'P{i}'] for i in range(4)}, 'COUNTS_MATCH', all(r[f'so_p{i}'] == counts[f'P{i}'] for i in range(4)))
    print('ROUND', n, 'FINDINGS_IDS', r['findings_ids'])
    print('ROUND', n, 'REVIEWED_SHA_MATCH', r['reviewed_sha'] == lines[1].split(':', 1)[1].strip() == run['head'], 'TREE', git('rev-parse', r['reviewed_sha'] + '^{tree}'), 'LEASE_BASE', lease['base_sha'])
    print('ROUND', n, 'OPTIONAL_FIELDS', {k: r.get(k, 'ABSENT') for k in ['reviewed_tree', 'base_sha', 'muc_bang_chung_model']})
    print('ROUND', n, 'VERDICT_HASH_MATCH', hashlib.sha256(v).hexdigest() == r['verdict_sha256'], 'BYTES_MATCH', len(v) == r['verdict_bytes'], 'RECEIPT_ID_HASH_SUFFIX', r['receipt_id'].endswith(r['verdict_sha256'][:8]))
    anchor_oid, anchor_path = r['evidence_url'].split('/blob/', 1)[1].split('/', 1)
    actual = subprocess.check_output(['git', '-C', str(root), 'show', anchor_oid + ':' + anchor_path])
    print('ROUND', n, 'EVIDENCE_URL', r['evidence_url'], 'BLOB_EQUAL', actual == v, 'ANCHOR', r['anchor'])
    for a, b in [(anchor_oid, head), (r['reviewed_sha'], merge), (lease['base_sha'], r['reviewed_sha'])]:
        p = subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', a, b])
        print('ROUND', n, 'ANCESTRY', a, b, 'rc', p.returncode)
    m = r['model_reviewer_identity']
    for k, key in [('provider', 'provider'), ('surface', 'execution_surface'), ('transport', 'transport'), ('session_run_id', 'run_id')]:
        print('ROUND', n, 'IDENTITY', k, m[k], 'RUN_MATCH', m[k] == run[key])
    print('ROUND', n, 'MODEL_FIELDS', {k: m.get(k) for k in ['model_yeu_cau', 'model', 'model_da_chay', 'model_evidence', 'model_evidence_ref']})
    print('ROUND', n, 'MEASURED_MODELS', run['model_phuc_vu_trang_thai'], len(run['model_phuc_vu']), dict(Counter(x['model'] for x in run['model_phuc_vu'])), 'EFFORT', run['effort_phuc_vu_trang_thai'], run['effort_phuc_vu'])
    print('ROUND', n, 'RUNTIME', {k: run.get(k) for k in ['run_id', 'head', 'trang_thai', 'ma_thoat', 'thoi_luong_giay', 'worktree_sach', 'so_muc_ban', 'prompt_sha256', 'sandbox_trang_thai', 'sandbox_gioi_han']})
    print('ROUND', n, 'PROMPT_HASH_MATCH', run['prompt_sha256'] == hashlib.sha256((root / base / 'PROMPT.md').read_bytes()).hexdigest())
    print('ROUND', n, 'START_IN_LEASE', datetime.fromisoformat(lease['leased_at_utc']) <= datetime.fromisoformat(run['bat_dau_utc']) < datetime.fromisoformat(lease['lease_expires_at_utc']))
    print('ROUND', n, 'LENH_METADATA', run['lenh'], 'CLI_VERSION_FIELDS', [k for k in run if 'cli_version' in k or 'argv' in k])
    print('ROUND', n, 'ASSURANCE', r['assurance'], 'EXECUTOR_MODEL', lease['model'], lease['model_family'])
    print('ROUND', n, 'CAVEATS', json.dumps(r['verdict_usage_caveats'], ensure_ascii=False))
print('MERGE_HEAD_PARENT', git('rev-parse', merge + '^2'))
normalized = sorted(unicodedata.normalize('NFC', x).casefold() for x in lease['write_set'])
print('WRITE_SET_HASH', hashlib.sha256(json.dumps(normalized, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest(), 'EXPECTED', lease['write_set_hash'])
print('BOOKKEEPING_HEAD_IN_MASTER_RC', subprocess.run(['git', '-C', str(root), 'merge-base', '--is-ancestor', head, merge]).returncode)
