from pathlib import Path
import sys,subprocess,concurrent.futures,json,time
O=Path(__file__).resolve().parent;P=O/'prototype';S=O.parent/'cay-kho/ops/specs/wp1466/nguyen-mau-r4';D=O/'n8';D.mkdir(exist_ok=True)
# Capture exactly the author's declared 13+7 variants without executing their runner.
variants=[]
for mode in ['ma','test']:
 file='packet_loop.py' if mode=='ma' else 'packet_loop_test.py';h=(P/'.claude/dev'/file).read_text()
 def collect(name,s,want,mode=mode,file=file):variants.append((mode,name,s,want,file,'declared'))
 src=(S/'thu_pv.py').read_text();body=src[src.index('def R('):src.index('print(f"TONG')];exec(body,{'che_do':mode,'h':h,'thu':collect})
 variants.append((mode,'clean',h,True,file,'control'))
 if mode=='ma':
  at='def cmd_doctrine_scan(a, state_dir: Path) -> int:\n'
  extra={
   'new_function_default_binding':'def _inv_probe(x=(RC_ADR := RC_ADR)):\n    return x\n\n\n',
   'new_function_annotation_binding':'def _inv_probe(x: (RC_ADR := RC_ADR)):\n    return x\n\n\n',
   'new_function_decorator_binding':'@(_INV_identity := (lambda f: f))\n@((RC_ADR := RC_ADR) and _INV_identity)\ndef _inv_probe():\n    return None\n\n\n',
   'new_class_body_binding':'class _inv_probe:\n    global RC_ADR\n    RC_ADR = RC_ADR\n\n\n',
   'except_binding':'try:\n    pass\nexcept Exception as RC_ADR:\n    pass\n_INV_probe = None\n\n\n',
   'old_function_decorator':'@staticmethod\n',
  }
  for name,ins in extra.items():variants.append((mode,name,h.replace(at,ins+at,1),False,file,'independent'))
  # Decorator's innocuous side effect occurs at function definition time. The CLI module is not executed.
 else:
  at='\n\nif __name__ =='
  extra={'new_function_default_binding':'\ndef _inv_probe(x=(ROOT := ROOT)):\n    return x\n',
         'new_function_decorator_binding':'\n@(_INV_identity := (lambda f: f))\n@((ROOT := ROOT) and _INV_identity)\ndef _inv_probe():\n    return None\n'}
  for name,ins in extra.items():variants.append((mode,name,h.replace(at,ins+at,1),False,file,'independent'))
def run(v):
 mode,name,source,want,file,kind=v;p=D/(mode+'-'+name.split(' ')[0]+'.py');p.write_text(source);t=time.time()
 r=subprocess.run([sys.executable,'-B',str(O/'n8_spec.py'),mode,str(O/('base-'+file)),str(p)],capture_output=True,text=True)
 row={'mode':mode,'name':name,'kind':kind,'expected_rc0':want,'rc':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'seconds':round(time.time()-t,2)}
 print(json.dumps(row,ensure_ascii=False),flush=True);return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:rows=list(ex.map(run,variants))
(O/'n8-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
for mode in ['ma','test']:
 rs=[r for r in rows if r['mode']==mode and r['kind']=='declared'];print('DECLARED_MATRIX',mode,'RED',sum(r['rc']!=0 for r in rs),'GREEN',sum(r['rc']==0 for r in rs),'EXPECTED_MATCH',sum((r['rc']==0)==r['expected_rc0'] for r in rs),len(rs),flush=True)
