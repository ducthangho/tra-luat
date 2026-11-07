import collections, hashlib, json, pathlib, re, subprocess, sys
import yaml
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
sys.path.insert(0,str(W/'soan'))
import gram,sinh_r8 as s,dot_bien_r8

def git(*args):return subprocess.check_output(['git',*args],cwd=R)
ns={'__name__':'facts'}
src=git('show','508d678:ops/gate_output_doi_chieu.py').decode().replace('Path(__file__).with_name("ci_provenance.py")',repr(str(R/'ops/ci_provenance.py')))
exec(compile(src,'generation1','exec'),ns)
expected=set(ns['LUAT_v1']['JOB_BAT_BUOC']);names={t for m in ns['LUAT_v1']['MUC'] for b in m['buoc'] for t in b['ten']}
out={}
for base in ('b796259','d26b36f'):
 paths=git('ls-tree','-r','--name-only',base,'ops/land').decode().splitlines()
 count=match=all_prov=ckbad=wd=wdmatch=0;runids=[]
 for path in paths:
  if '-provenance/' not in path or not path.endswith('.yaml'):continue
  p=yaml.safe_load(git('show',f'{base}:{path}'))
  if not isinstance(p,dict) or p.get('schema')!='ci_provenance/1':continue
  all_prov+=1;m=p['moc'];run=m['run']
  cks={c['sha'] for c in m['checkout'] if c['trang_thai']=='passed'}
  ckbad+=any(c!=run['head_sha'] for c in cks)
  if m['workflow_definition'].get('trang_thai')=='passed':
   wd+=1
   blobs={git('rev-parse',f'{c}:{run["loi_khai_rest_path"]}').decode().strip() for c in cks}
   wdmatch+=bool(blobs) and blobs=={m['workflow_definition']['blob']}
  if run['loi_khai_rest_path']=='.github/workflows/ci.yml' and run['event']=='push':
   count+=1;runids.append(run['run_id'])
   j=[j['name'] for j in m['gate_output']['jobs'] if j['conclusion']!='skipped' and 'ubuntu-latest' in (j['labels'] or []) and j['name']!='chuan-bi']
   match+=len(j)==len(expected) and set(j)==expected
 out[base]={'provenance':all_prov,'ci_push':count,'job_set_match':match,'earliest_run':min(runids),'checkout_head_mismatch':ckbad,'workflow_passed':wd,'workflow_blob_match':wdmatch}
wf=yaml.safe_load(git('show','fe84620:.github/workflows/ci.yml'))
steps=[s0 for j in wf['jobs'].values() for s0 in j['steps'] if s0.get('name') in names]
accepted=[s0 for s0 in steps if gram.cp(s0.get('run'),s0.get('shell')) is None]
out['workflow']={'rule_steps':len(steps),'accepted':len(accepted),'accepted_with_args':sum(len(s0['run'].split())>2 for s0 in accepted),'shells':dict(collections.Counter(str(s0.get('shell')) for s0 in steps)),'actions':dict(collections.Counter(s0['uses'] for j in wf['jobs'].values() for s0 in j['steps'] if 'uses' in s0))}
land='8ab100793df9831505f495543a74044b91c2c9ab'
first=set(git('rev-list','--first-parent','origin/master').decode().splitlines())
out['adr_land']={}
for adr,filename in [(52,'0052-tran-loi-goi-codex-len-tam.md'),(53,'0053-tran-kich-thuoc-sensitive-len-sau-tep.md')]:
 path='docs/adr/'+filename
 rc=[subprocess.run(['git','cat-file','-e',rev+':'+path],cwd=R,capture_output=True).returncode for rev in (land,land+'^1')]
 out['adr_land'][str(adr)]={'exists_rcs':rc,'first_parent':land in first,'ref':git('rev-parse','origin/master').decode().strip()}
out['numstat']=git('diff','--numstat','d26b36f','508d678','--','ops/gate_output_doi_chieu.py','ops/gate_output_doi_chieu_test.py','.claude/dev/ci_dang_ky_test.py').decode().splitlines()
out['estimate']={'test_net':-40+120+55+45+65+40+22+200+20+8+20,'module_net':-15+25,'total_explicit_terms':1620-15+25-40+120+55+45+65+40+22+200+20+8+20,'mutants_listed':53+91+8+6+6,'current_total':1620+10+555+63}
hat=s.LENH+[f'{a} | {b}' for a in s.LENH for b in s.LENH]+[f'{s.LENH[0]} | {b} | {s.LENH[2]}' for b in s.LENH]
kho=set(s.kho());x,y,z='python ops/x.py','bash ops/z.sh','pwsh -NoProfile -File ops/v.ps1'
full={p for m in s.chen('python ops/m.py w') for p in [f'{m} | {y} | {z}',f'{x} | {m} | {z}',f'{x} | {y} | {m}']}
out['generator']={'KT':len(s.KT),'hat':len(hat),'all_position_pipeline_unique':len(full),'present':len(full&kho),'missing':len(full-kho)}
readme=(W/'soan/g1/README.md').read_text();lines=re.findall(r'^([0-9a-f]{64})  (\S+)$',readme,re.M)
out['g1_hashes']=[len(lines),sum(hashlib.sha256((W/'soan/g1'/p).read_bytes()).hexdigest()==h for h,p in lines)]
checks={}
for ca,mutation in [('A1','m-A1c'),('B1','m-B1b'),('C1','m-C1b'),('D1','m-D1b')]:
 prefix='| A1 dương ' if ca=='A1' else '| '+ca+' '
 line=next(l for l in (W.parent/'SPEC.md').read_text().splitlines() if l.startswith(prefix))
 checks[ca]={'GIOI_HAN':'GIOI_HAN' in line,'mutant':mutation in line}
assert all(all(r.values()) for r in checks.values())
out['limit_assertions']=checks
out['H04']={'reference':gram.cp(None,'pwsh'),'swapped':dot_bien_r8.DB['m-S19_dao_thu_tu_1_2'][0](None,'pwsh')}
(W/'audit_facts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
