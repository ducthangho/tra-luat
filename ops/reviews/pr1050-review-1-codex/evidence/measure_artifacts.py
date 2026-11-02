from pathlib import Path
import hashlib, json, subprocess, re
repo = Path('cay-kho')
head = 'c24875d00e93e6a98e0a0abd0837e0cbcad65d4d'
source = 'a34b9a38cda2669f9a90958c69bb6f2faa0f4353'
def git(*args): return subprocess.check_output(['git','-C',str(repo),*args])
def sha(b): return hashlib.sha256(b).hexdigest()
for n in (1,2):
    dest = repo/f'ops/reviews/wp1037-g1-codex-luot{n}'
    mappings = [('PROMPT.md',f'luot{n}-PROMPT.md'),('VERDICT.md',f'luot{n}-VERDICT-codex.md'),('run/run.json',f'luot{n}-run.json')]
    for local, original in mappings:
        b = (dest/local).read_bytes(); old = git('show',f'{source}:ops/handoff/wp1037-g1-claude/{original}')
        print(f'ROUND {n} {local}: bytes={len(b)} sha256={sha(b)} original_equal={b==old} HEAD_equal={b==git("show",head+":"+str((dest/local).relative_to(repo)))}')
    b = (repo/f'ops/reviews/wp1037-g1-codex-luot{n}-verdict.md').read_bytes()
    print(f'ROUND {n} flat_equals_VERDICT={b==(dest/"VERDICT.md").read_bytes()}')
    d=json.loads((dest/'run/run.json').read_bytes())
    for fn,key in [('PROMPT.md','prompt'),('run/stdout.log','stdout'),('run/stderr.log','stderr'),('run/checkpoint.json','checkpoint')]:
        b=(dest/fn).read_bytes(); print(f'ROUND {n} run-ref {fn}: sha256_match={sha(b)==d[key+"_sha256"]} bytes_match={len(b)==d.get(key+"_byte",len(b))}')
for folder in [repo/'ops/reviews/wp1037-g1-codex-luot1',repo/'ops/reviews/wp1037-g1-codex-luot2',repo/'ops/land/pr1041-wp1037-provenance']:
    listed=set()
    for line in (folder/'SHA256SUMS').read_text().splitlines():
        expected,fn=line.split(maxsplit=1);fn=fn.removeprefix('./');listed.add(fn)
        b=(folder/fn).read_bytes();print(f'SUM {folder.relative_to(repo)}/{fn}: {"OK" if sha(b)==expected else "FAIL"}')
    actual={str(f.relative_to(folder)) for f in folder.rglob('*') if f.is_file() and f.name!='SHA256SUMS'}
    print(f'INVENTORY {folder.relative_to(repo)}: listed={len(listed)} files={len(actual)} missing={sorted(listed-actual)} extra={sorted(actual-listed)}')
original=git('ls-tree','-r','--name-only',source,'ops/handoff/wp1037-g1-claude').decode().splitlines()
print('ORIGINAL_INVENTORY:',original)
lease=git('show',source+':ops/leases/wp1037-r1-g1-claude.yaml')
print('lease snapshot byte_equal=',lease==(repo/'ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt').read_bytes(),'sha256=',sha(lease))
spec=git('show',source+':ops/specs/wp1037.md')
print('spec_sha256=',sha(spec))
