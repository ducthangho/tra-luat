"""Generation 1 + literal K7-S integration MODEL, not production r8 code."""
import ast
import contextlib
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import types
import yaml

W = Path(__file__).resolve().parent
R = W.parent/'repo'
sys.path.insert(0,str(W))
with contextlib.redirect_stdout(io.StringIO()):
    import audit_s0 as audit

def git(*args,cwd=R,data=None):
    return subprocess.check_output(['git',*args],cwd=cwd,input=data).decode().strip()

raw = git('show','508d678:ops/gate_output_doi_chieu.py')
raw = raw.replace('Path(__file__).with_name("ci_provenance.py")',repr(str(R/'ops/ci_provenance.py')))
old = 'elif ly := che_do_shell(str(y.get("run", "")), y.get("shell")):\n                nm.append(f"{ly}:{s[\'name\'][:30]}")'
new = 'elif ly := cu_phap_run(y.get("run"), y.get("shell")):\n                nm.append(f"cu_phap_run:{ly}:{p[\'name\']}:{s[\'name\']}")'
assert raw.count(old)==1
raw=raw.replace(old,new)
lines=raw.splitlines(keepends=True)
remove=set()
for node in ast.parse(raw).body:
    name = node.name if isinstance(node,ast.FunctionDef) else getattr(node.targets[0],'id',None) if isinstance(node,ast.Assign) else None
    if name in {'RE_ONG','RE_TAT_TUY_CHON','RE_CAU_TRUC_SHELL','_bo_nhay','che_do_shell'}:
        remove.update(range(node.lineno-1,node.end_lineno))
raw=''.join(line for i,line in enumerate(lines) if i not in remove)
base=raw+'\n'+audit.core
target='            y, lb = wf["jobs"][k]["steps"][sy[0]], ten_luat.get(s["name"])\n'
assert base.count(target)==1
caller=base.replace(target,target+'            y = dict(y)\n            if type(y.get("run")) is str:\n                y["run"] = unicodedata.normalize("NFC", y["run"])\n')+'\nimport unicodedata\n'
sources={'baseline':base,'rebound_callable':base+audit.normalise,'normalised_step':caller}
mods={}
out={'model':'generation1 + literal K7-S, not an r8 implementation','A14_S0':{}}
for name,src in sources.items():
    mods[name],clauses=audit.check(src)
    (W/('full_'+name+'.py')).write_text(src)
    assert all(clauses), (name,clauses)
    out['A14_S0'][name]=clauses

test=types.ModuleType('fixture_generation1')
test.__file__=str(W/'fixture_generation1.py')
os.environ['GATE_OUTPUT_DOI_CHIEU_GOC']=str(R)
test_src=git('show','508d678:ops/gate_output_doi_chieu_test.py')
exec(compile(test_src,test.__file__,'exec'),vars(test))
test.MA=W/'full_baseline.py'
goc=test.goc()

def commit(wf):
    blob=git('hash-object','-w','--stdin',cwd=goc,data=yaml.safe_dump(wf,allow_unicode=True,sort_keys=False).encode())
    tree=git('mktree',cwd=goc,data=f'100644 blob {blob}\tci.yml\n'.encode())
    tree=git('mktree',cwd=goc,data=f'040000 tree {tree}\tworkflows\n'.encode())
    tree=git('mktree',cwd=goc,data=f'040000 tree {tree}\t.github\n'.encode())
    return git('-c','user.name=review','-c','user.email=review@local','commit-tree',tree,'-p',test.SHA_CK,'-m','scratch fixture',cwd=goc)

wf=yaml.safe_load(test.ci_goc())
rewrite={
    'tl selftest (co bang chung exact-identity)':'bash .github/checks/tl_selftest_bang_chung.sh\n',
    'release-bundle x2 cùng SHA-256':'bash .github/checks/release_bundle_x2.sh\n',
    'G5 manh ban kinh dot bien (#668)':'python ops/cong_cu_test.py\n',
    'lease-publish selftest (đo lại setup sau G5)':'bash ops/chay_lease_publish_test.sh\n',
    'don-nhanh selftest (chốt xoá nhánh)':'pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n',
    'bo ca gate chay TRONG cgroup duoc uy quyen (Linux)':'bash ops/ci/gate_cgroup.sh\n',
}
for j in wf['jobs'].values():
    for step in j['steps']:
        if step.get('name') in rewrite:
            step['run']=rewrite[step['name']]
            if step['name'].startswith('don-nhanh'):step.pop('shell')
sha=commit(wf)
text,original=test.f_ok()
p=copy.deepcopy(original)
for c in p['moc']['checkout']:c['sha']=sha
out['F_ok']={n:m.kiem(text,p,goc) for n,m in mods.items()}
out['F_ok_goc']=mods['baseline'].kiem(text,original,goc)
assert all(v==('passed',[]) for v in out['F_ok'].values())
assert out['F_ok_goc'][0]=='not_measured' and len(out['F_ok_goc'][1])==13

def changed(run,shell):
    change=copy.deepcopy(wf)
    step=next(s for s in change['jobs']['gate-packet-loop']['steps'] if s.get('name')=='packet-loop selftest')
    step['run']=run
    if shell is None:step.pop('shell',None)
    else:step['shell']=shell
    q=copy.deepcopy(p)
    ck=commit(change)
    for c in q['moc']['checkout']:c['sha']=ck
    return q


out["registry_cases"] = {}
for label, before, after in (
    ("e_prime", '(sum(m[1] is None for m in mien) != 1)', 'False'),
    ("f", '(len(ds) != len(set(ds)))', 'False'),
    ("g", 'not set(CHECK_BAT_BUOC) <= set(ds)', 'False'),
    ("h", 'len(_muc(v, t)) != 1', 'len(_muc(v, t)) > 1'),
    ("i", 'len(_muc(v, t)) != 1', 'len(_muc(v, t)) < 1'),
    ("i_prime", 'MIEN_HIEU_LUC.get(k, (0, 0))[1] is None and', 'True and'),
):
    pair = []
    for mutate in (False, True):
        ns = {"__name__": "registry_model"}
        assert base.count(before) == 1
        exec(compile(base.replace(before, after) if mutate else base, "registry_model", "exec"), ns)
        
        law = copy.deepcopy(ns["LUAT_v1"])
        if label == "f":
            law["JOB_BAT_BUOC"].append(law["JOB_BAT_BUOC"][0])
        elif label in ("g", "i_prime"):
            law["JOB_BAT_BUOC"].remove("gate-ops (ubuntu-latest)")
        elif label == "h":
            law["JOB_BAT_BUOC"].append("khac (ubuntu-latest)")
        elif label == "i":
            law["MUC"].append(copy.deepcopy(law["MUC"][0]))
        key = ns["bam"](law)
        ns["LUAT_PHIEN_BAN"] = {key: law}
        ns["MIEN_HIEU_LUC"] = {key: (1, 9 if label in ("e_prime", "i_prime") else None)}
        if label == "i_prime":
            other = ns["LUAT_v1"]
            ns["LUAT_PHIEN_BAN"][ns["bam"](other)] = other
            ns["MIEN_HIEU_LUC"][ns["bam"](other)] = (10, None)
        pair.append({"registry": ns["kiem_so_luat"](), "kiem_has_registry_error": "so_luat_hong" in ns["kiem"](text, p, goc)[1]})
    out["registry_cases"][label] = pair
    assert pair[0]["kiem_has_registry_error"] != pair[1]["kiem_has_registry_error"]


out['A14_i_prime']={}
for sh in (None,'bash'):
    q=changed('python .claude/dev/packet_loop_test.py | python ops/tee_test.py',sh)
    out['A14_i_prime'][str(sh)]=mods['baseline'].kiem(text,q,goc)
(W/'audit_previous.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k in ('registry_cases','A14_i_prime')},ensure_ascii=False,indent=2))
