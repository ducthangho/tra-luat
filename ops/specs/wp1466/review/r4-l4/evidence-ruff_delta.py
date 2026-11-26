from pathlib import Path
import subprocess,json,collections
O=Path(__file__).resolve().parent
version=subprocess.run(['ruff','--version'],capture_output=True,text=True);print('VERSION',version.stdout.strip(),'RC',version.returncode)
allrows={}
for label,root in [('base',O/'auditor/base'),('prototype',O/'prototype')]:
 cmd=['ruff','check','--no-cache','--select','F','--output-format','json','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py']
 r=subprocess.run(cmd,cwd=root,capture_output=True,text=True);(O/f'ruff-{label}.json').write_text(r.stdout);rows=json.loads(r.stdout);allrows[label]=rows
 print('COMMAND',label,' '.join(cmd),'RC',r.returncode,'COUNT',len(rows),'CODES',dict(collections.Counter(x['code'] for x in rows)),'STDERR',r.stderr.strip())
def norm(rows):return collections.Counter((Path(x['filename']).name,x['code'],x['message']) for x in rows)
a,b=norm(allrows['base']),norm(allrows['prototype']);print('DELTA_NEW',list((b-a).items()));print('DELTA_REMOVED',list((a-b).items()))
for label,rows in allrows.items():
 for x in rows:print('DIAGNOSTIC',label,Path(x['filename']).name,x['location']['row'],x['code'],x['message'])
# F811 embeds source line numbers in its message. Compare stable enclosing function + source text,
# and remove only the embedded line location, not rule/name/message semantics.
import ast,re

def stable(label,rows):
 root=O/('auditor/base' if label=='base' else 'prototype');out=collections.Counter()
 for x in rows:
  name=Path(x['filename']).name;src=(root/'.claude/dev'/name).read_text();row=x['location']['row'];tree=ast.parse(src)
  scopes=[(n.lineno,n.name) for n in ast.walk(tree) if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and n.lineno<=row<=n.end_lineno]
  scope=tuple(n for _,n in sorted(scopes));line=src.splitlines()[row-1]
  msg=re.sub(r'from line [0-9]+:', 'from line <location>:',x['message'])
  out[(name,scope,x['code'],msg,line)]+=1
 return out
sa,sb=stable('base',allrows['base']),stable('prototype',allrows['prototype'])
print('STABLE_DELTA_NEW',list((sb-sa).items()));print('STABLE_DELTA_REMOVED',list((sa-sb).items()))
