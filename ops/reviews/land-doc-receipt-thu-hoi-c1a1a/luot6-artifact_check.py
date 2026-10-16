import pathlib,hashlib,json,subprocess
root=pathlib.Path.cwd();d=root/'ops/reviews/land-doc-receipt-thu-hoi-c1a1a'
sha=lambda b:hashlib.sha256(b).hexdigest()
for n in (4,5):
 rows=[]; absent=[]
 for line in (d/f'luot{n}-ARTIFACTS.sha256').read_text().splitlines():
  digest,name=line.split(None,1);p=d/f'luot{n}-{name}'
  if name=='VERDICT.md':p=d/f'luot{n}-verdict-day-du.md'
  if not p.is_file():absent.append(name);continue
  got=sha(p.read_bytes());rows.append(dict(name=name,path=str(p.relative_to(root)),expected=digest,actual=got,match=got==digest))
 print(json.dumps(dict(round=n,available=len(rows),matched=sum(r['match'] for r in rows),rows=rows,not_archived_count=len(absent),not_archived=absent),ensure_ascii=False))
 if n==4:
  paths=[str(p.relative_to(root)) for p in d.glob('luot4-*')]
  checks=[]
  for path in paths:
   p=subprocess.run(['git','show','de927ca:'+path],capture_output=True)
   checks.append(dict(path=path,read_rc=p.returncode,unchanged=p.stdout==(root/path).read_bytes()))
  print(json.dumps(dict(previous_commit_checks=checks)))
paths=[str(p.relative_to(root)) for p in d.iterdir() if p.is_file()]+['.claude/dev/doc_receipt_thu_hoi_test.py','ops/reviews/other/example.patch','ops/reviews/land-doc-receipt-thu-hoi-c1a1a/a.py','ops/reviews/land-doc-receipt-thu-hoi-c1a1a/a.json']
p=subprocess.run(['git','check-attr','whitespace','text','eol','--',*paths],capture_output=True,text=True)
print(json.dumps(dict(command=['git','check-attr','whitespace','text','eol','--',*paths],rc=p.returncode,stdout=p.stdout)))
# Manifest/input copies where names overlap.
checks=[]
for p in pathlib.Path('/tmp/review650-r6-input').glob('*.py'):
 q=d/('luot5-'+p.name)
 if q.exists():checks.append(dict(script=p.name,match=p.read_bytes()==q.read_bytes()))
print(json.dumps(dict(input_copies=checks)))

p=d/'luot4-verdict-day-du.md';body=p.read_bytes().split(b'\n',1)[1]
print(json.dumps(dict(round4_wrapper='one leading HTML metadata line, present at de927ca',whole_sha256=sha(p.read_bytes()),body_sha256=sha(body),original_expected='fb7a1305cc42e1dad49bcffb8fe5dc05177651d70273c974ebc3aac4679ff566',body_match=sha(body)=='fb7a1305cc42e1dad49bcffb8fe5dc05177651d70273c974ebc3aac4679ff566')))
