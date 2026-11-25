import pathlib, subprocess, json, hashlib, re, os, sys, datetime
ROOT=pathlib.Path.cwd(); OUT=ROOT/'out'; SRC=ROOT/'cay-kho'; MIR=ROOT/'kho.git'
def run(args,cwd=SRC):
 p=subprocess.run(args,cwd=cwd,capture_output=True); return p

def snapshot():
 d={}
 for folder in [SRC,MIR]:
  for p in sorted(folder.rglob('*')):
   s=p.lstat(); k=str(p.relative_to(ROOT))
   if p.is_symlink(): d[k]=['link',os.readlink(p),s.st_mtime_ns]
   elif p.is_file(): d[k]=['file',s.st_size,s.st_mtime_ns,hashlib.sha256(p.read_bytes()).hexdigest()]
 return d
if sys.argv[1:] == ['finish']:
 a=json.loads((OUT/'snapshot-before.json').read_text()); b=snapshot()
 delta=[k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)]
 (OUT/'snapshot-after.json').write_text(json.dumps(b,ensure_ascii=False))
 print('SNAPSHOT',len(a),len(b),'DELTA',len(delta),delta[:20]); sys.exit(bool(delta))
(OUT/'snapshot-before.json').write_text(json.dumps(snapshot(),ensure_ascii=False))
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
for args in [('rev-parse','HEAD','HEAD^{tree}','origin/master'),('status','--porcelain=v1','--untracked-files=all'),('rev-parse','--is-shallow-repository'),('config','core.abbrev')]:
 p=run(['git',*args]);print('git',*args,'rc',p.returncode,p.stdout.decode().strip())
a=run(['git','show','3c89d87:ops/specs/wp1466.md']).stdout;b=(SRC/'ops/specs/wp1466.md').read_bytes()
print('SPEC_BLOB_MATCH',b==run(['git','show','e215940:ops/specs/wp1466.md']).stdout)
for label,s in [('r7',a),('r8',b)]:print('SIZE',label,'lines',s.count(b'\n'),'bytes',len(s))
blocks=lambda x: dict(re.findall(rb'^~~~ ([^\n]+)\n(.*?)^~~~\s*$',x,re.M|re.S))
ba,bb=blocks(a),blocks(b)
for name in sorted(ba.keys()|bb.keys()): print('BLOCK',name.decode(),'equal',ba.get(name)==bb.get(name),'sha',hashlib.sha256(bb[name]).hexdigest() if name in bb else 'REMOVED')
patch='ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch'; pp=(SRC/patch).read_bytes()
print('PATCH_EQUAL_R7',pp==run(['git','show','3c89d87:'+patch]).stdout,'sha',hashlib.sha256(pp).hexdigest())
print('PATCH_NUMSTAT',run(['git','apply','--numstat',str(SRC/patch)]).stdout.decode().strip())
for n in ['0053','0055']:
 line=next(x for x in b.decode().splitlines() if x.startswith('tran_') and 'ADR-'+n+'@' in x);oid=line.split('@')[1];path=next((SRC/'docs/adr').glob(n+'-*')).relative_to(SRC).as_posix()
 p1=run(['git','cat-file','-e',oid+':'+path]);p2=run(['git','cat-file','-e',oid+'^1:'+path]);p3=oid in run(['git','rev-list','--first-parent','origin/master']).stdout.decode().splitlines()
 print('OPTIN',n,'count',sum(x==line for x in b.decode().splitlines()),'oid',oid,'exists_rc',p1.returncode,'parent_rc',p2.returncode,'first_parent',p3)
print('ADR0052_OPTIN',len(re.findall(rb'^tran_loi_goi_codex: ADR-0052@',b,re.M)))
# semantic debt references independent extraction
adr=bb[b'adr'].decode(); tab=bb[b'p2-moi'].decode()
no=set(re.findall(r'^- `([^`]+)`:',adr,re.M)); refs=set(re.findall(r'(?:còn nợ|nợ): `([^`]+)`',tab))
print('DEBT_NAMES',len(no),'REFERENCES',len(refs),'MISSING',sorted(refs-no))
print('ADR_1484_LINK', '#1484' in adr,'SPEC_1484_COUNT',b.count(b'#1484'))
print('PRECHECK_BLOCK_PRESENT',b'tien-kiem' in bb)
print('REGEX_HISTORY_COUNT',len(re.findall(rb'^.*(?:^~~~ tien-kiem|^\| V[0-9]+ \||TI\xe1\xbb\x80N KI\xe1\xbb\x82M: (?:\xc4\x90\xe1\xba\xa0T|D\xe1\xbb\xaaNG)).*$',b,re.M)))
# Separate clone: no writes to source; remote is local mirror snapshot, never GitHub.
copy=OUT/'snapshot-clone'
p=run(['git','clone','--no-hardlinks','--no-checkout',str(MIR),str(copy)],ROOT);print('CLONE_RC',p.returncode);assert p.returncode==0,p.stderr
p=run(['git','config','core.abbrev','7'],copy);assert not p.returncode
p=run(['git','checkout','--detach','origin/master'],copy);print('DETACH_RC',p.returncode);assert not p.returncode,p.stderr
print('COPY',copy)
