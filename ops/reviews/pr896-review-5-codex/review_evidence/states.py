from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys
import yaml

from audit import BASE, ROOT, SHA, MASTER, PARENT, record

def rc(*a):
    return subprocess.run(['git', '-C', str(ROOT), *a], capture_output=True).returncode

def full(oid):
    return subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', oid]).decode().strip()

def yaml_field(p, names):
    node = yaml.compose(p.read_text())
    for name in names:
        if isinstance(node, yaml.SequenceNode):
            node = node.value[int(name)]
        else:
            node = next(v for k,v in node.value if k.value == name)
    return node.start_mark.line + 1, node.value

def ancestry():
    patched = []
    for p in sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml')):
        d = yaml.safe_load(p.read_text())
        fields = [str(v) for v in d.get('anchor', {}).values()]
        fields += [c.get('mo_ta', '') for c in d.get('verdict_usage_caveats', [])]
        for s in fields:
            m = re.search(r'git merge-base --is-ancestor ([0-9a-f]{40}) 101263f', s)
            if m:
                anchor = re.search(r'commit ghi bien nhan ([0-9a-f]{40}):', s)
                patched.append({'receipt': p.name, 'oid': m[1], 'anchor': anchor[1] if anchor else None})
                break
    extra = yaml.safe_load((ROOT / 'ops/reviews/pr896-review-4-legacy-caveats.yaml').read_text())
    c = extra['caveats'][0]
    m = re.search(r'git merge-base --is-ancestor ([0-9a-f]{40}) 101263f', c['mo_ta'])
    patched.append({'receipt': Path(c['receipt_path']).name, 'oid': m[1], 'anchor': None})
    targets = ['101263f', '2e4183b', MASTER, SHA]
    for entry in patched:
        entry['ancestor_rc'] = {t: rc('merge-base', '--is-ancestor', entry['oid'], t) for t in targets}
        if entry['anchor']:
            entry['anchor_receipt_exists_rc'] = rc('cat-file', '-e', entry['anchor'] + ':ops/reviews/' + entry['receipt'])
    selected = [
        ('ci-windows-review-5-claude-verdict.receipt.yaml', ['chuoi_verdict_ghi_chu'], 'c2f6898'),
        ('doctrine-scan-review-1-claude-verdict.receipt.yaml', ['anchor','gioi_han'], 'bc5d0c6'),
        ('doctrine-scan-review-2-claude-verdict.receipt.receipt.yaml'.replace('.receipt.receipt', '.receipt'), ['anchor','gioi_han'], '80d8161'),
        ('doctrine-scan-review-3-claude-verdict.receipt.yaml', ['anchor','gioi_han'], '7d8bb69'),
        ('wp538-review-1-claude-verdict.receipt.yaml', ['anchor','gioi_han'], 'ab27f78'),
        ('wp538-review-2-claude-verdict.receipt.yaml', ['anchor','gioi_han'], 'ab27f78'),
        ('wp540-review-1-claude-verdict.receipt.yaml', ['anchor','gioi_han'], 'ab27f78'),
    ]
    residual = []
    for name, keys, oid in selected:
        p = ROOT / 'ops/reviews' / name
        line, value = yaml_field(p, keys)
        residual.append({'receipt': name, 'field': '.'.join(keys), 'line': line, 'text': value, 'oid': full(oid), 'ancestor_rc': {t: rc('merge-base', '--is-ancestor', oid, t) for t in [MASTER, SHA]}})
    chain = yaml.safe_load((ROOT / 'ops/reviews/ci-windows-review-5-claude-verdict.receipt.yaml').read_text())
    chain_values = next(v for k,v in chain.items() if isinstance(v, list) and len(v) == 5 and all(isinstance(x,dict) and 'luot' in x and 'sha' in x for x in v))
    allfive = {full(x['sha']): {t: rc('merge-base', '--is-ancestor', x['sha'], t) for t in [MASTER, SHA]} for x in chain_values}
    exclusions = {o: {t: rc('merge-base', '--is-ancestor', o, t) for t in [MASTER, SHA]} for o in ['4bc9432','604b8d9','2e4183b','82359c4']}
    details = {'patched': patched, 'residual': residual, 'ci_windows_all_five': allfive, 'exclusions': exclusions}
    (BASE / 'ancestry-details.json').write_text(json.dumps(details, ensure_ascii=False, indent=2) + '\n')
    lines = [f'old_23_receipts={len(patched)} checks={len(patched)*len(targets)} all_rc0={all(all(r == 0 for r in x["ancestor_rc"].values()) for x in patched)}',
             f'historical_receipt_anchors_exist={sum(x.get("anchor_receipt_exists_rc") == 0 for x in patched)}/{sum(bool(x["anchor"]) for x in patched)}',
             'residual_unanchored_fields=' + str(len(residual))]
    for x in residual:
        lines.append(x['receipt'] + ':' + str(x['line']) + ' ' + x['field'] + ' oid=' + x['oid'] + ' rc(master,candidate)=' + str(list(x['ancestor_rc'].values())))
        lines.append('TEXT ' + x['text'])
    lines.append('ci_windows_five_verdict_blob_oids=' + json.dumps(allfive))
    lines.append('excluded_or_historical=' + json.dumps(exclusions))
    record('HƯỚNG 6 - ancestry va truong con sot', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py ancestry', '\n'.join(lines), 'LỖI P1 phu-nhan-ancestry-chi-tren-nhanh-da-cu còn 7 receipt: bản vá neo đúng trường đã chọn nhưng bỏ trường khác. Không suy landed/assurance từ ancestry. 4bc9432 và 604b8d9 không phải ancestor master; hai head PR947 cũng chưa là ancestor master, không báo những câu tương ứng là sai.')

def reviews():
    patched = []
    for p in sorted((ROOT / 'ops/reviews').glob('*.receipt.yaml')):
        d = yaml.safe_load(p.read_text())
        for c in d.get('verdict_usage_caveats', []):
            s = c.get('mo_ta', c.get('noi_dung', ''))
            m = re.search(r'Sau moc ay, (\S+-verdict.md) da review ban va tai ([0-9a-f]{40})', s)
            if not m:
                continue
            anchor = re.search(r'commit ghi bien nhan ([0-9a-f]{40}):', s)[1]
            v = ROOT / 'ops/reviews' / m[1]
            r = yaml.safe_load((ROOT / 'ops/reviews' / m[1].replace('.md', '.receipt.yaml')).read_text())
            patched.append({'receipt': p.name, 'anchor': anchor, 'next_verdict': m[1], 'next_reviewed_sha': m[2], 'receipt_sha_matches': r['reviewed_sha'] == m[2], 'verdict_sha_matches': any('reviewed_sha' in l and m[2] in l for l in v.read_text().splitlines()[:15]), 'hash_matches': hashlib.sha256(v.read_bytes()).hexdigest()==r['verdict_sha256'], 'next_verdict_at_anchor_rc': rc('cat-file','-e',anchor+':ops/reviews/'+m[1])})
    residual = []
    for number, oid in [('870','06a50c5'), ('889','094e8d1')]:
        p = ROOT / f'ops/reviews/pr{number}-review-1-codex-verdict.receipt.yaml'
        d = yaml.safe_load(p.read_text())
        caveat_index = next(i for i,c in enumerate(d['verdict_usage_caveats']) if c['id'] == 'HEAD-MERGE-CHUA-REVIEW-LAI')
        locations = {}
        for keys in [['assurance_ghi_chu'], ['verdict_usage_caveats',str(caveat_index),'mo_ta']]:
            line, text = yaml_field(p, keys)
            locations['.'.join(keys)] = {'line': line, 'text': text}
        nextverdicts = []
        for turn in [2,3]:
            v = ROOT / f'ops/reviews/pr{number}-review-{turn}-codex-verdict.md'
            r = yaml.safe_load(v.with_suffix('.receipt.yaml').read_text())
            nextverdicts.append({'path': str(v.relative_to(ROOT)), 'reviewed_sha': r['reviewed_sha'], 'matches_oid': r['reviewed_sha']==full(oid), 'verdict': r['verdict'], 'hash_matches': hashlib.sha256(v.read_bytes()).hexdigest()==r['verdict_sha256']})
        readme = (ROOT / 'ops/reviews/README.md').read_text().splitlines()
        rows = [{'line': i, 'text': l} for i,l in enumerate(readme,1) if (l.startswith('| `pr'+number+'-review-1-codex-verdict.md` | `HEAD-MERGE-CHUA-REVIEW-LAI` |') or l.startswith('| [`pr'+number+'-review-1-codex-verdict.md`]'))]
        residual.append({'receipt': p.name,'locations':locations,'readme':rows,'later_reviews':nextverdicts})
    details = {'old_eight': patched, 'residual': residual}
    (BASE / 'review-states.json').write_text(json.dumps(details,ensure_ascii=False,indent=2)+'\n')
    lines = [f'old_review_caveats_historically_anchored={len(patched)} all_next_sha_and_hash_match={all(x["receipt_sha_matches"] and x["verdict_sha_matches"] and x["hash_matches"] for x in patched)}']
    for x in patched:
        lines.append('OLD '+x['receipt']+' anchor='+x['anchor']+' next='+x['next_verdict']+' reviewed='+x['next_reviewed_sha']+' next_verdict_exists_at_anchor_rc='+str(x['next_verdict_at_anchor_rc']))
    for x in residual:
        lines.append('RESIDUAL '+x['receipt'])
        for k,v in x['locations'].items(): lines.append(k+':'+str(v['line'])+' '+v['text'])
        for row in x['readme']: lines.append('README:'+str(row['line'])+' '+row['text'])
        for v in x['later_reviews']: lines.append('LATER '+json.dumps(v,ensure_ascii=False))
    record('HƯỚNG 7 - trang thai da review', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews', '\n'.join(lines), 'LỖI P1 trang-thai-chua-review-da-bi-verdict-sau-bac: 8/8 thể hiện cũ được neo lịch sử đúng, nhưng còn PR870/PR889 lượt 1 ở assurance, caveat và README. Cả lượt 2 và lượt 3 đã review đúng head bản vá. Giữ nguyên verdict lịch sử và assurance; đây không phải quyền land.')

if __name__ == '__main__':
    {'ancestry': ancestry, 'reviews': reviews}[sys.argv[1]]()
