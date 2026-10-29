import hashlib,struct,tempfile
from pathlib import Path
import probe_recheck as h
with tempfile.TemporaryDirectory(prefix='r3-graph-') as tmp:
 p=Path(tmp);k,sha,al=h.anc(p,which='B0')
 h.log(before=h.raw(p,al))
 k['g']('commit-graph','write','--reachable');f=p/'.git/objects/info/commit-graph';data=bytearray(f.read_bytes())
 chunks={bytes(data[8+i*12:12+i*12]):int.from_bytes(data[12+i*12:20+i*12],'big') for i in range(data[6]+1)}
 count=int.from_bytes(data[chunks[b'OIDF']+255*4:chunks[b'OIDF']+256*4],'big')
 ids=[data[chunks[b'OIDL']+i*20:chunks[b'OIDL']+(i+1)*20].hex() for i in range(count)]
 pos=chunks[b'CDAT']+ids.index(k['M'])*36+20
 h.log(commit=k['M'],old_parent=hex(int.from_bytes(data[pos:pos+4],'big')),chunks={x.decode('ascii'):y for x,y in chunks.items()},count=count)
 data[pos:pos+4]=(0x70000000).to_bytes(4,'big');data[-20:]=hashlib.sha1(data[:-20]).digest();f.chmod(0o644);f.write_bytes(data)
 h.log(verify=h.git(p,'commit-graph','verify'),normal_ancestor=h.git(p,'merge-base','--is-ancestor',sha,'master'),without_graph=h.git(p,'-c','core.commitGraph=false','merge-base','--is-ancestor',sha,'master'))
 for no in ((),(h.KEY,)):
  h.log(debt=bool(no),result=h.raw(p,al,no))
