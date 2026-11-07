import collections, hashlib, importlib.util, json, pathlib, re, subprocess, sys
import yaml
BASE=pathlib.Path(__file__).resolve().parent.parent
REPO=BASE/'repo'; WORK=BASE/'work'
sys.dont_write_bytecode=True

def git(*a): return subprocess.check_output(['git','-C',str(REPO),*a])
p=WORK/'candidate/ops/gate_output_doi_chieu.py'
s=importlib.util.spec_from_file_location('m508',p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)
record=[]
for x in git('ls-tree','-r','--name-only','b796259','--','ops/land').decode().splitlines():
    name=pathlib.Path(x).name
    if not (name == 'provenance.yaml' or re.fullmatch(r'ci-provenance-.*\.yaml',name)): continue
    d=yaml.safe_load(git('show',f'b796259:{x}'))
    if not isinstance(d,dict) or d.get('schema')!='ci_provenance/1':continue
    run=d.get('moc',{}).get('run',{})
    if run.get('event')=='push' and run.get('loi_khai_rest_path')=='.github/workflows/ci.yml':record.append((run['run_id'],x))
markers=[]
for law in m.LUAT_v1['MUC']:
    for step in law['buoc']:
        for kind, pattern in step['dau_hieu']:
            if kind=='DONG':
                groups=re.compile(pattern).groups
                if groups:markers.append((step['ten'][0],groups))
L='8ab100793df9831505f495543a74044b91c2c9ab'
adrs={}
for name in ('0052-tran-loi-goi-codex-len-tam.md','0053-tran-kich-thuoc-sensitive-len-sau-tep.md'):
    def exists(rev):return subprocess.run(['git','-C',str(REPO),'cat-file','-e',f'{rev}:docs/adr/{name}'],capture_output=True).returncode
    adrs[name]={'exists_at_land_rc':exists(L),'exists_at_parent_rc':exists(L+'^1'),'first_parent':L in git('rev-list','--first-parent','origin/master').decode().splitlines()}
result={'r7_push_provenance':len(record),'earliest':min(record) if record else None,'luat_sha256':m.bam(m.LUAT_v1),'count_patterns':len(markers),'capture_groups':sum(g for _,g in markers),'ADR_effectiveness_offline':adrs,'SPEC_matches_repo':(BASE/'SPEC.md').read_bytes()==(REPO/'ops/specs/wp1236-r8.md').read_bytes()}
(WORK/'metadata_r8.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
