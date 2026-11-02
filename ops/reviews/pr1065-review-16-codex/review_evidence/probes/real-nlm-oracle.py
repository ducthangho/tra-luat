from pathlib import Path
import subprocess,sys,json,shutil,os,venv,zipfile
r=Path(__file__).resolve().parents[1]
s=(r/'probes/third-paths.ps1').read_text();needle='if ($Log) {';assert s.count(needle)==1
extra='''# Actual offline pip and metadata, two real interpreters for stale launcher control.
$realShim=@'
#!/usr/bin/python3
import os,sys,subprocess,json
target=os.environ['REVIEW_NLM_CLI_PY'] if sys.argv[0].endswith('nlm.exe') else os.environ['REVIEW_NLM_PY']
args=['-m','notebooklm_fixture',*sys.argv[1:]] if sys.argv[0].endswith('nlm.exe') else sys.argv[1:]
p=subprocess.run([target,*args],capture_output=True,text=True)
with open(os.environ['REVIEW_USER_LOG'],'a') as f:
 f.write(json.dumps({'exe':sys.argv[0],'real_python':target,'argv':sys.argv[1:],'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})+'\\n')
sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);sys.exit(p.returncode)
'@
foreach($e in "$base/nlm/Scripts/python.exe", "$base/nlm/Scripts/nlm.exe") {
 [IO.File]::WriteAllText($e,$realShim); & /bin/chmod +x $e
}
'''
(r/'probes/real-nlm.ps1').write_text(s.replace(needle,extra+needle))
base=r/'fixtures/real-nlm';base.mkdir(parents=True,exist_ok=True);wheels=base/'wheels';wheels.mkdir(exist_ok=True)
env={**os.environ,'PIP_NO_INDEX':'1','PIP_FIND_LINKS':str(wheels),'PIP_CONFIG_FILE':os.devnull,'PIP_DISABLE_PIP_VERSION_CHECK':'1','PIP_DRY_RUN':'0','PIP_CACHE_DIR':str(base/'pip-cache')}
py={}
setup=[]
for version in ['0.4.0','0.5.0']:
 dist=f'notebooklm_mcp_cli-{version}.dist-info';wheel=wheels/f'notebooklm_mcp_cli-{version}-py3-none-any.whl'
 with zipfile.ZipFile(wheel,'w') as z:
  z.writestr(f'{dist}/METADATA',f'Metadata-Version: 2.1\nName: notebooklm-mcp-cli\nVersion: {version}\n')
  z.writestr(f'{dist}/WHEEL','Wheel-Version: 1.0\nGenerator: reviewer-local-fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
  z.writestr('notebooklm_fixture.py',"import importlib.metadata as m,sys,json\nprint('nlm version '+m.version('notebooklm-mcp-cli') if sys.argv[1:]==['--version'] else json.dumps({'mode':'file'}))\n")
  z.writestr(f'{dist}/RECORD','')
 d=base/('venv-'+version);venv.EnvBuilder(with_pip=True).create(d);py[version]=str(d/'bin/python')
 cmd=[py[version],'-m','pip','install',str(wheel)];p=subprocess.run(cmd,env=env,capture_output=True,text=True)
 setup.append(dict(command=cmd,rc=p.returncode,stdout=p.stdout,stderr=p.stderr));assert p.returncode==0
rows=[]
for mode,cli in [('real-nlm-control','0.5.0'),('real-nlm-stale','0.4.0')]:
 fixture=base/mode;log=r/'evidence'/(mode+'.json');e={**env,'REVIEW_NLM_PY':py['0.5.0'],'REVIEW_NLM_CLI_PY':py[cli]}
 cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/real-nlm.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 p=subprocess.run(cmd,env=e,capture_output=True,text=True,timeout=60);(r/'evidence'/(mode+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());events=[json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()];v=next(x for x in d['ket_qua'] if x['cong_cu']=='nlm')
 after=[]
 for args in [['-c',"import importlib.metadata as m; print(m.version('notebooklm-mcp-cli'))"],['-m','pip','index','versions','notebooklm-mcp-cli','--disable-pip-version-check']]:
  q=subprocess.run([py['0.5.0'],*args],env=e,capture_output=True,text=True);after.append(dict(argv=args,rc=q.returncode,stdout=q.stdout,stderr=q.stderr))
 summary=dict(mode=mode,product_rc=p.returncode,ok=d['ok'],errors=d['loi'],nlm=v,direct_after=after,real_calls=[x for x in events if 'real_python' in x])
 print(json.dumps(summary,ensure_ascii=False),flush=True);rows.append(dict(command=cmd,summary=summary,data=d,events=events))
(r/'evidence/real-nlm-oracle.json').write_text(json.dumps(dict(setup=setup,results=rows),ensure_ascii=False,indent=2))
assert rows[0]['summary']['ok'] and rows[0]['summary']['product_rc']==0
print('Real NLM stale launcher:', 'FALSE SUCCESS' if rows[1]['summary']['ok'] else 'REJECTED')
shutil.rmtree(base)
raise SystemExit(1 if rows[1]['summary']['ok'] else 0)
