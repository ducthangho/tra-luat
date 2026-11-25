from pathlib import Path
import json,subprocess,sys,hashlib,os
O=Path(__file__).resolve().parent;P=O/'prototype';D=O/'probes';D.mkdir(exist_ok=True)
raw=(P/'docs/PROTOCOL_DA_PHIEN.md').read_bytes();locks=json.loads((O/'locks.json').read_text());results=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(D))
def run(name,b,want):
 d=D/name;(d/'docs').mkdir(parents=True,exist_ok=True);(d/'docs/PROTOCOL_DA_PHIEN.md').write_bytes(b)
 r=subprocess.run([sys.executable,'-B',str(P/'.claude/dev/packet_loop.py'),'doctrine-scan','--root',str(d)],capture_output=True,text=True,env=env)
 row={'case':name,'rc':r.returncode,'expected':want,'bytes_changed':b!=raw,'stdout':r.stdout.strip(),'stderr':r.stderr.strip(),'sha256':hashlib.sha256(b).hexdigest()};results.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
run('baseline',raw,0)
for k,v in locks.items():
 u=v['unit'].encode();assert raw.count(u)==1
 run('delete_'+k,raw.replace(u,b'',1),9)
 run('crlf_inside_'+k,raw.replace(u,u.replace(b'\n',b'\r\n',1),1),9)
 run('tab_indent_'+k,raw.replace(u,b'\n'.join(b'\t'+line for line in u.split(b'\n')),1),9)
 run('trailing_space_'+k,raw.replace(u,u+b' ',1),9)
 if v['index']:
  run('duplicate_'+k,raw+b'\n\n'+u+b'\n',9)
  run('relocate_'+k,raw.replace(u,b'Mot doan ghi chu thu nghiem.',1)+b'\n\n'+u+b'\n',9)
for k in ['K04','K05']:
 u=locks[k]['unit'].encode();run('insert_block_before_'+k,raw.replace(u,b'Doan bien tap thu nghiem.\n\n'+u,1),9)
# Cover old identifier variants and headings cardinality, with harmless table text only.
for name,line in [('plain',b'INV-01 | ghi chu'),('compact',b'|`INV-01`|ghi chu|'),('canonical',b'| `INV-01` | ghi chu |'),('debt',b'| INV-01-NO | ghi chu |')]:run('id_'+name,raw+b'\n\n'+line+b'\n',0 if name=='debt' else 9)
u=locks['K01']['unit'].encode();run('duplicate_K01_same_ancestor',raw.replace(u,u+b'\n\n'+u,1),9)
run('relocate_K01',raw.replace(u,b'',1)+b'\n\n## Phu luc thu nghiem\n\n'+u+b'\n',9)
# Freeze only protocol bytes, not real docs outside units: this is the documented intentional price.
run('append_unlocked_note',raw+b'\nGhi chu bien tap thu nghiem.\n',0)
(O/'probes-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print('SUMMARY',len(results),'MISMATCH',[(r['case'],r['rc'],r['expected']) for r in results if r['rc']!=r['expected']])
