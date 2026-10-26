import hashlib, json, pathlib, subprocess
R=pathlib.Path(__file__).resolve().parent;root=R.parent;base='ba222ffd1615f0d74b59985b9612f725211b62f5';prior='9b329bfab0b38a821992a7105d479ca44bed389b';rows=[]
for args in (['remote','get-url','origin'],['rev-parse','HEAD','HEAD^{tree}'],['branch','--show-current'],['merge-base','--is-ancestor',base,'HEAD'],['diff','--name-status',base,'HEAD'],['diff','--numstat',base,'HEAD'],['diff','--check',base,'HEAD'],['config','--get','core.abbrev'],['rev-parse','--is-shallow-repository'],['status','--short']):
    cmd=['git',*args];p=subprocess.run(cmd,cwd=root,capture_output=True);rows.append({'command':cmd,'rc':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode()})
for name,oid in [('base.patch',base),('delta.patch',prior)]:
    p=subprocess.run(['git','diff',oid,'HEAD'],cwd=root,capture_output=True,check=True);(R/name).write_bytes(p.stdout)
specs={}
for p in (root/'.review-input').glob('wp899-r*.md'):
    b=p.read_bytes();specs[p.name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
assert specs['wp899-r4.md']['sha256']=='be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45'
(R/'preflight8-results.json').write_text(json.dumps({'commands':rows,'specs':specs},ensure_ascii=False,indent=2));print('PREFLIGHT exact HEAD/base/diff/spec saved',len(rows),'commands')
