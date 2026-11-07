import ast
import collections
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys
import yaml

ROOT = Path(__file__).resolve().parent.parent / 'repo'
WORK = Path(__file__).resolve().parent

def mod(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True)

def walk(obj, path='$'):
    if isinstance(obj, dict):
        for k,v in obj.items():
            yield str(k),v,path+'.'+str(k)
            yield from walk(v,path+'.'+str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):
            yield from walk(v,f'{path}[{i}]')

def sha40(x):
    return isinstance(x,str) and re.fullmatch('[0-9a-f]{40}',x)

def census():
    le = mod('land_evidence_nguon', 'ops/land_evidence_nguon.py')
    kh = mod('kiem_ho_so_land', 'ops/kiem_ho_so_land.py')
    docs = [(p,yaml.safe_load(p.read_text())) for p in sorted((ROOT/'ops/land').glob('*-land-evidence.yaml'))]
    prov = []
    keycounts=collections.Counter(); valuecounts=collections.Counter()
    formats=collections.defaultdict(set); cited=[]; misses=[]; roots=0; multis=[]; empty=[]
    claimdocs=set(); nonnm=set(); exemptions=[]; landed=[]; withclaims=[]
    for p,d in docs:
        directory=p.with_name(p.name.replace('-land-evidence.yaml','-provenance'))
        ps=[]
        for q in sorted(directory.rglob('*.yaml')):
            z=yaml.safe_load(q.read_text())
            if isinstance(z,dict) and z.get('schema')=='ci_provenance/1':
                ps.append((q,z)); prov.append((p,q,z))
        h={d['merge_commit']} if sha40(d.get('merge_commit')) else set()
        roots += bool(h)
        extra={v['merge_commit'] for v in d.get('prs',[]) if isinstance(v,dict) and sha40(v.get('merge_commit'))}
        h |= extra
        if extra: multis.append((p.name, len(h), sorted(h)))
        tt,_,island=kh._xet_mot_tep(p,yaml)
        if island:
            landed.append(p.name)
            if not h: empty.append(p.name)
        claims=[]
        for k,v,path in walk(d):
            canon=''.join(c for c in k.casefold() if c.isalnum())
            if 'gateoutput' not in canon: continue
            keycounts[k] += 1
            if canon in {'gateoutputnguon','gateoutputnguonvagioihan','mocgateoutputrcdisposition'}: continue
            claims.append((v,path)); claimdocs.add(p.name)
            token=re.match(r'\s*([a-z_]+)(?=$|[\s—\-:(,.;])',v.casefold()) if isinstance(v,str) else None
            token=token[1] if token else type(v).__name__ if not isinstance(v,str) else 'other'
            valuecounts[token]+=1
            if token!='not_measured': nonnm.add(p.name)
            if token in {'measured','passed'} and ps:
                for t in le.token_nguon(v):
                    if 'gate-output' not in t and 'kiem-gate' not in t: continue
                    target=le.phan_giai(t,ROOT,directory,p)
                    if not target or not target.is_file():
                        misses.append((p.name,path,t)); continue
                    s=target.read_text(errors='replace')
                    fmt='danh_gia' if re.search(r'^MOC_GATE_OUTPUT: \S+ \(\d+/\d+',s,re.M) else 'tom' if re.search(r'^JOB \d+ .*sha256=[0-9a-f]{64} ##\[error\]=\d+',s,re.M) else 'tu_do'
                    formats[p.name].add(fmt); cited.append((p.name,t,fmt))
        if island and claims: withclaims.append(p.name)
        if p.name in nonnm and p.name in le.MIEN_TRU_CUTOVER:
            exemptions.append((p.name,hashlib.sha256(p.read_bytes()).hexdigest()==le.MIEN_TRU_CUTOVER[p.name]))
    push=collections.Counter(); states=collections.Counter(); exact=0; dupsteps=[]; windows_same=set()
    for p,q,z in prov:
        r=z['moc']['run']; jobs=z['moc']['gate_output']['jobs']
        if r['event']=='push': push[(r['loi_khai_rest_path'],len(jobs))]+=1
        states.update(j['trang_thai'] for j in jobs)
        exact += {str(j['job_id']) for j in jobs if j['conclusion']!='skipped'}==set(map(str,z['log_day_du']))
        for j in jobs:
            ns=[s['name'] for s in j.get('buoc',[])]
            if len(ns)!=len(set(ns)): dupsteps.append((q.name,j['job_id']))
        d=dict(docs)[p]
        if r['head_sha']==d.get('merge_commit') and any('windows-latest' in j['labels'] for j in jobs): windows_same.add(p.name)
    result={'time':datetime.datetime.now(datetime.timezone.utc).isoformat(),'total_docs':len(docs),'root_merge_count':roots,'multi_pr_heads':multis,'landed_empty_H':empty,'provenance_docs':len({p for p,q,z in prov}),'provenance_files':len(prov),'push':{str(k):v for k,v in push.items()},'states':dict(states),'job_log_sets_equal':exact,'duplicate_steps':dupsteps,'windows_same_root_head':sorted(windows_same),'claim_key_counts':dict(keycounts),'claim_value_counts':dict(valuecounts),'claim_docs':len(claimdocs),'nonnm_docs':len(nonnm),'exemptions':exemptions,'L8_retrospective':len(nonnm)-sum(v for _,v in exemptions),'landed':len(landed),'landed_with_claims':len(withclaims),'formats':{k:[sum(k in vs for vs in formats.values()),sum(vs=={k} for vs in formats.values())] for k in ('danh_gia','tom','tu_do')},'format_details':{k:sorted(v) for k,v in formats.items()},'unresolved_citations':misses}
    (WORK/'census.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False,indent=2))

def k7():
    cp=mod('ci_provenance','ops/ci_provenance.py')
    tree=ast.parse((ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text())
    scope={}
    for node in tree.body:
        if isinstance(node,ast.Assign) and any(isinstance(n,ast.Name) and n.id in {'JSON_OK','TL_SELFTEST','TL_SELFTEST_PATS','LUAT'} for n in node.targets):
            exec(compile(ast.Module(body=[node],type_ignores=[]),'rules','exec'),scope)
    p=yaml.safe_load((ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_text())
    shas={v['sha'] for v in p['moc']['checkout'] if v['trang_thai']=='passed'}
    assert len(shas)==1
    sha=next(iter(shas)); wf=cp.doc_wf(git('show',sha+':.github/workflows/ci.yml'))
    base=cp.doc_wf(git('show','3163f4d:.github/workflows/ci.yml'))
    J=[j for j in p['moc']['gate_output']['jobs'] if j['conclusion']!='skipped' and 'ubuntu-latest' in j['labels'] and j['name']!='chuan-bi']
    details=[]; unpaired=[]; envdiff=[]; ogjobs=set(); newjobs=set(); pipes=[]
    for j in J:
        key=cp.ghep_job(j['name'],wf)
        rule=next(v for prefix,v in scope['LUAT'] if j['name'].startswith(prefix))
        for label,pats in rule:
            def matches(s):
                return ('tl.py --selftest' if label==scope['TL_SELFTEST'] else label) in s.get('run','')
            sy=[(i,s) for i,s in enumerate(wf['jobs'][key]['steps']) if matches(s)]
            rest={s['name']:s['conclusion'] for s in j['buoc']}
            sy=[(i,s) for i,s in sy if rest.get(cp.ten_du_kien(s))=='success']
            if len(sy)!=1:
                unpaired.append((j['name'],label,[(i,s.get('name')) for i,s in sy])); continue
            i,s=sy[0]; job=wf['jobs'][key]
            sb=[x for x in base['jobs'][key]['steps'] if matches(x) and x.get('name')==s.get('name')]
            assert len(sb)==1,(key,label,sb)
            allowed=set(sb[0].get('env',{}))
            if set(s.get('env',{}))!=allowed: envdiff.append((key,s['name'],sorted(s.get('env',{})),sorted(allowed)))
            why=[]
            if 'defaults' in wf or 'defaults' in job: why.append('defaults')
            if cp._env_chan(wf) or cp._env_chan(job): why.append('_env_chan')
            if set(s)-cp.KHOA_BUOC-{'env'}: why.append('extra_keys')
            if 'env' in s and (type(s['env']) is not dict or set(s['env'])-allowed): why.append('env_step')
            if s.get('shell','bash') not in ('bash','pwsh','sh'): why.append('shell')
            if any(re.search('GITHUB_(ENV|PATH)',str(t.get('run',''))) for t in job['steps'][:i]): why.append('prior_env_path')
            if s.get('continue-on-error',False) is not False: why.append('continue_on_error')
            old=cp.chan_buoc(wf,key,i)
            if old: ogjobs.add(j['name'])
            if why: newjobs.add(j['name'])
            lex=shlex.shlex(s.get('run',''),posix=False,punctuation_chars='|'); lex.whitespace_split=True
            tokens=list(lex)
            haspipe=any(t and set(t)=={'|'} for t in tokens)
            if haspipe:
                pipewhy=s.get('shell') in (None,'sh') and not any(t in s['run'] for t in ('set -o pipefail','set -euo pipefail'))
                pipes.append((j['name'],s['name'],s.get('shell'),pipewhy))
            details.append({'job':j['name'],'step':s['name'],'env_keys':sorted(allowed),'old_block':old,'r4_block':why,'pipe':haspipe})
    info={'checkout':sha,'T':len(p['moc']['gate_output']['jobs']),'J':len(J),'matched_steps':len(details),'unpaired':unpaired,'env_differences':envdiff,'old_blocked_jobs':len(ogjobs),'old_blocked_steps':sum(s['old_block'] for s in details),'r4_blocked_jobs':len(newjobs),'r4_blocked_steps':sum(bool(s['r4_block']) for s in details),'pipe_steps':pipes,'unique_env_sets':sorted({(s['step'],tuple(s['env_keys'])) for s in details if s['env_keys']}),'details':details}
    (WORK/'k7.json').write_text(json.dumps(info,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in info.items() if k!='details'},ensure_ascii=False,indent=2))

if __name__=='__main__':
    {'census':census,'k7':k7}[sys.argv[1]]()
