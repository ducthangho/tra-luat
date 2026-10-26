import importlib.util,sys,json
from pathlib import Path
s=importlib.util.spec_from_file_location('t',Path('ops/ci_provenance_test.py'));t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
old=t.bang
rows=[]
def bang(ok,msg):
 f=sys._getframe(1)
 if f.f_code.co_name=='c48_nguyen_van_va_mien':
  for name,p,gh,markers in f.f_locals['hang']:
   g=t.gate(p);rows.append({'case':name,'expected_ghep':gh,'actual_ghep':t.ghep(p),'expected_markers':markers,'actual_markers':[(d['trang_thai'],d.get('ly_do')) for d in g['dau_duong']]})
 old(ok,msg)
t.bang=bang;rc,o=t.chay_ca('c48_nguyen_van_va_mien');Path('.review/c48-rows5.json').write_text(json.dumps({'rc':rc,'output':o,'count':len(rows),'rows':rows},ensure_ascii=False,indent=2));print(rc,len(rows),o)
