#!/usr/bin/env python3
import ast
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from probe import ROOT, OUT, SOURCE, M

def git(*args):
    return subprocess.check_output(['git','-C',str(ROOT/'kho-guong.git'),*args])

def calls(source):
    return [n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Call)
            and isinstance(n.func,ast.Name) and n.func.id in ('bang','chot')]

data={}
data['changed_paths']=git('diff','--name-status','dc02c9b','3f1cda1').decode().splitlines()
data['numstat']=git('diff','--numstat','dc02c9b','3f1cda1').decode().splitlines()
data['tree']=git('rev-parse','3f1cda1^{tree}').decode().strip()
data['refs']=dict(Counter(r.split('/')[1] for r in git('for-each-ref','--format=%(refname)').decode().splitlines()))
data['master_commits']=int(git('rev-list','--count','refs/remotes/origin/master'))
data['shallow']=git('rev-parse','--is-shallow-repository').decode().strip()
data['tables']={name:len(getattr(M,name)) for name in
    ['CA','DOT_BIEN_512','CONTROL_512','CONTROL_BO_SUNG_512','DOT_BIEN_TU_KIEM_512','_VUNG_CAT_512',
     'CHOT_CO_DAU_VAO_PHAN_BIET_512','CHOT_BI_HAP_THU_512','NO_CHUA_CO_TU_KIEM_512']}
data['control_expected']=dict(Counter(x[4] for x in M.CONTROL_512))
data['selftest_expected']=dict(Counter(x[3] for x in M.DOT_BIEN_TU_KIEM_512))
data['selftest_channel']=dict(Counter(x[4] for x in M.DOT_BIEN_TU_KIEM_512))
data['removed_name_exists']=hasattr(M,'CHOT_CHUA_CO_CONTROL_512')
data['anchors26']=dict(Counter(SOURCE.count(x[2]) for x in M.DOT_BIEN_512+M.CONTROL_512))
data['anchors28']=dict(Counter(SOURCE.count(x[2]) for x in M.DOT_BIEN_512+M._muc_control_512()))
data['executables']=[n.lineno for n in ast.walk(ast.parse(SOURCE)) if isinstance(n,ast.Attribute)
     and isinstance(n.value,ast.Name) and n.value.id=='sys' and n.attr=='executable']
data['signal_counts']={}
data['added_lines']={}
data['historical_case_counts']={}
for sha in ['dc02c9b','540b6f1','a1c7d7f','d5e7e7d','3f1cda1','36f68c7']:
    source=git('show',sha+':ops/lease_publish_test.py').decode()
    tree=ast.parse(source)
    data['historical_case_counts'][sha]=len([n for n in tree.body if isinstance(n,ast.FunctionDef)
        and any(isinstance(d,ast.Name) and d.id=='ca' for d in n.decorator_list)])
    data['signal_counts'][sha]=len(calls(source))
    doclines=set()
    for node in ast.walk(tree):
        if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Module)):
            if node.body and isinstance(node.body[0],ast.Expr) and isinstance(node.body[0].value,ast.Constant) and isinstance(node.body[0].value.value,str):
                doclines.update(range(node.body[0].lineno,node.body[0].end_lineno+1))
    diff=git('diff','-U0','dc02c9b',sha,'--','ops/lease_publish_test.py').decode()
    line=0; types=Counter(); detail=[]
    for text in diff.splitlines():
        if text.startswith('@@'):
            line=int(re.search(r'\+(\d+)',text).group(1)); continue
        if text.startswith('+++') or text.startswith('---'): continue
        if text.startswith('+'):
            s=text[1:]
            kind='blank' if not s.strip() else 'comment' if s.lstrip().startswith('#') else 'docstring' if line in doclines else 'code_data'
            types[kind]+=1; detail.append([line,kind]); line+=1
        elif text.startswith(' '): line+=1
    data['added_lines'][sha]=dict(types)
    (OUT/f'added-lines-{sha}.json').write_text(json.dumps(detail))

base=ast.parse(git('show','dc02c9b:ops/lease_publish_test.py').decode())
head=ast.parse(SOURCE)
def cases(tree):
    return {n.name:n for n in tree.body if isinstance(n,ast.FunctionDef) and
            any(isinstance(d,ast.Name) and d.id=='ca' for d in n.decorator_list)}
old,new=cases(base),cases(head)
class Normalize(ast.NodeTransformer):
    def visit_Call(self,n):
        if isinstance(n.func,ast.Name) and n.func.id=='chot': n.func.id='bang'
        return self.generic_visit(n)
data['m1_per_case']={}
data['old_case_AST_changes']=[]
for name,node in old.items():
    before=ast.dump(node); after=ast.dump(new[name])
    if before!=after:
        count=lambda n:Counter(x.func.id for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('bang','chot'))
        data['m1_per_case'][name]={'before':dict(count(node)),'after':dict(count(new[name]))}
    if ast.dump(Normalize().visit(node))!=ast.dump(Normalize().visit(new[name])):
        data['old_case_AST_changes'].append(name)

hist=OUT/'history'; hist.mkdir(exist_ok=True)
ref='refs/remotes/origin/ops/handoff-530'
paths=git('ls-tree','-r','--name-only',ref,'ops/handoff/530').decode().splitlines()
for path in paths:
    content=git('show',ref+':'+path)
    dest=hist/Path(path).relative_to('ops/handoff/530'); dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(content)
v=(hist/'review-vong1/VERDICT.rv530-1.md').read_bytes()
r=json.loads((hist/'review-vong1/run.json').read_text())
data['v1']={'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest(),'duration_s':r['thoi_luong_giay'],
  'recomputed_duration_s':(datetime.fromisoformat(r['ket_thuc_utc'])-datetime.fromisoformat(r['bat_dau_utc'])).total_seconds(),
  'reported_stderr_bytes':r['stderr_byte'],'rc':r['ma_thoat']}
log=(OUT/'gate-wrapper.log').read_text()
rows=re.findall(r'(?m)^(?:(\[A\]|\[B\]) )?lease_publish: (\d+)/(\d+) đạt; đã chạy=(\d+), bỏ qua=(\d+)$',log)
data['A5']={'summary_rows':rows,'red_rows':len(re.findall(r'(?m)^(?:(?:\[A\]|\[B\]) )?  ĐỎ  ',log)),
 'case_exits':len(re.findall(r'(?m)^<<< ra ',log)),'rc_file':(OUT/'gate-wrapper.rc').read_text().strip()}
assert len(rows)==3 and all(a==b==c=='159' and skip=='0' for _,a,b,c,skip in rows)
assert data['A5']['red_rows']==0
(OUT/'counts.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
print(json.dumps(data,ensure_ascii=False,indent=2))
