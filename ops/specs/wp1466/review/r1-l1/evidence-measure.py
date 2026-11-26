import sys, pathlib, subprocess, re, json, collections, datetime, importlib.util
ROOT=pathlib.Path('cay-kho').resolve(); OUT=pathlib.Path('out').resolve(); BASE='origin/master'
def git(*args,check=True):
 p=subprocess.run(['git','-C',str(ROOT),*args],capture_output=True)
 if check and p.returncode: raise RuntimeError((args,p.returncode,p.stderr.decode()))
 return p
def blob(path,ref=BASE): return git('show',ref+':'+path).stdout
files=['ops/lease_publish.py','.claude/dev/packet_loop.py','.claude/dev/launcher.py','.claude/dev/gate_lifecycle.py','.github/workflows/ci.yml','.github/workflows/ops-publish-lease.yml']
src=[blob(p) for p in files]
print('TIME',datetime.datetime.now(datetime.timezone.utc).isoformat())
for p,s in zip(files,src): print('LINES',p,len(s.splitlines()),'LF',s.count(b'\n'))
print('REFS',len(git('for-each-ref','--format=%(refname)','refs/remotes/origin').stdout.splitlines()))
print('SHALLOW',git('rev-parse','--is-shallow-repository').stdout.decode().strip(),'ABBREV',git('config','core.abbrev').stdout.decode().strip())
for no,oid,name in [('55','d2e3052d479d140b7e7b91df41ec4914fab7d544','0055-tran-loi-goi-codex-len-muoi.md'),('53','8ab100793df9831505f495543a74044b91c2c9ab','0053-tran-kich-thuoc-sensitive-len-sau-tep.md')]:
 path='docs/adr/'+name
 print('OID',no,git('cat-file','-e',oid+':'+path,check=False).returncode,git('cat-file','-e',oid+'^1:'+path,check=False).returncode,int(oid.encode() not in git('rev-list','--first-parent',BASE).stdout.splitlines()))
patterns=[r'ai-dang-giu|ai_dang_giu|RC_DANG_GIU',r'\bLIVE\b','refs/pull/',r'eol|EOL|gitattributes','RC_PROVIDER',r'reviewed_sha|reviewing_head_sha',r'spec_hash|spec_sha256','changed_paths',r'(diff|changed).*write_set|write_set.*(diff|changed)','tested_sha',r'model_family|ho_model','bang_lop','class_slug',r'effective_review_class|_kiem_lop_review|RC_LOP',r'chup-workspace|chup_workspace|ghi_workspace',r'MOC_10_2_2|moc_10_2_2',r'codex_review_calls|RC_TRAN',r'ADR-0067|uy_quyen_quyet_dinh',r'Drive MCP|Sheets MCP',r'NGUOI_CO_THAM_QUYEN|RC_TU_CAP','doctrine','mien_p3','doi_chieu_luot','KET_LUAN','review_verdict','numstat','tran_loi_goi_codex','tran_kich_thuoc_sensitive',r'ghi hộ|ghi_ho']
for pat in patterns:
 counts=[subprocess.run(['grep','-cE',pat],input=s,capture_output=True).stdout.decode().strip() for s in src]
 print('SCAN',pat, '·'.join(counts))
tracked=git('ls-tree','-r','--name-only',BASE).stdout.decode().splitlines()
adr=[p for p in tracked if p.startswith('docs/adr/') and p.endswith('.md')]
print('ADR',len(adr),'MAX',max(adr))
receipts=[p for p in tracked if p.startswith('ops/reviews/') and p.endswith('.receipt.yaml')]
print('RECEIPTS',len(receipts),'bang_lop_text',sum(b'bang_lop' in blob(p) for p in receipts))
print('BIEN_NHAN_bang_lop',sum('bang_lop' in l for l in blob('ops/bien_nhan_v2.py').decode().splitlines()))
import yaml
print('RECEIPTS_bang_lop_KEY',sum('bang_lop' in yaml.safe_load(blob(p)) for p in receipts))
try:
 import jsonschema
 schema=json.loads(blob('.github/coordination/schemas/review_verdict.v1.schema.json'))
 validator=jsonschema.Draft202012Validator(schema)
 jpaths=[p for p in tracked if p.endswith('.json')]; ok=0; valid=[]; bad=[]
 for p in jpaths:
  try: ob=json.loads(blob(p))
  except Exception: bad.append(p); continue
  ok+=1
  if validator.is_valid(ob): valid.append(p)
 print('JSON',len(jpaths),'PARSE',ok,'VALID_V1',valid,'INVALID_JSON',bad,'REQUIRED',len(schema['required']))
except ImportError as e: print('JSON_NOT_MEASURED',str(e))
for pr in [836,1116,1127,1317]:
 matches=git('log','--first-parent',BASE,'--format=%H %s','--grep=Merge pull request #'+str(pr)+' ').stdout.decode().splitlines()
 for match in matches:
  oid=match.split()[0]; rows=[x.split('\t') for x in git('diff','--numstat',oid+'^1',oid).stdout.decode().splitlines()]
  print('PR',pr,oid,'FILES',len(rows),'ADD',sum(int(x[0]) for x in rows),'DEL',sum(int(x[1]) for x in rows))
proto=blob('docs/PROTOCOL_DA_PHIEN.md').decode()
rows=re.findall(r'^\| `ADR-\d{4}`.*$',proto,re.M); a=rows[:50]; b=rows[50:]
print('SECTION20',len(rows),'A',len(a),'B',len(b))
print('A_LABELS',collections.Counter('co nhac' if 'có nhắc:' in l.split('|')[-2] else 'chua do' if l.split('|')[-2].strip()=='chưa đo' else 'khong cong' if l.split('|')[-2].strip().startswith('không cổng') else '0 cong' if l.split('|')[-2].strip().replace('*','').startswith('0 cổng') else 'cu the' for l in a))
print('WORKFLOWS',[(pat,sum(sum(pat in l for l in blob(p).decode().splitlines()) for p in tracked if p.startswith('.github/workflows/') and p.endswith('.yml'))) for pat in ['kiem-merge','adr-song']])
print('1172',sum('1172' in l for l in src[1].decode().splitlines()))
# Load registry without invoking tests; -B prevents checkout bytecode writes.
sys.path.insert(0,str(ROOT/'.claude/dev'))
import packet_loop_test as pt
print('REGISTRY',len(pt.CASES),len(pt.MUTANTS),'ADR_CASES',sum(n.startswith('adr_song_') for n,f in pt.CASES),'DOCTRINE_CASES',sum(n.startswith('doctrine_scan_') for n,f in pt.CASES),'ADR_MUTANTS',sum(n.startswith('adr_') for n in pt.MUTANTS))
(OUT/'registry-names.json').write_text(json.dumps({'cases':[n for n,f in pt.CASES],'mutants':list(pt.MUTANTS)},ensure_ascii=False,indent=2))
spec= (ROOT/'ops/specs/wp1466.md').read_text(); blocks=dict(re.findall(r'^~~~ ([^\n]+)\n(.*?)^~~~$',spec,re.M|re.S))
print('ADR_BLOCK_LINES',len(blocks['adr'].splitlines()))
for k in ['p1-moi','p2-moi','p3-moi','p4-moi','p5-moi','p6-moi']: print('BLOCK_LINES',k,len(blocks[k].splitlines()))
checks=spec[spec.index('| chốt | luật |'):spec.index('Đếm theo bảng, đơn vị')]
checks=checks.replace('`r1466_xoa_neo_1` … `r1466_xoa_neo_8`',' '.join('`r1466_xoa_neo_%d`'%i for i in range(1,9))).replace('`inv_bo_neo_1` … `inv_bo_neo_8`',' '.join('`inv_bo_neo_%d`'%i for i in range(1,9)))
ca=set(re.findall(r'`(r1466_\w+)`',checks)); mu=set(re.findall(r'`((?:inv_|t1466_)\w+)`',checks))
print('NEW_CASES',len(ca),'NEW_MUTANTS',len(mu)); print('NEW_CASE_NAMES',' '.join(sorted(ca)))
print('NEW_MUTANT_NAMES',' '.join(sorted(mu)))
refs=re.findall(r'ca: `([^`]+)::([^`]+)`',blocks['p2-moi'])
print('INV_CASE_REFS',len(refs),'GATE_ROWS',sum(l.startswith('| `INV') and 'cổng:' in l for l in blocks['p2-moi'].splitlines()))
for path,name in refs:
 content=blob(path).decode()
 present=bool(re.search(r'^\s*def (?:case_)?'+re.escape(name)+r'\(',content,re.M) or '("'+name+'",' in content)
 print('CASE_REF',path,name,present)
