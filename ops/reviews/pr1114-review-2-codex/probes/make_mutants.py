import pathlib,json,shutil
root=pathlib.Path(__file__).resolve().parents[1]
source=(root/'work/head/ops/cloud_agent_creds.py').read_text()
test=(root/'work/head/ops/cloud_agent_creds_test.py').read_text()
anchor='os.killpg(p.pid, signal.SIGKILL) if os.name != "nt" else p.kill()'
assert source.count(anchor)==1
out=root/'work/mutations';out.mkdir(exist_ok=True)
rows=[]
for mode,replacement in [('parent_only','p.kill()'),('no_kill','None')]:
 p=out/(mode+'.py');p.write_text(source.replace(anchor,replacement))
 rows.append(dict(mode=mode,path=str(p.relative_to(root)),anchor=anchor,replacement=replacement))
assert test.count(', cho_chet=0)')==1
p=root/'work/head/ops/review_a9_default.py'
p.write_text(test.replace(', cho_chet=0)',')'))
rows.append(dict(mode='a9_default',path=str(p.relative_to(root)),anchor=', cho_chet=0)',replacement=')'))
(root/'evidence/mutant-definitions.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(rows,ensure_ascii=False,indent=2))
