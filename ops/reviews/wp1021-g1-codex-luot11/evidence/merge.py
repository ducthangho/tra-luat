from pathlib import Path
import hashlib
import subprocess
from record import ROOT, REPO, ENV, record

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], env=ENV)

head = git('rev-parse', 'HEAD').decode().strip()
p1, p2 = git('show', '-s', '--format=%P', head).decode().split()
out = []
def say(s):
    out.append(str(s))

say('HEAD=' + head)
say('tree=' + git('rev-parse', 'HEAD^{tree}').decode().strip())
say('parents=' + p1 + ' ' + p2)
say('shallow=' + git('rev-parse', '--is-shallow-repository').decode().strip())
say('symbolic-ref rc=' + str(subprocess.run(['git','-C',str(REPO),'symbolic-ref','-q','HEAD'],env=ENV,capture_output=True).returncode))
say('core.abbrev=' + git('config', '--get', 'core.abbrev').decode().strip())
spec_hash = hashlib.sha256((ROOT/'SPEC.md').read_bytes()).hexdigest()
say('SPEC.md sha256=' + spec_hash)
assert spec_hash == 'd5dd5a5df5a2dd8ce799a30442ed974fa3a0d669728446fafdbc2267a59b5b1d'
assert head == 'a16932aa09ce860a614f0bab4b2015699e7221bc'
assert p1 == '356a27e1378b2162bbc0be2ec06ff08fdacbdead'
assert p2 == '3dfb9731ceda05afbcec4e803a919c4df5e2e5a2'
write_set = ['ops/bien_nhan_v2.py','ops/bien_nhan_v2_test.py']
for rel in write_set:
    blobs = [git('rev-parse', s + ':' + rel).decode().strip() for s in (head,p1,p2)]
    say(rel + ': HEAD=' + blobs[0] + ' P1=' + blobs[1] + ' P2=' + blobs[2])
    assert blobs[0] == blobs[1]
    assert git('show', head + ':' + rel) == (REPO/rel).read_bytes()
changed = git('diff','--name-only',p2,head).decode().splitlines()
say('P2..HEAD paths=' + repr(changed))
assert changed == write_set
say('P2..HEAD numstat:\n' + git('diff','--numstat',p2,head).decode().strip())
def tree(rev):
    rows = git('ls-tree', '-rz', rev).split(b'\0')
    return {r.split(b'\t',1)[1]: r.split(b'\t',1)[0] for r in rows if r}
t, t1, t2 = map(tree, (head,p1,p2))
novel = [p.decode() for p in sorted(t.keys() | t1.keys() | t2.keys())
         if t.get(p) != t1.get(p) and t.get(p) != t2.get(p)]
say('union_tree_entries=' + str(len(t.keys() | t1.keys() | t2.keys())))
say('entries_different_from_both_parents=' + repr(novel))
assert not novel
patch = git('diff',p2,head)
say('actual diff sha256=' + hashlib.sha256(patch).hexdigest())
say('diff.patch sha256=' + hashlib.sha256((ROOT/'diff.patch').read_bytes()).hexdigest())
say('diff.patch byte_identical=' + str(patch == (ROOT/'diff.patch').read_bytes()))
assert patch == (ROOT/'diff.patch').read_bytes()
record('h01','Neo SHA, đặc tả và tính toàn vẹn merge',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/merge.py', '\n'.join(out))
