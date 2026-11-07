"""Đối chiếu độc lập hợp đồng K7 với F-that, không phải chạy module A1 chưa tồn tại."""
import ast
import json
from pathlib import Path
import re
import shlex
from measure import ROOT, OUT, git, load_module, save
import yaml

cp = load_module(ROOT/'ops/ci_provenance.py','ci_provenance_probe')
tree=ast.parse((ROOT/'ops/land/pr1231-wp1105-provenance/danh_gia_gate.py').read_text())
assignments=[n for n in tree.body if isinstance(n,ast.Assign)
             and any(isinstance(t,ast.Name) and t.id in ('JSON_OK','TL_SELFTEST','TL_SELFTEST_PATS','LUAT') for t in n.targets)]
namespace={}
exec(compile(ast.Module(body=assignments,type_ignores=[]),'prototype_law_constants','exec'),namespace)
law=namespace['LUAT']
prov=yaml.safe_load((ROOT/'ops/land/pr1231-wp1105-provenance/ci/provenance.yaml').read_bytes())
sha_set={c['sha'] for c in prov['moc']['checkout'] if c['trang_thai']=='passed'}
sha=next(iter(sha_set))
workflow=cp.doc_wf(git('show',sha+':.github/workflows/ci.yml'))
base_workflow=cp.doc_wf(git('show','51d6509:.github/workflows/ci.yml'))
T=[j for j in prov['moc']['gate_output']['jobs'] if j['conclusion']!='skipped']
J=[j for j in T if 'ubuntu-latest' in j['labels'] and j['name']!='chuan-bi']
ENV={'PYTHONIOENCODING','PYTHONUTF8','PYTHONDONTWRITEBYTECODE'}

def selects(marker,step):
    # Các bước nhanh chỉ echo tên các lệnh bỏ qua; không phải bước thực thi luật day_du.
    if str(step.get('name','')).startswith('DUONG_NHANH'):
        return False
    body=step.get('run','')
    return ('tl.py --selftest' in body) if marker==namespace['TL_SELFTEST'] else marker in body

rows=[]
for job in J:
    matches=[r for r in law if job['name'].startswith(r[0])]
    assert len(matches)==1,job['name']
    jobkey=cp.ghep_job(job['name'],workflow)
    for marker,_ in matches[0][1]:
        steps=[(i,s) for i,s in enumerate(workflow['jobs'][jobkey]['steps']) if selects(marker,s)
               and any(b['name']==cp.ten_du_kien(s) and b['conclusion']=='success' for b in job['buoc'])]
        assert len(steps)==1,(job['name'],marker,len(steps))
        i,s=steps[0]
        name=cp.ten_du_kien(s)
        rest=[b for b in job['buoc'] if b['name']==name]
        base=[x for x in base_workflow['jobs'][jobkey]['steps'] if cp.ten_du_kien(x)==name]
        assert len(base)==1
        allowed_env=set(base[0].get('env',{}))
        block=[]
        for level,d in [('workflow',workflow),('job',workflow['jobs'][jobkey])]:
            if 'defaults' in d: block.append(level+':defaults')
            if cp._env_chan(d): block.append(level+':env_dynamic')
            if set(d.get('env',{}))-ENV: block.append(level+':extra_env')
        if set(s)-cp.KHOA_BUOC-{'env'}: block.append('step_keys')
        if not isinstance(s.get('env',{}),dict) or set(s.get('env',{}))-allowed_env: block.append('step_env')
        if s.get('shell','bash') not in ('bash','pwsh','sh'): block.append('shell')
        if s.get('continue-on-error',False) is not False: block.append('continue_on_error')
        if any(re.search(r'GITHUB_(ENV|PATH)',str(x.get('run',''))) for x in workflow['jobs'][jobkey]['steps'][:i]):
            block.append('prior_env_path')
        run=s.get('run','')
        lex=shlex.shlex(run,posix=True,punctuation_chars='|')
        lex.whitespace_split=True
        tokens=list(lex)
        has_pipe=any(t and set(t)=={'|'} for t in tokens)
        pipe_bad=has_pipe and s.get('shell') in (None,'sh') and not any(x in run for x in ('set -o pipefail','set -euo pipefail'))
        rows.append({'job':job['name'],'step':name,'rest_matches':len(rest),'rest_success':bool(rest) and rest[0]['conclusion']=='success',
                     'blocked':block,'pipe_bad':pipe_bad,'old_chan_buoc':cp.chan_buoc(workflow,jobkey,i),
                     'checkout_ok':any(c['job_id']==job['job_id'] and c['trang_thai']=='passed' and c['sha']==sha for c in prov['moc']['checkout'])})

env_observed=set(workflow.get('env',{}))
for job in J:
    env_observed.update(workflow['jobs'][cp.ghep_job(job['name'],workflow)].get('env',{}))
summary={'T':len(T),'J':len(J),'steps':len(rows),'rest_mismatches':sum(x['rest_matches']!=1 or not x['rest_success'] for x in rows),
         'blocked_steps':sum(bool(x['blocked']) for x in rows),'pipe_bad':sum(x['pipe_bad'] for x in rows),
         'checkout_bad':sum(not x['checkout_ok'] for x in rows),'checkout_shas':sorted(sha_set),
         'old_blocked_jobs':len({x['job'] for x in rows if x['old_chan_buoc']}),'env':sorted(env_observed),
         'workflow_diff_to_base':git('diff',sha,'51d6509','--','.github/workflows/ci.yml')}
save('workflow',{'summary':summary,'rows':rows})
print(json.dumps(summary,ensure_ascii=False,indent=2))
