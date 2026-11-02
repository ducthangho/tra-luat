import hashlib,json,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
candidate=root/'cay-kho'
commands=[['rev-parse','HEAD','HEAD^{tree}'],['status','--porcelain','--untracked-files=all'],['ls-files','--others','--ignored','--exclude-standard'],['diff','--exit-code','HEAD'],['diff','--cached','--exit-code','HEAD'],['diff','--check','3bdd987','HEAD']]
rows=[]
for cmd in commands:
 r=subprocess.run(['git','--no-optional-locks','-C',str(candidate),*cmd],capture_output=True,text=True)
 rows.append(dict(command=cmd,rc=r.returncode,stdout=r.stdout,stderr=r.stderr))
 assert r.returncode==0,(cmd,r.stderr)
 if cmd[0]!='rev-parse':assert r.stdout==''
initial=json.loads((root/'evidence/initial-hashes.json').read_text())
changed=[p for p,h in initial.items() if not (candidate/p).is_file() or hashlib.sha256((candidate/p).read_bytes()).hexdigest()!=h]
assert not changed
r=dict(git=rows,tracked_files_hashed=len(initial),changed=changed,copies={})
for name in ['head','base']:
 path=root/'work'/name
 sha=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD']).decode().strip()
 diff=subprocess.run(['git','-C',str(path),'diff','--exit-code','HEAD'],capture_output=True,text=True)
 assert diff.returncode==0
 r['copies'][name]=dict(head=sha,tracked_diff_rc=diff.returncode)
assert (candidate/'ops/cloud_agent_creds_test.py').read_bytes()==(root/'work/head/ops/cloud_agent_creds_test.py').read_bytes()
r['candidate_head_copy_test_identical']=True
(root/'evidence/final-integrity.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False),flush=True)
