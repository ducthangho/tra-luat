import audit as A
import ast, contextlib, io, json, os, pathlib, sys, tempfile, types
T=A.T

def state():return [sys.get_int_max_str_digits(),os.environ.get(T._E)]
def outcome(f):
 try:f();return 'pass'
 except BaseException as e:return type(e).__name__+': '+str(e)

def ghim():
 original=state(); events=[]
 real_run=T.subprocess.run
 def traced(cmd,*args,**kw):
  events.append({'command':cmd[:3],'parent':state(),'child_env':kw.get('env',os.environ).get(T._E)})
  return real_run(cmd,*args,**kw)
 T.subprocess.run=traced
 try:
  for lim,env in [(0,None),(0,'0'),(640,None),(640,'640'),(4300,'0')]:
   sys.set_int_max_str_digits(lim)
   if env is None:os.environ.pop(T._E,None)
   else:os.environ[T._E]=env
   before=state();records=[];active=[]
   def probe(raw,**kw):
    active.append(state());return A.M.kiem_json(raw,**kw)
   proxy=types.SimpleNamespace(kiem_json=probe,__file__=A.M.__file__)
   cases={
    'direct_ca':lambda:T.ca(proxy,'long_limit',T._SO(T.LIM),()),
    'direct_ca_error':lambda:T.ca(proxy,'wrong',T.ma(T.FIX),('K1',)),
    'chay_ca':lambda:T.chay_ca(proxy,T.MODUN,{'so_dai_gioi_han','so_dai_vuot'}),
    'ca_thu_tu':lambda:T.ca_thu_tu('thu_tu_k1',A.M),
    'ca_dang_ky':lambda:T.ca_dang_ky('dang_ky'),
    'ca_cli':lambda:T.ca_cli('cli',T.MODUN,proxy),
    'ca_tinh':lambda:T.ca_tinh('tinh',A.M),
    'mutant_M2j':lambda:T.chay_dot_bien(A.SRC,next(r for r in T.DB if r[0]=='M2j')),
    'mutant_M5g':lambda:T.chay_dot_bien(A.SRC,next(r for r in T.DB if r[0]=='M5g')),
   }
   for name,fn in cases.items():
    res=outcome(fn); records.append({'name':name,'result':res,'after':state()});assert state()==before
    if name!='direct_ca_error':assert res=='pass',records[-1]
    else:assert res.startswith('TinHieuChotCa:'),res
   nested=[]
   for ex in (ValueError,KeyboardInterrupt,SystemExit):
    def inner():
     nested.append(['inner',state()]);assert state()==[4300,'4300'];raise ex('control')
    def outer():
     nested.append(['outer_before',state()]);res=outcome(T._ghim(inner));nested.append(['outer_after',state(),res]);assert state()==[4300,'4300']
    assert outcome(T._ghim(outer))=='pass';assert state()==before
   assert all(x==[4300,'4300'] for x in active)
   A.emit(kind='ghim_matrix',before=before,after=state(),calls=records,active=active,nested=nested)
  assert all(e['parent']==[4300,'4300'] and e['child_env']=='4300' for e in events)
  A.emit(kind='child_pinning',children=len(events),all_pinned=True,events=events)
 finally:
  T.subprocess.run=real_run;sys.set_int_max_str_digits(original[0])
  if original[1] is None:os.environ.pop(T._E,None)
  else:os.environ[T._E]=original[1]
 # Raw function retained only in each wrapper closure, not in tables/defaults/globals.
 raw={name:next(c.cell_contents for c in getattr(T,name).__closure__ if callable(c.cell_contents)) for name in ('ca','ca_cli','ca_tinh')}
 aliases={name:[k for k,v in vars(T).items() if v is fn] for name,fn in raw.items()}
 assert all(not names for names in aliases.values())
 A.emit(kind='global_aliases',unwrapped_aliases=aliases,wrapped_names={n:getattr(T,n).__name__ for n in raw},ca_table_callable_names=sorted({getattr(c[1],'__name__','bytes') for c in T.CA}))

def k4():
 old='[f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]'
 targets=['duong_fixture','k4_base','k4_head','k4_ca_hai','a11_k3_k4','kieu_S','kieu_H']
 variants={}
 for sep in (' ',':',': ',' : '):
  for receipt in ('','receipt '):
   for phrase in ('stale, chay lai','stale, chạy lại'):
    name='valid_'+repr((sep,receipt,phrase))
    variants[name]=A.edit(old,'[f"{k}'+sep+receipt+phrase+'" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]]')
 for name,msg in [('fresh','K4:S fresh, khong can chay lai'),('suffix','K4:S stale, chay lai, fresh'),('duplicate','K4:S stale, chay lai'),('space_prefix',' K4:S fresh, khong can chay lai'),('tab_prefix','\tK4:S fresh, khong can chay lai'),('K40','K40:S fresh, khong can chay lai'),('K3_mentions_K4','K3: K4 la ten workflow')]:
  anchor='    ghi("K5",'
  variants[name]=A.edit(anchor,'    ly_do += ['+repr(msg)+'] if base_hien_hanh != r["S"] else []\n'+anchor)
 for name,src in variants.items():
  with tempfile.TemporaryDirectory() as td:
   p=pathlib.Path(td)/'m.py';p.write_text(src);m=A.load(p,'k4_'+name)
   results={c:A.target(m,p,c) for c in targets}
   A.emit(kind='k4_matrix',name=name,results=results)
   if name.startswith('valid_'):assert all(v=='pass' for v in results.values())
   if name in ('space_prefix','tab_prefix'):
    A.emit(kind='unseen_K4_label',name=name,result=m.kiem_json(T.ma(T.FIX),kho=T.KHO,nhanh='master',base_hien_hanh=T.X40,head_hien_hanh=T.H))
    A.suite('k4_'+name,src)
 row=next(r for r in T.DB if r[0]=='M5g')
 with tempfile.TemporaryDirectory() as td:
  p=pathlib.Path(td)/'m5g.py';p.write_text(A.edit(row[3],row[4]));m=A.load(p,'M5g_independent')
  A.emit(kind='M5g',baseline=A.target(A.M,T.MODUN,'k4_base'),positive=A.target(m,p,'duong_fixture'),target=A.target(m,p,'k4_base'),disposition=T.chay_dot_bien(A.SRC,row))
  # Put back round-six narrow filter only in a separate imported test copy.
  src=(A.DEV/'doc_receipt_thu_hoi_test.py').read_text();old_filter='if re.match(r"K4\\b", x)';assert src.count(old_filter)==1
  tp=pathlib.Path(td)/'test.py';tp.write_text(src.replace(old_filter,'if x.startswith("K4: ")'));U=A.load(tp,'unfixed_filter')
  A.emit(kind='M5g_old_filter',disposition=U.chay_dot_bien(A.SRC,row))
 for name,repl in [('benign', '    # no behavioral change\n'+row[3]),('too_broad', '    ly_do += ["K4:S fresh"]\n'+row[3]),('wrong_exception','    if r["S"] != base_hien_hanh: raise ValueError("control")\n'+row[3])]:
  changed=(*row[:4],repl,*row[5:]);disp=T.chay_dot_bien(A.SRC,changed)
  A.emit(kind='M5g_credit_control',name=name,disposition=disp);assert disp[0]=='unresolved'
if __name__=='__main__':globals()[sys.argv[2]]()
