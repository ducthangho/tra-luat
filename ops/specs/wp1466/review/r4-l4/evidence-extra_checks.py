from pathlib import Path
import subprocess,sys,json,ast,hashlib,re,dis,types,os
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';P=O/'prototype';sys.dont_write_bytecode=True;sys.path[:0]=[str(R/'ops'),str(R/'.claude/dev')]
import ci_duong_nhanh as c
paths=['docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py']
for p in paths:print('CI_PR',p,c.phan_loai_packet_loop('pull_request',[p]))
print('CI_PUSH',c.phan_loai_packet_loop('push',paths))
for root in [R,P]:
 for cmd in ['doctrine-scan','adr-song']:
  q=subprocess.run([sys.executable,'-B',str(root/'.claude/dev/packet_loop.py'),cmd,'--root',str(root)],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'probes')));print('DIRECT_GATE',root.name,cmd,q.returncode,q.stdout.strip(),q.stderr.strip())
q=subprocess.run(['git','-C',str(R),'show','origin/ops/wp1460-r1:ops/specs/wp1460-r1/SPEC.md'],capture_output=True);assert q.returncode==0;(O/'packet-1460-spec.md').write_bytes(q.stdout)
text=q.stdout.decode();lines=text.splitlines();a=next(i for i,s in enumerate(lines) if s.startswith('## Write set'));print('WP1460_WRITESET','\n'.join(lines[a:a+12]))
# Bytecode inspection only, no execution of candidate modules. Assignment of old values is harmless in these fixtures.
for mode in ['ma','test']:
 file='packet_loop.py' if mode=='ma' else 'packet_loop_test.py';old='RC_ADR' if mode=='ma' else 'ROOT'
 for name in ['clean','new_function_default_binding','new_function_decorator_binding']+(['new_class_body_binding','new_function_annotation_binding'] if mode=='ma' else []):
  p=O/'n8'/(mode+'-'+name+'.py')
  if not p.exists():continue
  try:code=compile(p.read_text(),str(p),'exec')
  except SyntaxError as e:print('COMPILE',mode,name,'SYNTAX_ERROR',str(e));continue
  stores=[(i.opname,i.argval,i.starts_line) for i in dis.get_instructions(code) if i.opname in ['STORE_NAME','STORE_GLOBAL'] and i.argval==old]
  nested=[]
  for obj in code.co_consts:
   if isinstance(obj,types.CodeType) and obj.co_name=='_inv_probe':nested=[(i.opname,i.argval) for i in dis.get_instructions(obj) if i.opname=='STORE_GLOBAL' and i.argval==old]
  print('COMPILE',mode,name,'OK','MODULE_OLD_STORES',stores,'CLASS_GLOBAL_STORES',nested)
# Counts of direct callers on base, plus fixed anchors on prospective baseline.
source=(R/'.claude/dev/packet_loop_test.py').read_text();print('BASE_CLI_DOCTRINE_STRING',source.count('"doctrine-scan"'))
adapters=[]
for d in ['.claude/skills','.agents/skills']:
 for p in (R/d).rglob('*.md'):
  if 'doctrine-scan --root .' in p.read_text():adapters.append(str(p.relative_to(R)))
print('ADAPTERS',len(adapters),adapters)
print('CI_WORKFLOW_CALLS',(R/'.github/workflows/ci.yml').read_text().count('doctrine-scan --root .'))
for p,mark in [('.claude/dev/packet_loop.py','    proto_words = _doc_nguon_protocol(root)'),('.claude/dev/packet_loop.py','9 bảng ADR §20 lệch với docs/adr/'),('.claude/dev/packet_loop_test.py','protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=')]:print('BASE_N8_ANCHOR',mark,(R/p).read_text().count(mark))
for f,h in [('mu.log','8c8a1a35f40685170bd82d2510e5c6cee6dadf9316ea0bb53c88d3ede791e3da'),('cu.log','8e719e79ee3e345468a1770591b8ae85ac2961d781a00629e404365d35f95ef8')]:print('AUTHOR_LOG_HASH',f,hashlib.sha256((R/'ops/specs/wp1466/nguyen-mau-r4'/f).read_bytes()).hexdigest()==h)
print('R3_VERDICT_HASH',hashlib.sha256((R/'ops/specs/wp1466/review/r3-l3/VERDICT.md').read_bytes()).hexdigest())
