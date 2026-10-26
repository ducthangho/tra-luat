from pathlib import Path
import ast,re,json,sys,os,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
ops={x['name']:x for x in json.loads((R/'operators6/results.json').read_text())};base={c:(rc,o) for c,rc,o in json.loads((R/'frontier6/baseline.json').read_text())}
jobs=[]
for line in (root/'.review-input/tu-dot-bien/kq8.txt').read_text().splitlines():
 m=re.fullmatch(r'(.*?) GIET\+NEM (.*)',line)
 if not m:continue
 killed,errors=ast.literal_eval(m[2]);assert m[1] in ops
 for c in errors:jobs.append((m[1],c,ops[m[1]]['source']))
def one(v):
 name,c,src=v;assert base[c][0]==0
 cmd=[sys.executable,'-B',str(root/'ops/ci_provenance_test.py'),'--mot-ca',c];q=subprocess.run(cmd,capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=src,PYTHONDONTWRITEBYTECODE='1'),timeout=300);o=(q.stdout+q.stderr).decode()
 return {'name':name,'case':c,'source':src,'command':cmd,'baseline':{'source':'frontier6/baseline.json','rc':base[c][0]},'rc':q.returncode,'output':o,'rank':'TIN_DUNG_GIA' if q.returncode==4 else 'GIET_DUNG_CA' if q.returncode==3 and o.startswith('DO:'+c+':') else 'KHAC','scope':'only error cases listed in supplied kq8.txt, max3 per operator'}
rows=[]
with concurrent.futures.ThreadPoolExecutor(3) as ex:
 for r in ex.map(one,jobs):
  rows.append(r);(R/'operator-errors6-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(r['name'],r['case'],r['rank'],flush=True)
print('OPERATORS',len(set(z['name'] for z in rows)),'CASES',len(rows),collections.Counter(z['rank'] for z in rows))
