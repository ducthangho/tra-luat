from pathlib import Path
import hashlib,json,subprocess
B=Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review9';p=R/'ops/reviews/pr468-hoso-4-packet-review-8-codex';p6=R/'ops/reviews/pr468-hoso-4-packet-review-6-codex';dst=O/'artifact-repair';dst.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest();rows=[]
for line in (p/'ARTIFACTS.sha256').read_text().splitlines():
 expected,rel=line.split(maxsplit=1);rel=rel.lstrip('*');f=p/rel;source=f
 if not f.is_file():
  assert rel.startswith(('rig/source/','rig/do-review/'))
  source=p6/rel.split('/',2)[2]
 row=dict(path=rel,exists=f.is_file(),tracked=bool(subprocess.check_output(['git','-C',str(R),'ls-files','--',str(f.relative_to(R))]).strip()),source=str(source.relative_to(R)),expected=expected,recoverable=source.is_file() and sha(source.read_bytes())==expected)
 if row['recoverable']:
  t=dst/rel;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(source.read_bytes())
 rows.append(row)
(dst/'ARTIFACTS.sha256').write_bytes((p/'ARTIFACTS.sha256').read_bytes())
def check(path,name):
 r=subprocess.run(['sha256sum','--check','ARTIFACTS.sha256'],cwd=path,capture_output=True);(O/(name+'.stdout')).write_bytes(r.stdout);(O/(name+'.stderr')).write_bytes(r.stderr);return r.returncode
report=dict(listed=len(rows),present=sum(x['exists'] for x in rows),missing=sum(not x['exists'] for x in rows),recoverable=sum(x['recoverable'] for x in rows),original_rc=check(p,'manifest8-original'),repaired_copy_rc=check(dst,'manifest8-repair'),files=rows,method='Fill declared missing paths in reviewer scratch with exact-hash bytes already archived in turn 6; no repository changes.')
(O/'artifact-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False,indent=2))
