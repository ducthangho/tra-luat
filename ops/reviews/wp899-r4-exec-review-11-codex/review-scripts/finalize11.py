import hashlib, json, pathlib, re, subprocess, sys
R=pathlib.Path(__file__).resolve().parent
start=json.loads((R/'snapshot-start.json').read_text())
end=json.loads((R/'snapshot-end.json').read_text())
changed=[p for p in set(start['files'])|set(end['files']) if start['files'].get(p)!=end['files'].get(p)]
commands_equal=[(x['command'],x['rc'],x['stdout'],x['stderr']) for x in start['commands']]==[(x['command'],x['rc'],x['stdout'],x['stderr']) for x in end['commands']]
cmp={'files_start':len(start['files']),'files_end':len(end['files']),'changed_paths':sorted(changed),'commands_equal':commands_equal,
     'scope':'assigned checkout, all files except .git internals and .review scratch; boundary snapshots only',
     'head':'1f731c7bfc99c8fca3cba74d4cd8bbf6a14db986','tree':'13843e747b31df410a56e83b1dbc2f98a76e7d2d'}
(R/'snapshot-comparison11.json').write_text(json.dumps(cmp,ensure_ascii=False,indent=2))
assert not changed and commands_equal and len(start['files'])==len(end['files'])==16771,cmp
z=subprocess.run([sys.executable,'-B',str(R/'render11.py')],capture_output=True)
assert z.returncode==0,z.stderr.decode()
verdict=(R/'VERDICT.md').read_bytes()
assert verdict.startswith(b'verdict: approve\n')
assert b'Reviewed commit: 1f731c7bfc99c8fca3cba74d4cd8bbf6a14db986\n' in verdict
checks=[]
for label in ('suite','closed','patch','yaml-fixtures','generator-audit','equivalences','operators','criteria','classifier-pipeline','replay','history','product-new-oracle'):
    row=json.loads((R/(label+'.json')).read_text())
    assert row['rc']==0
    for channel in ('stdout','stderr'):
        actual=hashlib.sha256((R/(label+'.'+channel+'.txt')).read_bytes()).hexdigest()
        assert actual==row[channel+'_sha256']
    checks.append(label)
(R/'final-readback11.json').write_text(json.dumps({'verdict_sha256':hashlib.sha256(verdict).hexdigest(),'verdict_size':len(verdict),
        'render_command':[sys.executable,'-B',str(R/'render11.py')],'render_rc':z.returncode,'render_stdout':z.stdout.decode(),
        'positive_receipt_hashes_verified':checks,'snapshot_comparison':cmp},ensure_ascii=False,indent=2))
files={}
for p in sorted(R.rglob('*')):
    if p.is_file() and p.name!='evidence-manifest11.json':
        files[str(p.relative_to(R))]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(R/'evidence-manifest11.json').write_text(json.dumps({'reviewed_sha':cmp['head'],'reviewed_tree':cmp['tree'],
        'verdict_sha256':hashlib.sha256(verdict).hexdigest(),'files':files},ensure_ascii=False,indent=2))
print('READBACK: approve; HEAD/tree anchored; 16771/16771 files unchanged; stable artifact hashes',len(files))
print('VERDICT SHA256',hashlib.sha256(verdict).hexdigest())
