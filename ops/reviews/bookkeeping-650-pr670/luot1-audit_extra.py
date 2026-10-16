import ast, datetime as dt, hashlib, json, pathlib, platform, re, subprocess, yaml
from run_checks import ROOT
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT)
e=json.loads((ROOT/'ops/land/pr666-wp650-provenance/artifact-10956094584-tl-selftest-Linux.json').read_text())
code=git('show','f8a7829:.claude/dev/gate_lifecycle.py'); m=ast.parse(code)
paths=next(ast.literal_eval(n.value) for n in m.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_CATALOG_POLICY_PATHS' for t in n.targets))
assert hashlib.sha256(code).hexdigest()==e['identity']['runner_sha256']
cmd_bytes=(json.dumps(e['command'],ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
assert hashlib.sha256(cmd_bytes).hexdigest()==e['command_sha256']
# ls-files -s representation recreated from the frozen commit's tree, without replacing the index.
rows=git('ls-tree','-r','f8a7829','--',*paths).decode().splitlines()
ls_files='\n'.join(line.split(' ')[0]+' '+line.split(' ')[2].split('\t')[0]+' 0\t'+line.split('\t',1)[1] for line in rows)
assert hashlib.sha256(ls_files.encode()).hexdigest()==e['identity']['catalog_policy_sha256']
print('ARTIFACT_INTERNAL_HASHES','runner/command/catalog MATCH')
elapsed=(dt.datetime.fromisoformat(e['completed_at'])-dt.datetime.fromisoformat(e['started_at'])).total_seconds()
assert abs(elapsed-e['duration_seconds'])<0.001
print('ARTIFACT_TIME',e['started_at'],e['completed_at'],'wall_delta',elapsed,'monotonic_duration',e['duration_seconds'])
v=yaml.safe_load((ROOT/'ops/land/pr666-wp650-provenance.yaml').read_bytes())
for entry in v['bon_moc']:
    wf=yaml.safe_load(git('show','f8a7829:'+entry['run']['path']))
    jobs=json.loads((ROOT/f"ops/land/pr666-wp650-provenance/readback-jobs-{entry['run']['id']}.json").read_text())['jobs']
    for g in entry['gate_output']:
        j=next(x for x in jobs if x['id']==g['id']); defs=wf['jobs'][g['job'].split(' (')[0]]['steps']
        skipped=[s['name'] for s in j['steps'] if s['conclusion']=='skipped']
        for name in skipped:
            step=next(x for x in defs if x.get('name')==name); assert 'if' in step
        assert all(not s.get('continue-on-error') for s in defs)
        raw=pathlib.Path(f"/tmp/do650/log-{g['id']}.txt").read_text().splitlines()
        os_i=next(i for i,x in enumerate(raw) if x.endswith('##[group]Operating System'))
        os_text=' | '.join(x.split('Z ',1)[-1] for x in raw[os_i+1:os_i+4] if not x.endswith('##[endgroup]'))
        runtimes=[x.split('Z ',1)[-1] for x in raw if re.search(r'Successfully set up (CPython|Python)|he: .*\| python:',x)]
        print('JOB_RUNTIME',g['id'],os_text,runtimes,'skipped_all_if=True','continue_on_error=False')
print('ENV',platform.platform(),'python',platform.python_version(),'PyYAML',yaml.__version__)
print('HASHES',hashlib.sha256(git('diff','--binary','origin/master..HEAD')).hexdigest())
