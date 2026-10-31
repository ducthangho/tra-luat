from pathlib import Path
import subprocess,sys,json,shutil,os,venv,zipfile
r=Path(__file__).resolve().parents[1]
prototype='--prototype' in sys.argv;label='-prototype' if prototype else ''
s=(r/'probes/third-paths.ps1').read_text();needle='if ($Log) {';assert s.count(needle)==1
extra='''# Real pip on local wheels; driver builds an isolated real venv outside source.
$realShim=@'
#!/usr/bin/python3
import os,sys,subprocess,json
p=subprocess.run([os.environ['REVIEW_REAL_PY'],*sys.argv[1:]],capture_output=True,text=True)
with open(os.environ['REVIEW_USER_LOG'],'a') as f:
 f.write(json.dumps({'exe':sys.argv[0],'real_python':os.environ['REVIEW_REAL_PY'],'argv':sys.argv[1:],'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})+'\\n')
sys.stdout.write(p.stdout);sys.stderr.write(p.stderr);sys.exit(p.returncode)
'@
[IO.File]::WriteAllText("$base/venv/Scripts/python.exe",$realShim); & /bin/chmod +x "$base/venv/Scripts/python.exe"
[IO.File]::WriteAllText("$base/repo/requirements.txt", "PyYAML==6.0.3`njsonschema==4.25.1`n")
'''
(r/'probes/real-pip.ps1').write_text(s.replace(needle,extra+needle))
out=[]
for mode in ['real-pip-control','real-pip-dryrun']:
 fixture=r/'fixtures'/(mode+label);venv_dir=fixture/'real-venv'
 venv.EnvBuilder(with_pip=True).create(venv_dir);realpy=venv_dir/'bin/python';wheels=fixture/'wheels';wheels.mkdir()
 for name,version,module in [('PyYAML','6.0.3','yaml'),('jsonschema','4.25.1','jsonschema')]:
  dist=f'{name}-{version}.dist-info';wheel=wheels/f'{name}-{version}-py3-none-any.whl'
  with zipfile.ZipFile(wheel,'w') as z:
   z.writestr(f'{dist}/METADATA',f'Metadata-Version: 2.1\nName: {name}\nVersion: {version}\n')
   z.writestr(f'{dist}/WHEEL','Wheel-Version: 1.0\nGenerator: reviewer-local-fixture\nRoot-Is-Purelib: true\nTag: py3-none-any\n')
   z.writestr(f'{module}/__init__.py',f'__version__ = {version!r}\n')
   z.writestr(f'{dist}/RECORD','')
 env={**os.environ,'REVIEW_REAL_PY':str(realpy),'PIP_NO_INDEX':'1','PIP_FIND_LINKS':str(wheels),'PIP_CONFIG_FILE':os.devnull,'PIP_DISABLE_PIP_VERSION_CHECK':'1','PIP_DRY_RUN':'1' if mode.endswith('dryrun') else '0','PIP_CACHE_DIR':str(fixture/'pip-cache')}
 version=subprocess.run([str(realpy),'-m','pip','--version'],capture_output=True,text=True,env=env,check=True).stdout.strip()
 log=r/'evidence'/(mode+label+'.json');cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/real-pip.ps1'),'-Mode',mode,'-Log',str(log),'-FixtureRoot',str(fixture)]
 if prototype: cmd += ['-Product',str(r/'hint-prototype/ops/vm/cap-nhat-cong-cu.ps1')]
 p=subprocess.run(cmd,text=True,capture_output=True,timeout=55,env=env);(r/'evidence'/(mode+label+'.log')).write_text(p.stdout+p.stderr)
 d=json.loads(log.read_text());events=[json.loads(x) for x in (fixture/'native.jsonl').read_text().splitlines()]
 after=[]
 for pkg in ['PyYAML','jsonschema']:
  q=subprocess.run([str(realpy),'-c',f"import importlib.metadata as m; print(m.version('{pkg}'))"],text=True,capture_output=True,env=env)
  after.append(dict(package=pkg,rc=q.returncode,stdout=q.stdout.strip(),stderr=q.stderr.strip()))
 v=next(x for x in d['ket_qua'] if x['cong_cu']=='venv-kho')
 good=mode.endswith('control');passed=d['ok']==good and p.returncode==(0 if good else 1)
 summary=dict(mode=mode,passed=passed,pip=version,pip_no_index=env['PIP_NO_INDEX'],pip_dry_run=env['PIP_DRY_RUN'],product_rc=p.returncode,ok=d['ok'],errors=d['loi'],rows=d['tong'],venv=v,actual_pip_events=[x for x in events if 'real_python' in x],direct_after=after)
 out.append(dict(command=cmd,summary=summary,data=d,events=events));print(json.dumps(summary,ensure_ascii=False),flush=True)
 shutil.rmtree(fixture)
(r/('evidence/real-pip-oracle'+label+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f"Real pip oracle: {sum(x['summary']['passed'] for x in out)}/{len(out)} PASS")
raise SystemExit(0 if all(x['summary']['passed'] for x in out) else 1)
