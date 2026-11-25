from pathlib import Path
import os,subprocess,json,hashlib,re,datetime
R=Path.cwd();O=R/'out';S=R/'cay-kho';M=R/'kho.git';os.environ['GIT_OPTIONAL_LOCKS']='0'
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
before=json.loads((O/'source-before.json').read_text());after={}
for root in [S,M]:
 for p in sorted(root.rglob('*')):
  if p.is_symlink():after[str(p.relative_to(R))]=['link',os.readlink(p),p.lstat().st_mtime_ns]
  elif p.is_file():after[str(p.relative_to(R))]=[hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size,p.stat().st_mtime_ns]
delta=[p for p in before.keys()|after.keys() if before.get(p)!=after.get(p)]
print('SOURCE_ENTRIES',len(before),len(after),'DELTA',len(delta),delta[:10]);assert not delta
assert hashlib.sha256((S/'ops/specs/wp1466.md').read_bytes()).hexdigest()=='baf01d45ba30512e768466fd077842346644db730d69471a44efb2a40b6b9139'
print('HEAD',subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD'],text=True).strip())
print('STATUS',repr(subprocess.check_output(['git','-C',str(S),'status','--porcelain=v1','--untracked-files=all'],text=True)))
s=(O/'VERDICT.md').read_text()
for h in ['## ĐỐI CHIẾU LƯỢT TRƯỚC','### Theo từng finding','### Theo lớp','## BẢNG LỚP (i)','## BẢNG LỚP (ii)','## BẢNG SĂN','## BẢNG ĐO','**TỆP/DÒNG:**','**VẤN ĐỀ:**','**GỢI Ý VÁ:**','**ĐÃ THỬ NGHIỆM:**','**ĐỘ TIN:**']:assert h in s,h
assert re.findall(r'^### ([a-z0-9-]+) \[P[0-3]\]',s,re.M)==['tien-kiem-lease-chua-du']
assert not any(w in s for w in ['ĐANG CHẠY','CHỜ ĐO','Chưa chốt','sẽ cập nhật'])
for label,t in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',s):
 if not t.startswith('http') and t not in ['SHA256SUMS','seal.log']:assert (O/t).exists(),t
print('VERDICT_REQUIRED_SHAPE_OK True')
paths=[p for p in O.iterdir() if p.is_file() and p.name!='SHA256SUMS' and p.suffix in ('.py','.md','.log','.json','.diff') and p.name!='seal.log']
for folder in ['sc','mutation-details']:paths.extend(p for p in (O/folder).rglob('*') if p.is_file())
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(O)) for p in sorted(paths)]
(O/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print('SEALED_FILES',len(paths),'VERDICT_SHA256',hashlib.sha256((O/'VERDICT.md').read_bytes()).hexdigest())
