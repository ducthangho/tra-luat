import sys, json, importlib.util
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('boundary_test',root/'ops/ci_provenance_test.py')
t=importlib.util.module_from_spec(s); s.loader.exec_module(t)
x='python '+t.DUONG_GIA
base=t.buoc(x,'THU: 4/4 dat')
rows=[*base[:3],t.T+' ##[group]details',base[3],t.T+' \x1b[36;1mecho tail\x1b[0m',base[4]]
rc,stdout,prov,_=t.chay([(t.job(1),t.log_voi(rows))],wf=t.wf_tu(x+'\necho tail',x))
r={'rc':rc,'stdout':stdout,'gate':t.gate(prov),'rows':rows,'blocks':t.nap().tach_buoc(t.log_voi(rows).splitlines())}
(R/'boundary-case.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
case='F02_nested_incomplete_echo'
try:t.khong_marker(prov,'child endgroup cannot prove the unclosed parent echo complete, and late color must not be discarded')
except t.TinHieuChotCa as e:print('DO:'+case+':'+str(e));sys.exit(3)
print('DAT:'+case)
