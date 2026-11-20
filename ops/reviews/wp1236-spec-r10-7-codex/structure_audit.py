import ast,collections,difflib,hashlib,importlib.util,json,os,subprocess,sys
from pathlib import Path
from generate_review import W,R,M,Q,K,G,ENV,run
sp=importlib.util.spec_from_file_location('scanner_read',Q);q=importlib.util.module_from_spec(sp);sp.loader.exec_module(q)
g=G.read_text();formatted=W/'formatted_source.py';formatted.write_text('# Only formatting and comments differ.\n\n'+ast.unparse(ast.parse(g))+'\n')
n,r,out=run('formatted_regression',['hoi-quy',K,'-',formatted,'--ra',W/'formatted_h.jsonl'])
a=[json.loads(x) for x in (W/'h.jsonl').read_text().splitlines()];b=[json.loads(x) for x in (W/'formatted_h.jsonl').read_text().splitlines()]
manifest=[json.loads(x) for x in (W/'m1.jsonl').read_text().splitlines()];base=ast.parse(g)
# Archive all changes as review data, summarize scope per operator.
ops={}
for m in manifest:
 delta=list(difflib.unified_diff(ast.unparse(base).splitlines(),m['src'].splitlines(),n=1))
 ops.setdefault(m['op'],[]).append({'id':m['id'],'delta':delta})
(W/'operator_deltas.json').write_text(json.dumps(ops,ensure_ascii=False,indent=2))
Krows=[json.loads(x) for x in K.read_text().splitlines()]
num=subprocess.run(['git','-C',str(M),'diff','--numstat','0f9aa2a2cc697129e1f5be72feddf60986286865','HEAD','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py'],capture_output=True)
report={'format_regression':{'command_receipt':r,'stdout':out,'all_127_equal':a==b},'anchor_lines':{'mean':sum(len(x['cu'].splitlines()) for x in Krows)/len(Krows),'max':max(len(x['cu'].splitlines()) for x in Krows)},'numstat':{'rc':num.returncode,'stdout':num.stdout.decode()},'original_sha256':hashlib.sha256(G.read_bytes()).hexdigest(),'normalized_sha256':hashlib.sha256(ast.unparse(base).encode()).hexdigest()}
# New-head ordinary semantics-preserving refactoring: a private helper local gets a fresh name.
t=ast.parse(g)
f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_chuan')
renames=collections.Counter()
for n in ast.walk(f):
 if isinstance(n,ast.Name) and n.id=='c':n.id='ky_tu';renames['Name']+=1
# This is a valid rederivation portability probe, not a new mutant/attack.
rename=W/'renamed_local.py';rename.write_text(ast.unparse(t)+'\n')
n,r,out=run('renamed_regression',['hoi-quy',K,'-',rename,'--ra',W/'renamed_h.jsonl'])
rr=[json.loads(x) for x in (W/'renamed_h.jsonl').read_text().splitlines()]
report['rename_regression']={'renames':dict(renames),'receipt':r,'stdout':out,'not_applicable':[x for x in rr if 'src' not in x]}
(W/'structure_audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
