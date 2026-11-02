import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import yaml
from audit import BASE, SHA, MASTER, record

copy = Path((BASE/'copy-path.txt').read_text().strip())
assert subprocess.check_output(['git','-C',str(copy),'rev-parse','HEAD']).decode().strip() == SHA
assert not subprocess.check_output(['git','-C',str(copy),'status','--porcelain=v1']).strip()
readme = copy/'ops/reviews/README.md'
originals = {readme:readme.read_bytes()}
ancestry = json.loads((BASE/'ancestry-details.json').read_text())['residual']
reviewstates = json.loads((BASE/'review-states.json').read_text())['residual']

def replace_scalar(path, keys, new):
    if path not in originals:
        originals[path] = path.read_bytes()
    text = path.read_text()
    node = yaml.compose(text)
    for key in keys:
        if isinstance(node, yaml.SequenceNode):
            node = node.value[int(key)]
        else:
            node = next(v for k,v in node.value if k.value == key)
    # PyYAML includes the trailing newline in a block scalar's source range.
    tail_newline = '\n' if text[node.start_mark.index:node.end_mark.index].endswith('\n') else ''
    path.write_text(text[:node.start_mark.index]+json.dumps(new,ensure_ascii=False)+tail_newline+text[node.end_mark.index:])

results = []
try:
    for x in ancestry:
        p = copy/'ops/reviews'/x['receipt']
        d = yaml.safe_load(p.read_text())
        anchor = re.search(r'commit ghi bien nhan ([0-9a-f]{40}):',yaml.safe_dump(d['anchor'],allow_unicode=True))[1]
        desc = 'Anh chup lich su tai commit ghi bien nhan '+anchor+': '+x['text']+' Do lai tai '+SHA+': git merge-base --is-ancestor '+x['oid']+' '+MASTER+' va voi '+SHA+' deu rc=0. Vi vay menh de phu nhan ancestry/chi-tren-nhanh cua moc cu o tren khong con la trang thai hien hanh. Chi xac nhan quan he Git cua OID nay; giu cuong_do/assurance lich su, khong suy Packet da landed hay trang thai cac verdict khac.'
        replace_scalar(p,x['field'].split('.'),desc)
    for x in reviewstates:
        p = copy/'ops/reviews'/x['receipt']
        number = re.search(r'pr(\d+)-',p.name)[1]
        ref = {'870':'600b6ce','889':'e02d0c3'}[number]
        anchor = subprocess.check_output(['git','-C',str(copy),'rev-parse',ref]).decode().strip()
        oid = x['later_reviews'][0]['reviewed_sha']
        sequel = ' Sau moc ay, pr'+number+'-review-2-codex-verdict.md va pr'+number+'-review-3-codex-verdict.md da review dung '+oid+' (deu approve 0/0/0/0). Cau chua/khong review lai chi thuoc moc lich su; khong doi verdict, byte hay assurance cua luot 1, khong suy quyen merge/land.'
        new_caveat = None
        for field,info in x['locations'].items():
            new = 'Anh chup lich su tai commit ghi bien nhan '+anchor+': '+info['text']+sequel
            replace_scalar(p,field.split('.'),new)
            if 'verdict_usage_caveats' in field:
                new_caveat = new
        text = readme.read_text()
        oldrow = next(row['text'] for row in x['readme'] if row['text'].startswith('| `'))
        fields = oldrow.split(' | ')
        newrow = ' | '.join(fields[:2]+[new_caveat+' |'])
        assert oldrow in text
        text=text.replace(oldrow,newrow,1)
        oldindex = next(row['text'] for row in x['readme'] if row['text'].startswith('| [`'))
        assert 'KHONG review lai' in oldindex
        newindex = oldindex.replace('KHONG review lai','CHUA review tai moc '+anchor+'; sau do luot 2 va 3 da review dung '+oid+' (deu approve 0/0/0/0); giu ket qua/assurance luot 1, khong suy quyen land',1)
        assert oldindex in text
        readme.write_text(text.replace(oldindex,newindex,1))
    for p in originals:
        if p.suffix=='.yaml':
            d=yaml.safe_load(p.read_text())
            ids=[c['id'] for c in d.get('verdict_usage_caveats',[])]
            assert len(ids)==len(set(ids))
    patch='# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'
    modified={p:p.read_bytes() for p in originals}
    for p in sorted(originals):
        path=p.relative_to(copy).as_posix()
        patch+=''.join(difflib.unified_diff(originals[p].decode().splitlines(keepends=True),modified[p].decode().splitlines(keepends=True),fromfile=path,tofile=path,n=3))
    hint=BASE.parent/'HINT.patch'
    hint.write_text(patch)
    for p,data in originals.items(): p.write_bytes(data)
    def cmdrun(name,cmd):
        r=subprocess.run(cmd,cwd=copy,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
        (BASE/(name+'.stdout')).write_text(r.stdout)
        (BASE/(name+'.stderr')).write_text(r.stderr)
        if name=='hint-doc-claims':
            conclusion='JSON ok='+str(json.loads(r.stdout).get('ok'))
        else:
            conclusion=' / '.join(r.stdout.splitlines()[-2:])
        item={'name':name,'command':cmd,'rc':r.returncode,'conclusion':conclusion}
        results.append(item)
        print(json.dumps(item,ensure_ascii=False),flush=True)
        return r
    dry=cmdrun('hint-dry-run',['patch','--dry-run','--batch','--fuzz=0','-p0','-i',str(hint)])
    assert dry.returncode==0 and not any(w in dry.stdout+dry.stderr for w in ['FAILED','offset','fuzz'])
    applied=cmdrun('hint-apply',['patch','--batch','--fuzz=0','-p0','-i',str(hint)])
    assert applied.returncode==0
    print('hint_changed_files='+str(len(originals)),flush=True)
    for prefix in ['t26_','t27_','t138_']:
        cmdrun('hint-'+prefix,['python3','ops/lease_publish_test.py','--chi-ca='+prefix])
    cmdrun('hint-bien-nhan-v2',['python3','ops/bien_nhan_v2.py','--root','.'])
    cmdrun('hint-land',['python3','ops/land_evidence_nguon.py','--root','.'])
    cmdrun('hint-doctrine',['python3','.claude/dev/packet_loop.py','doctrine-scan','--root','.'])
    cmdrun('hint-doc-claims',['python3','scripts/tl.py','doc-claims-check','--json'])
    hashes=0
    for p in (copy/'ops/reviews').glob('*.receipt.yaml'):
        d=yaml.safe_load(p.read_text())
        assert hashlib.sha256((copy/d['verdict_path']).read_bytes()).hexdigest()==d['verdict_sha256']
        hashes+=1
    for x in reviewstates:
        d=yaml.safe_load((copy/'ops/reviews'/x['receipt']).read_text())
        c=next(c for c in d['verdict_usage_caveats'] if c['id']=='HEAD-MERGE-CHUA-REVIEW-LAI')
        row=next(l for l in readme.read_text().splitlines() if l.startswith('| `'+x['receipt'].replace('.receipt.yaml','.md')+'` | `HEAD-MERGE-CHUA-REVIEW-LAI` |'))
        assert c['mo_ta'] in row
    (BASE/'hint-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
    record('HƯỚNG 10 - HINT tren ban sao', 'PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py', 'changed_files='+str(len(originals))+'; verified_verdict_hashes='+str(hashes)+'\n'+'\n'.join(x['name']+' rc='+str(x['rc'])+' '+x['conclusion'] for x in results), 'KHÔNG PHẢI LỖI của gợi ý theo phép đo: dry-run --fuzz=0 và áp đều sạch; chỉ đổi 9 receipt v2 và README; không đổi verdict/v1/mã cổng. HINT chưa áp vào cây thật; executor tự áp và tự đo.')
finally:
    for p,data in originals.items(): p.write_bytes(data)
print('copy_status_after_restore='+subprocess.check_output(['git','-C',str(copy),'status','--porcelain=v1']).decode().strip(),flush=True)
