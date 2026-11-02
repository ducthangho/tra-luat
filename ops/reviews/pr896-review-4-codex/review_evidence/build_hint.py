"""Derive a documentation-only hint in scratch; never write cay-kho/."""
import difflib
import json
from pathlib import Path
import re
import subprocess
import yaml

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'cay-kho'
SCRATCH = Path('/tmp/pr896-r4-audit-9b8d9a76/hint-result')
SHA = '2e4183bc2dc40e6bc306e377fc442ff0f405bbe0'
states = json.loads((BASE / 'review_evidence/proven-states.json').read_text())
texts = {}
original = {}
legacy = []

def read(rel):
    if rel not in texts:
        p = ROOT / rel
        original[rel] = p.read_text() if p.exists() else ''
        texts[rel] = original[rel]
    return texts[rel]

def node_for(node, path):
    for key in path:
        if isinstance(node, yaml.SequenceNode):
            node = node.value[key]
        else:
            node = next(v for k, v in node.value if k.value == key)
    return node

def replace_scalar(rel, path, value):
    text = read(rel)
    node = node_for(yaml.compose(text), path)
    if not isinstance(node, yaml.ScalarNode):
        raise ValueError(path)
    old = text[node.start_mark.index:node.end_mark.index]
    suffix = re.search(r'\n(?:[ \t]*\n)*$', old)
    new = json.dumps(value, ensure_ascii=False) + (suffix[0] if suffix else '')
    texts[rel] = text[:node.start_mark.index] + new + text[node.end_mark.index:]
    yaml.safe_load(texts[rel])

README = 'ops/reviews/README.md'

def caveat_row(verdict, cid, description):
    text = read(README)
    prefix = f'| `{verdict}` | `{cid}` | '
    rows = [l for l in text.splitlines() if l.startswith(prefix)]
    replacement = prefix + description + ' |'
    if len(rows) == 1:
        texts[README] = text.replace(rows[0], replacement, 1)
    elif not rows:
        marker = '\n## Mục lục\n'
        if text.count(marker) != 1:
            raise ValueError('README section')
        texts[README] = text.replace(marker, replacement + '\n' + marker, 1)
    else:
        raise ValueError(rows)

for item in states['review']:
    rel = 'ops/reviews/' + item['receipt']
    d = yaml.safe_load(read(rel))
    idx, c = next((i, c) for i, c in enumerate(d['verdict_usage_caveats']) if c['id'] == item['id'])
    field = 'mo_ta' if 'mo_ta' in c else 'noi_dung'
    description = (f"Anh chup lich su tai commit ghi bien nhan {item['introduced']}: {c[field]} "
                   f"Sau moc ay, {item['next_verdict']} da review ban va tai {item['next_reviewed_sha']}. "
                   "Vi vay cau CHUA review/Chua dong o tren chi thuoc moc lich su; doc ket qua dong/mot phan/loi moi "
                   "trong verdict ke tiep, khong suy thanh approve hay quyen land.")
    replace_scalar(rel, ['verdict_usage_caveats', idx, field], description)
    caveat_row(Path(d['verdict_path']).name, c['id'], description)

for item in states['ancestry']:
    rel = 'ops/reviews/' + item['receipt']
    d = yaml.safe_load(read(rel))
    correction = (f"Do lai tai {SHA}: git merge-base --is-ancestor {item['oid']} 101263f va voi 2e4183b deu rc=0. "
                  "Cau phu nhan ancestry/chi-tren-nhanh cua moc cu khong con la trang thai hien hanh. "
                  "Chi xac nhan quan he Git, khong tu nang assurance/cuong_do va khong suy Packet da landed.")
    prefix = f"Anh chup lich su tai commit ghi bien nhan {item['introduced']}: "
    if item['schema'] == 1:
        legacy.append(dict(receipt_path=rel, verdict_path=d['verdict_path'], verdict_sha256=d['verdict_sha256'],
                           id='ANCESTRY-CHI-TREN-NHANH-LA-TRANG-THAI-LICH-SU', mo_ta=correction))
        caveat_row(Path(d['verdict_path']).name, legacy[-1]['id'], correction + ' Dinh chinh bo sung: pr896-review-4-legacy-caveats.yaml; receipt v1 giu nguyen.')
        continue
    name = item['receipt']
    paths = []
    if name.startswith('wp678-spec-'):
        paths.append(['spec_ghi_chu'])
        idx = next(i for i,c in enumerate(d['verdict_usage_caveats']) if c['id'] == 'REVIEWED-SHA-CHI-TREN-NHANH-SPEC')
        paths.append(['verdict_usage_caveats', idx, 'mo_ta'])
    elif name.startswith(('doctrine-scan-', 'wp538-', 'wp540-')):
        paths.append(['anchor', 'mo_ta'])
    else:
        paths.append(['anchor', 'gioi_han'])
    if name == 'pr508-review-5-codex-verdict.receipt.yaml':
        idx = next(i for i,c in enumerate(d['verdict_usage_caveats']) if c['id'] == 'ANCHOR-cuong_do-trung_binh-vi-PR-CHUA-MERGE')
        paths.append(['verdict_usage_caveats', idx, 'mo_ta'])
    for path in paths:
        curr = yaml.safe_load(read(rel))
        old = curr
        for key in path:
            old = old[key]
        new = prefix + old + ' ' + correction
        replace_scalar(rel, path, new)
        if path[0] == 'verdict_usage_caveats':
            c = curr['verdict_usage_caveats'][path[1]]
            caveat_row(Path(d['verdict_path']).name, c['id'], new)

# The new surface caveat does not choose between incompatible declarations.
cid = 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC'
rel = 'ops/reviews/pr526-review-3-codex-verdict.receipt.yaml'
description = ("Verdict dong 151 tu khai Codex service, receipt model_reviewer_identity.surface ghi codex_cli "
               "(run ID khai f466d135 / f466d135534244c1b888c9c0c44811b9). Day la hai loi khai khac nhau; "
               "checkout tai 2e4183b khong kem run.json cua chinh luot de phan xu runtime. "
               "Khong chon be mat truoc khi co bang chung dung run; giu nguyen byte verdict, khong chung thuc model/effort hay nang assurance.")
texts[rel] = read(rel).rstrip() + '\n\n' + yaml.safe_dump({'verdict_usage_caveats':[{'id':cid,'muc':'P2','mo_ta':description}]}, allow_unicode=True, sort_keys=False)
caveat_row('pr526-review-3-codex-verdict.md', cid, description)
rel = 'ops/reviews/slice-b-c-review-2-codex-verdict.receipt.yaml'
d = yaml.safe_load((ROOT / rel).read_text())
description = ("Verdict dong 19 tu khai Codex service; dong 6 va verdict_nguon cua receipt v1 ghi codex exec qua launcher, "
               "run ID khai 8ddb0c6f. Khong co run.json dung run trong checkout tai 2e4183b de phan xu hai loi khai. "
               "Khong chon be mat, khong chung thuc model/effort hay nang assurance; giu byte verdict va receipt v1 dong bang.")
legacy.append(dict(receipt_path=rel, verdict_path=d['verdict_path'], verdict_sha256=d['verdict_sha256'], id=cid, muc='P2', mo_ta=description))
caveat_row('slice-b-c-review-2-codex-verdict.md', cid, description + ' Dinh chinh bo sung: pr896-review-4-legacy-caveats.yaml.')
rel = 'ops/reviews/pr896-review-4-legacy-caveats.yaml'
read(rel)
texts[rel] = yaml.safe_dump(dict(kind='supplementary_historical_caveats', measured_at_sha=SHA,
                               ghi_chu='Dinh chinh tai lieu; khong phai review delivery receipt hay authority. Khong sua receipt v1 dong bang.',
                               caveats=legacy), allow_unicode=True, sort_keys=False)

# Fix the current-status clauses of the index, retaining historical verdicts.
text = read(README)
old = 'P1 luot 2 DA DONG; moi: P1 wp766 tu khai `codex_service` chua caveat, P1 ho so luot 2 van khai HINT chua ap, P2 13 verdict service/API lech receipt CLI — HINT.patch luot 3 chua ap'
new = ("Tai reviewed_sha 82359c4: P1 luot 2 DA DONG; finding moi luc ay la P1 wp766, P1 ho so luot 2 va P2 13 verdict service/API. "
       "HINT.patch luot 3 da ap tai 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0 (sau c8c1ee0); can verdict moi tren exact SHA ung vien")
if text.count(old) != 1:
    raise ValueError('r3 index')
text = text.replace(old, new, 1)
old = 'P2 `t162-khong-khoa-toan-bo-ma-tran-job` va o `3bc4244` bang nguyen HINT.patch, CHUA review lai'
new = 'P2 `t162-khong-khoa-toan-bo-ma-tran-job` va o `3bc4244`; CHUA review tai moc ghi so 2789cbb, sau do DA DONG theo pr896-review-2 tai 8d56009; giu verdict lich su'
if text.count(old) != 1:
    raise ValueError('r1 index')
text = text.replace(old, new, 1)
old = 'P1: verdict luot 2 #870/#889 khai sai surface `codex_service` chua co caveat — da ap HINT.patch, chua review lai'
new = 'Tai reviewed_sha 2789cbb: P1 hai verdict luot 2 #870/#889 thieu caveat; HINT da ap tai a9bc934; pr896-review-2 tai 8d56009 da kiem hai the hien nay DA DONG (lop luc ay con pr889 luot 1, duoc luot 3 kiem tai 82359c4); khong suy approve/land'
if text.count(old) != 1:
    raise ValueError('pr915 index')
texts[README] = text.replace(old, new, 1)

rel = 'ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml'
texts[rel] = read(rel).rstrip() + '\n\n' + yaml.safe_dump({'cap_nhat_review_4_moc_lich_su': {
    'measured_at_sha': SHA,
    'ghi_chu': 'Cau CHUA review lai trong cap_nhat_20261026.cross_review_moi.do_duoc la anh chup luc ghi so truoc luot 2, khong phai trang thai tai 2e4183b. pr896-review-2 da review ban va P2 3bc4244 va caveat a9bc934 tai 8d56009; P2 t162 va hai the hien P1 luot 2 #870/#889 DA DONG. Luot 3 tai 82359c4 kiem them caveat pr889 luot 1. Ket qua cac verdict van changes_requested; khong suy approve/land hay thay don vi land de xuat.'}}, allow_unicode=True, sort_keys=False)

SCRATCH.mkdir(parents=True, exist_ok=True)
patch = '# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'
for rel in sorted(texts):
    if texts[rel] == original[rel]:
        continue
    p = SCRATCH / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texts[rel])
    patch += ''.join(difflib.unified_diff(original[rel].splitlines(keepends=True), texts[rel].splitlines(keepends=True),
                                        fromfile=rel if original[rel] else '/dev/null', tofile=rel))
    print(rel)
(BASE / 'HINT.patch').write_text(patch)
print('changed_files=', sum(texts[k] != original[k] for k in texts))
