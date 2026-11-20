import os,sys,pathlib,importlib.util,subprocess,shutil,json,tempfile,hashlib,collections,ast,io,tarfile
from unittest.mock import patch
import yaml
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
t=load(r/'ops/gate_output_doi_chieu_test.py','tests');g=load(r/'ops/gate_output_doi_chieu.py','prod'); results=[]
def record(name,value,expected):
 ok=value==expected;results.append({'name':name,'value':value,'expected':expected,'ok':ok});print(name, 'PASS' if ok else 'FAIL',repr(value),flush=True)
mode=sys.argv[1]
if mode=='prior':
 for value in [[],None,5,'other',{'unrelated':'value'}]:
  with t.mini('T-v3-pass') as (f,d):
   (d/'other.yaml').write_text(yaml.safe_dump(value));record('F01:'+repr(value),g.kiem_tep(f,d),('passed',[]))
 for label,data,expected in [('yaml',b'a: [\n','ParserError'),('utf8',b'\xff','UnicodeDecodeError')]:
  with t.mini('T-v3-pass') as (f,d):
   (d/'bad.yaml').write_bytes(data);record('F02:'+label,g.kiem_tep(f,d),('not_measured',[expected]))
 with t.mini('T-v3-pass') as (f,d):
  (d/'alias.yaml').symlink_to(d/'prov.yaml');record('F02:symlink',g.kiem_tep(f,d),('not_measured',['symlink']))
 with t.mini('T-v3-pass') as (f,d):
  (d/'child').mkdir();shutil.copy(d/'prov.yaml',d/'child/prov.yaml');record('G01:two',g.kiem_tep(f,d),('not_measured',['provenance_nhieu']))
  saved=os.scandir
  def fail(p,*a,**kw):
   if pathlib.Path(p)==d/'child':raise PermissionError('probe child')
   return saved(p,*a,**kw)
  with patch.object(os,'scandir',fail):record('G01:walkerror',g.kiem_tep(f,d),('not_measured',['PermissionError']))
 with t.ho_so_tam() as d:
  src=next((r/'ops/land').glob('pr1378*-land-evidence.yaml'));doc=yaml.safe_load(src.read_bytes()); shared={'gate_output':'not_measured'}
  doc['probe_shared']=[shared,shared];record('F03:shared_alias',len([x for x in g.loi_khai(doc) if 'probe_shared' in x[0]]),2)
  doc['probe_cycle']=doc;p=d.parent/'cycle-land-evidence.yaml';p.write_text(yaml.safe_dump(doc,allow_unicode=True))
  p1=subprocess.run([sys.executable,'-B',str(r/'ops/gate_output_doi_chieu.py'),'kiem-ho-so',str(p)],capture_output=True,text=True);record('F03:cycle',(p1.returncode,'Traceback' in p1.stderr),(2,False))
 for name,a,b in [('file','/tmp/'+pathlib.Path(t.FX['T-v3-pass'][0]).name*10,str(r)),('directory',str(r/t.FX['T-v3-pass'][0]),'/tmp/'+pathlib.Path(t.FX['T-v3-pass'][1]).parent.name*30)]:
  p=subprocess.run([sys.executable,'-B',str(r/'ops/gate_output_doi_chieu.py'),'kiem-tep',a,'--provenance',b],capture_output=True,text=True);record('H02:'+name,(p.returncode,'Traceback' in p.stderr),(2,False))
if mode=='corpus':
 k=load(r/'ops/kiem_ho_so_land.py','land');nguon=load(r/'ops/land_evidence_nguon.py','nguon')
 # Immutable acceptance baseline requested by owner, independent from test BASE.
 with t.cay_tai('0f9aa2a2cc697129e1f5be72feddf60986286865','ops/land') as root:
  top=root/'ops/land';counts=collections.Counter();rows=[]
  for f in sorted(top.glob('**/danh-gia-gate-output-*.txt')):
   tt,ly=g.kiem_tep(f,top/f.relative_to(top).parts[0]);counts[tt]+=1;rows.append([str(f.relative_to(root)),tt,ly])
  record('66 files',dict(counts),{'passed':47,'failed':10,'not_measured':9})
  cs=collections.Counter();landed=diff=0;hsrows=[]
  for f in sorted(top.glob('*-land-evidence.yaml')):
   b=f.read_bytes();doc=yaml.safe_load(b.decode());landed+=g.la_landed(doc);diff+=g.la_landed(doc)!=k._xet_mot_tep(f,yaml)[2]
   claims=g.loi_khai(doc);vp=g.kiem_ho_so(doc,top/(f.name[:-len('-land-evidence.yaml')]+'-provenance'))
   state='MIEN_CUTOVER' if nguon.MIEN_TRU_CUTOVER.get(f.name)==hashlib.sha256(b).hexdigest() else 'DO' if vp else 'DAT' if claims else 'KHONG_LOI_KHAI';cs[state]+=1;hsrows.append([f.name,state,vp])
  record('170 records',dict(cs),{'MIEN_CUTOVER':25,'DO':56,'DAT':39,'KHONG_LOI_KHAI':50});record('landed',(landed,diff),(94,0))
  scripts=collections.Counter(hashlib.sha256(f.read_bytes()).hexdigest() for f in top.glob('**/danh_gia_gate.py'));record('BO_SINH set',set(scripts),set(g.BO_SINH)); print('scripts',dict(scripts))
  (w/'corpus_details.json').write_text(json.dumps({'files':rows,'records':hsrows,'scripts':dict(scripts)},ensure_ascii=False,indent=2))
if mode=='simplifications':
 p=w/'before_simplifications.py';p.write_bytes(subprocess.check_output(['git','show','89fb99b:ops/gate_output_doi_chieu.py'],cwd=r));old=load(p,'old')
 for body in [None,False,0,'',[],{},t.DONG]:
  with tempfile.TemporaryDirectory() as d:
   d=pathlib.Path(d);(d/'readback-test-issuecomment-123.json').write_text(json.dumps(t.rb(body)))
   record('body:'+repr(body),g.kiem_mien(t.URL+' '+t.SHA,d,None),old.kiem_mien(t.URL+' '+t.SHA,d,None))
 with tempfile.TemporaryDirectory() as d:
  d=pathlib.Path(d);(d/'file').write_text('x');(d/'link').symlink_to(d,target_is_directory=True)
  for p in [d,d/'absent',d/'file',d/'link']:
   record('glob:'+p.name,g.kiem_mien(t.URL,p,None),old.kiem_mien(t.URL,p,None))
 with t.mini('T-v3-pass') as (f,d),tempfile.TemporaryDirectory() as other:
  p=pathlib.Path(other);shutil.copy(d/'prov.yaml',p/'pv.yaml');(d/'link').symlink_to(p,target_is_directory=True)
  record('walk skip symlink',g.kiem_tep(f,d),old.kiem_tep(f,d))
 for tt in ['passed','failed','not_measured']:
  for conclusion in ['success','failure','cancelled','skipped','']:
   a=(tt=='passed' and conclusion!='success') or (conclusion!='success' and tt!='failed');b=conclusion!='success' and tt!='failed';record('K5:'+tt+'/'+conclusion,a,b)
if mode=='dotpath':
 with t.ho_so_tam() as d:
  for ref in [t.ten_tep('T-v3-pass'),'./'+t.ten_tep('T-v3-pass')]:
   record(ref,g.kiem_ho_so({'gate_output':'passed — '+ref},d),[])
(w/(mode+'_probes.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2,default=lambda x:sorted(x)))
sys.exit(0 if all(x['ok'] for x in results) else 1)
