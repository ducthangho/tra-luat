from pathlib import Path
import subprocess,re,hashlib,difflib,json,datetime
R=Path.cwd();S=R/'cay-kho';O=R/'out';p=S/'ops/specs/wp1466.md';b=p.read_bytes();s=b.decode();old=subprocess.check_output(['git','-C',str(S),'show','3c89d87:ops/specs/wp1466.md']).decode()
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat())
blocks=dict(re.findall(r'^~~~ (\S+)\n(.*?)\n~~~$',s,re.S|re.M));ob=dict(re.findall(r'^~~~ (\S+)\n(.*?)\n~~~$',old,re.S|re.M))
print('BLOCKS_RETAINED_EQUAL',sum(v==ob.get(k) for k,v in blocks.items()),'OF',len(blocks),'REMOVED',sorted(set(ob)-set(blocks)))
for number in range(20):
 def section(txt):
  m=re.search(r'^## '+str(number)+r'\. .*?(?=^## \d+\. |\Z)',txt,re.S|re.M);return m.group() if m else ''
 print('SECTION',number,'BYTE_EQUAL',section(s)==section(old))
for pattern in [r'^~~~ tien-kiem',r'^\| V[0-9]+ \|',r'TIỀN KIỂM: (ĐẠT|DỪNG)',r'#1484']:
 hits=[n for n,l in enumerate(s.splitlines(),1) if re.search(pattern,l)];print('PATTERN',pattern,'MATCH_LINES',len(hits),'LINES',hits)
print('PATTERN_1484_OCCURRENCES',s.count('#1484'))
# Reproduce the exact submitted grep, compare stdout byte-for-byte.
a=S/'ops/specs/wp1466/rut-tien-kiem-r8/grep_r8.log';lines=a.read_bytes().splitlines(keepends=True);rx='.{0,70}(tien-kiem|tiền kiểm|I-NGUON|fail-closed|\\bđóng\\b|\\bĐÓNG\\b|\\b3f\\b|--sau-dang|đầu vào của khối|danh sách cho phép).{0,70}'
g=subprocess.run(['grep','-n','-o','-i','-E',rx,str(p)],capture_output=True)
expected=b''.join(lines[2:next(i for i,l in enumerate(lines) if l.startswith(b'$ grep -c'))]);print('AUTHOR_GREP_EXACT_RC',g.returncode,'BYTES_EQUAL',g.stdout==expected,'MATCHES',len(g.stdout.splitlines()));(O/'grep-r8-reproduced.log').write_bytes(g.stdout)
c=subprocess.run(['grep','-c','-E',r'^~~~ tien-kiem|^\| V[0-9]+ \||TIỀN KIỂM: (ĐẠT|DỪNG)',str(p)],capture_output=True);print('AUTHOR_COUNT_GREP_RC',c.returncode,'OUTPUT',c.stdout.decode().strip())
for folder in ['rut-tien-kiem-r8','nguyen-mau-r5']:
 root=S/'ops/specs/wp1466'/folder;checks=[]
 for line in (root/'SHA256SUMS').read_text().splitlines():
  digest,name=line.split(maxsplit=1);f=root/name.removeprefix('*');checks.append((name,f.exists() and hashlib.sha256(f.read_bytes()).hexdigest()==digest))
 print('ARTIFACT_HASHES',folder,'TOTAL',len(checks),'MATCH',sum(x[1] for x in checks),'FAILED',[x for x in checks if not x[1]])
debt=blocks['adr'].split('## Nợ',1)[1].split('## Giới hạn',1)[0];names=set(re.findall(r'^- `([^`]+)`',debt,re.M));ref=set(re.findall(r'(?:còn nợ|nợ): `([^`]+)`',blocks['p2-moi']))
print('DEBT_NAMES_IN_SECTION',len(names),'REFERENCED',len(ref),'MISSING',sorted(ref-names))
print('OLD_VERDICT_HASH',hashlib.sha256((S/'ops/specs/wp1466/review/r7-l7/VERDICT.md').read_bytes()).hexdigest())
for x in ['INV-BANG-DOI-CHIEU-NGU-NGHIA','INV-12-CONG-VERDICT-THEO-LOP','INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE']:
 print('DEBT',x,'ADR_NAMED',x in names,'INV_REFERENCED',x in ref)
print('ADR_DIRECT_1484_LINK', '#1484' in blocks['adr'])
# All current acceptance rows; none mentions preflight. Entire prose read separately.
accept=s.split('## 9.',1)[1].split('## 10.',1)[0]
print('ACCEPTANCE_ROWS',len(re.findall(r'^\| N\d+ \|',accept,re.M)))
print('PREFLIGHT_ACCEPTANCE_ROWS',[l.split('|')[1].strip() for l in accept.splitlines() if re.match(r'^\| N\d+ \|',l) and re.search('tiền kiểm|tien-kiem|1484|I-NGUON',l,re.I)])
print('NO_SUCCESSOR_NEW_CODE',subprocess.check_output(['git','-C',str(S),'diff','--name-only','3c89d87','e215940','--',*['.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py','ops/lease_publish.py','docs/PROTOCOL_DA_PHIEN.md']]).decode().strip()=='')
