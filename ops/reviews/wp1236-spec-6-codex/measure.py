import ast
import collections
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'repo'
OUT = BASE / 'work'
os.environ['GIT_OPTIONAL_LOCKS'] = '0'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(OUT)
import yaml

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode()

def save(name, data):
    data = {'measured_at': datetime.datetime.now(datetime.timezone.utc).isoformat(), **data}
    (OUT / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    return data

def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def claims(obj, path='$'):
    if isinstance(obj, dict):
        for k, v in obj.items():
            norm = ''.join(c for c in str(k).casefold() if c.isalnum())
            at = path + '.' + str(k)
            if 'gateoutput' in norm and norm not in ('gateoutputnguon','gateoutputnguonvagioihan','mocgateoutputrcdisposition'):
                yield at, v
            yield from claims(v, at)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            yield from claims(v, path + f'[{i}]')

def census():
    source = load_module(ROOT / 'ops/land_evidence_nguon.py', 'source_gate')
    land = load_module(ROOT / 'ops/kiem_ho_so_land.py', 'land_gate')
    c = collections.Counter()
    cat = collections.Counter()
    breakdown = collections.Counter()
    details = []
    records = []
    for p in sorted((ROOT/'ops/land').glob('*-land-evidence.yaml')):
        doc = yaml.safe_load(p.read_bytes())
        cs = list(claims(doc))
        c['records'] += 1
        c['root_merge_commit'] += 'merge_commit' in doc
        c['claims'] += len(cs)
        c['records_with_claims'] += bool(cs)
        for _,v in cs:
            typ = 'mapping' if isinstance(v,dict) else 'list' if isinstance(v,list) else 'other'
            if isinstance(v,str):
                m = re.match(r'\s*([a-z_]+)(?=$|[\s—\-:(,.;])', v.casefold())
                typ = m[1] if m and m[1] in ('measured','passed','not_measured') else 'other_string'
            cat[typ] += 1
        provdir = p.with_name(p.name.removesuffix('-land-evidence.yaml')+'-provenance')
        n_prov = 0
        if provdir.is_dir():
            for q in sorted(provdir.rglob('*.yaml')):
                try:
                    prov = yaml.safe_load(q.read_bytes())
                except Exception:
                    continue
                if not isinstance(prov,dict) or prov.get('schema') != 'ci_provenance/1':
                    continue
                n_prov += 1
                run = prov['moc']['run']
                key = run.get('event','?') + '|' + run.get('loi_khai_rest_path','?')
                breakdown[key] += 1
                jobs = prov['moc']['gate_output']['jobs']
                details.append({'file':str(q.relative_to(ROOT)), 'run':run.get('run_id'), 'event':run.get('event'),
                                'workflow':run.get('loi_khai_rest_path'), 'head':run.get('head_sha'),
                                'job_count':len(jobs), 'non_skipped':sum(j.get('conclusion')!='skipped' for j in jobs)})
        c['provenance_records'] += bool(n_prov)
        c['provenance_files'] += n_prov
        status, reason, landed = land._xet_mot_tep(p,yaml)
        c['landed'] += landed
        c['landed_DAT'] += status=='DAT'
        c['landed_without_claims'] += landed and not cs
        c['l5_matching'] += source.MIEN_TRU_CUTOVER.get(p.name)==hashlib.sha256(p.read_bytes()).hexdigest()
        c['l5_lost'] += p.name in source.MIEN_TRU_CUTOVER and source.MIEN_TRU_CUTOVER[p.name]!=hashlib.sha256(p.read_bytes()).hexdigest()
        records.append({'file':p.name,'claims':len(cs),'provenance_files':n_prov,'landed':landed,'status':status})
    result=save('census', {'counts':dict(c),'claim_values':dict(cat),'q7':dict(breakdown),'files':details,'records':records})
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','records')},ensure_ascii=False,indent=2))

def sizes():
    paths=['ops/ci_provenance.py','ops/ci_provenance_test.py','ops/land_evidence_nguon.py',
           'ops/land_evidence_nguon_test.py','ops/kiem_ho_so_land.py','ops/kiem_ho_so_land_test.py']
    rows=[]
    for path in paths:
        oid=git('log','--diff-filter=A','--format=%H','--',path).splitlines()[-1]
        rows.append({'path':path,'created_commit':oid,'numstat':git('diff-tree','--root','--no-commit-id','--numstat','-r',oid,'--',path).strip()})
    prototypes={str(p.relative_to(ROOT)):len(p.read_text().splitlines()) for p in [
        ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py',ROOT/'ops/land/pr1127-wp1120-provenance/ci/tom_gate_output.py']}
    text=(BASE/'SPEC.md').read_text()
    block=text.split('```yaml\nnang_tran:\n',1)[1].split('```',1)[0]
    parsed=yaml.safe_load('nang_tran:\n'+block)
    result=save('size', {'creation_numstat':rows,'prototype_lines':prototypes,'a1_component_estimate':250+450+1,
                        'estimate_range':[580,760],'cap':800,'nang_tran':parsed})
    print(json.dumps(result,ensure_ascii=False,indent=2))

def checks():
    rows=[]
    commands=[
        [sys.executable,'-B','ops/land_evidence_nguon.py','--root','.'],
        [sys.executable,'-B','ops/kiem_ho_so_land.py','--root','.'],
        [sys.executable,'-B','.claude/dev/packet_loop.py','--state-dir',str(OUT/'state'),'doctrine-scan','--root','.'],
    ]
    for i,cmd in enumerate(commands):
        p=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        output=OUT/f'check-{i}.txt'
        output.write_text(p.stdout)
        rows.append({'command':cmd,'rc':p.returncode,'output':str(output),'sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'tail':p.stdout.splitlines()[-3:]})
    print(json.dumps(save('checks',{'checks':rows}),ensure_ascii=False,indent=2))

if __name__=='__main__':
    {'census':census,'sizes':sizes,'checks':checks}[sys.argv[1]]()
