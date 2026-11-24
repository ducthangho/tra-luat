"""Replay supplied r6 mutants against copies/fragments of real fixtures."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import collections
import yaml

sys.dont_write_bytecode = True
W=Path(__file__).resolve().parent
R=W.parent/'repo'
OLD=W.parents[1]/'a-6-codex/repo'
E=W/'evidence'
T=W/'tmp/method'
T.mkdir(exist_ok=True)

def load(name, path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

G=load('control_r9',OLD/'ops/gate_output_doi_chieu.py')
rows={}
versions=collections.defaultdict(list)
for n in ['independent_mutants.jsonl','independent_corrected.jsonl','extra_mutants.jsonl','order_url_mutants.jsonl','reason_complete_mutants.jsonl']:
    for row in map(json.loads,(E/n).read_text().splitlines()):
        versions[row['id']].append((n,hashlib.sha256(row['src'].encode()).hexdigest()))
        rows[row['id']]=row

source=R/'ops/land/pr1453-wp433-land-evidence.yaml'
doc=yaml.safe_load(source.read_text())
part=copy.deepcopy(doc['post_merge_checks'][1])
dg=R/'ops/land/pr1453-wp433-provenance/hau-due-66eae51/danh-gia-gate-output-44717155521.txt'
pv=R/'ops/land/pr1453-wp433-provenance/hau-due-66eae51/ci/provenance.yaml'
good=part['moc_gate_output'].replace('hau-due-66eae51/','')
(T/dg.name).write_bytes(dg.read_bytes())
(T/'provenance.yaml').write_bytes(pv.read_bytes())
part['moc_gate_output']=good
result={'scope':'Đối chứng trên r9 c2d606b, không phải kết quả r10',
        'fixture_source':str(source),'good':G.kiem_ho_so(part,T),'replays':[]}
for ident in ['ref_any_run','ref_txt_wild','key_alpha_only','phi_substring','phi_skip_descendants']:
    mp=T/(ident+'.py')
    mp.write_text(rows[ident]['src'])
    M=load(ident,mp)
    altered=copy.deepcopy(part)
    if ident in ['ref_any_run','ref_txt_wild']:
        new_name=dg.name.replace('44717155521','x') if ident=='ref_any_run' else dg.name.replace('.txt','Xtxt')
        (T/new_name).write_bytes(dg.read_bytes())
        altered['moc_gate_output']=good.replace(dg.name,new_name)
    else:
        # First real claim is intentionally inconsistent in the historical fixture.
        bad=copy.deepcopy(doc['post_merge_checks'][0]['moc_gate_output'])
        altered.pop('moc_gate_output')
        if ident=='key_alpha_only': altered['gate_output_nguon1']=bad
        elif ident=='phi_substring': altered['gate_output_nguon_extra']=bad
        else: altered['gate_output_nguon']={'moc_gate_output':bad}
    baseline=G.kiem_ho_so(altered,T)
    mutant=M.kiem_ho_so(altered,T)
    result['replays'].append({'id':ident,'original':baseline,'mutant':mutant,
                              'different':baseline!=mutant,'mutant_src_sha256':hashlib.sha256(rows[ident]['src'].encode()).hexdigest()})

result['regression_inventory']={'entries':sum(map(len,versions.values())), 'unique_ids':len(rows),
    'duplicate_ids':{k:v for k,v in versions.items() if len(v)>1},
    'conflicting_source_ids':[k for k,v in versions.items() if len({h for _,h in v})>1]}
errors=[]
for ident,row in rows.items():
    for n in ast.walk(ast.parse(row['src'])):
        if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id=='re' and n.func.attr=='compile' and n.args and isinstance(n.args[0],ast.Constant):
            try: re.compile(n.args[0].value)
            except re.error as e: errors.append({'id':ident,'error':str(e)})
result['regression_inventory']['invalid_regex']=errors
tree=ast.parse((OLD/'ops/gate_output_doi_chieu.py').read_text())
for f in tree.body:
    if isinstance(f,ast.FunctionDef) and f.name=='kiem_ho_so':
        result['consumer_args']=[x.arg for x in f.args.args]
        result['waiver_calls']=[ast.unparse(n) for n in ast.walk(f) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='kiem_mien']
result['literal_examples']={}
for f in tree.body:
    if isinstance(f,ast.Assign) and isinstance(f.targets[0],ast.Name) and f.targets[0].id in ['TOKEN','PHI_LOI_KHAI','BO_SINH']:
        result['literal_examples'][f.targets[0].id]=ast.unparse(f.value)
(W/'audit_method_r5.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
assert result['good']==[]
assert all(x['different'] and x['mutant']==[] for x in result['replays'])
assert result['regression_inventory']['unique_ids']==127
assert not errors
print('METHOD_R5_COMPLETE: 5/5 consumer contrasts; 127 unique regression mutants; original-source hashes verified separately')
print(json.dumps({k:result[k] for k in ['replays','consumer_args','waiver_calls']},ensure_ascii=False,indent=2))
