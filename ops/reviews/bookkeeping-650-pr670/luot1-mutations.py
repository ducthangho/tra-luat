import difflib, hashlib, json, pathlib, shutil
from run_checks import run, ROOT, OUT
source=ROOT/'ops/land/pr666-wp650-provenance/doi_chieu_buoc.py'
raw=pathlib.Path('/tmp/do650'); src=source.read_text()
master=raw/'log-108815233339.txt'
before=master.read_bytes(); after=(raw/'log-108815233339.txt.mut').read_bytes()
assert before.replace(b'\x1b[36;1mpython .github/checks/ci_phamvi.py --kiem-bam\x1b[0m',b'\x1b[36;1mpython .github/checks/ci_phamvi.py --kiem-bamX\x1b[0m')==after
assert before.count(b'\x1b[36;1mpython .github/checks/ci_phamvi.py --kiem-bam\x1b[0m')==1
print('EXECUTOR_MUTATION_EXACT','kiem-bam -> kiem-bamX, one ANSI run-body line')
p=run('executor-mutant',['python3','-B',str(raw/'buoc_mut.py')]); d=json.loads(p.stdout)
assert p.returncode==0 and d['108815233339']['matched']==21 and d['108815233339']['runs_in_log']==27 and d['108815233339']['all_in_order'] is False
print('EXECUTOR_EXPECTED_REJECTION',json.dumps(d['108815233339']))
# Reviewer mutation changes one executed command in a different, required job.
target='108815233290'; own=OUT/'own-mutant'; own.mkdir(exist_ok=True)
for p in raw.glob('log-*.txt'): shutil.copyfile(p,own/p.name)
b=(own/f'log-{target}.txt').read_bytes(); needle=b'\x1b[36;1mpython .claude/dev/packet_loop_test.py\x1b[0m'
assert b.count(needle)==1
(own/f'log-{target}.txt').write_bytes(b.replace(needle,b'\x1b[36;1mpython .claude/dev/packet_loop_test.py --reviewer-mutant\x1b[0m'))
script=OUT/'doi_chieu_own_mutant.py'; script.write_text(src.replace('/tmp/do650/',str(own)+'/'))
p=run('reviewer-mutant',['python3','-B',str(script)]); d=json.loads(p.stdout)
assert p.returncode==0 and d[target]['all_in_order'] is False
print('REVIEWER_EXPECTED_REJECTION',json.dumps(d[target]))
# Scope probe: erase a run-body block; this checker only proves subsequence matching.
delete=OUT/'deleted-body'; delete.mkdir(exist_ok=True)
for p in raw.glob('log-*.txt'): shutil.copyfile(p,delete/p.name)
lines=b.splitlines(keepends=True); hits=[i for i,x in enumerate(lines) if needle in x]; assert len(hits)==1
del lines[hits[0]]
(delete/f'log-{target}.txt').write_bytes(b''.join(lines))
script=OUT/'doi_chieu_deleted_body.py'; script.write_text(src.replace('/tmp/do650/',str(delete)+'/'))
p=run('reviewer-deletion-scope',['python3','-B',str(script)]); d=json.loads(p.stdout)
assert p.returncode==0 and d[target]['all_in_order'] is True and d[target]['runs_in_log']==7
print('SCOPE_SUBSEQUENCE_ONLY',json.dumps(d[target]),'must read counts and verify API steps; not an acceptance validator')
print('ORIGINAL_LOG_UNCHANGED',hashlib.sha256(master.read_bytes()).hexdigest())
