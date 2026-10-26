from pathlib import Path
import re,shutil,json
R=Path('.review').resolve(); root=R.parent; old=root/'.review-input/r4-luot5'
exclude=('setup','bootstrap','write_','final','snapshot','adapt','close','finish_after','legacy_manifest')
for p in old.glob('*.py'):
 if not p.name.startswith(exclude): (R/p.name).write_bytes(p.read_bytes())
for n in (1,2):
 for p in (old/f'prior{n}').rglob('*'):
  rel=p.relative_to(old)
  if p.is_file() and (len(rel.parts)==2 or (len(rel.parts)==3 and rel.parts[1] in ('old1','old2'))):
   if p.suffix=='.py' or p.name=='suite.stdout.txt':
    q=R/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
for p in R.rglob('*.py'):
 if p.name in ('setup6.py','prepare_legacy6.py','run.py'):continue
 s=p.read_text()
 s=re.sub(r'/tmp/claude-0/[^\"\x27\n]*?/scratchpad/r4review\d+/ws',str(root),s)
 s=s.replace('/home/user/tra-luat',str(root))
 s=s.replace('len(base)==48','len(base)==49').replace('48/48','49/49').replace('47/48','48/49').replace('209/209','231/231')
 p.write_text(s)
# Adjust only changed env helper signature in measurement copies; keep old names, log the transformations.
repls=[('_env_chan(wf.get("env"))','_env_chan(wf)'),('any(str(k).startswith("CI_DANG_KY_") for k in v)','any(str(k).startswith("CI_DANG_KY_") for k in d["env"])'),('list(v)[:1]','list(d["env"])[:1]'),('list(v)[-1:]','list(d["env"])[-1:]'),('return v is not None and (type(v) is not dict','return "env" in d and (type(d["env"]) is not dict'),('return v not in (None, False) and (type(v) is not dict','return "env" in d and d["env"] not in (None, False) and (type(d["env"]) is not dict'),('return v is not None and type(v) is not int and (type(v) is not dict','return "env" in d and type(d["env"]) is not int and (type(d["env"]) is not dict'),('return v not in (None, "") and (type(v) is not dict','return "env" in d and d["env"] not in (None, "") and (type(d["env"]) is not dict'),('return bool(v) and (type(v) is not dict','return "env" in d and bool(d["env"]) and (type(d["env"]) is not dict'),('type(v) is not dict or any(str(k)','type(d["env"]) is not dict or any(str(k)'),('type(v) is str or any(str(k)','type(d["env"]) is str or any(str(k)')]
for name in ('frontier.py','frontier2.py','frontier5.py'):
 p=R/name;s=p.read_text()
 for a,b in repls:s=s.replace(a,b)
 p.write_text(s)
(R/'legacy-adaptations6.json').write_text(json.dumps({'source':str(old),'changes':['absolute paths -> current root','baseline cases 48->49; mutation total209->231','env helper anchors -> parent dict signature'],'env_replacements':repls},indent=2))
print('measurement code copied; historical verdict writers excluded')
