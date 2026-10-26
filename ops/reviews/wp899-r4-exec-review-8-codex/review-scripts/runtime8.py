import importlib.util, json, os, pathlib, platform, subprocess, sys, yaml
R=pathlib.Path(__file__).resolve().parent;rows=[]
for cmd in ([sys.executable,'--version'],['git','--version'],['codex','--version'],[sys.executable,'-m','ruff','--version'],['git','merge-base','--is-ancestor','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],['git','diff','--check','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD']):
    p=subprocess.run(cmd,capture_output=True);rows.append({'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
thread=os.environ.get('CODEX_THREAD_ID');ident=[]
if thread:
    for p in pathlib.Path('/root/.codex/sessions').rglob('*'+thread+'*.jsonl'):
        selected=[]
        for line in p.open():
            try:v=json.loads(line)
            except ValueError:continue
            if v.get('type')=='session_meta':selected.append({'type':'session_meta',**{k:v.get('payload',{}).get(k) for k in ('id','cli_version','originator','model_provider','cwd')}})
            if v.get('type')=='turn_context':selected.append({'type':'turn_context',**{k:v.get('payload',{}).get(k) for k in ('model','effort','cwd')}})
        ident.append({'source':str(p),'metadata':selected})
out={'commands':rows,'platform':platform.platform(),'executable':sys.executable,'pyyaml':yaml.__version__,'thread':thread,'identity':ident};(R/'runtime8-results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False,indent=2))
