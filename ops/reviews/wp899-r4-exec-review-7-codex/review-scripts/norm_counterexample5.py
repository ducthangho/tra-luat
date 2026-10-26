from pathlib import Path
import sys,importlib.util,json,os
R=Path(__file__).resolve().parent;root=R.parent
s=importlib.util.spec_from_file_location('t',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
label='n_goi_strip_run'
run=t.X+' \\ '  # trailing escaped space is not a bare script call; trim makes backslash terminal
try:
 p=t.g1(t.wf_tu(t.X,buoc_them={'run':run}),t.khoi([run],'THU: 4/4 dat'))
 g=t.gate(p);print('OBS:'+json.dumps(g,ensure_ascii=False))
 t.bang(t.ghep(p)=='passed' and g['kich_ban']['buoc_xac_thuc']==1 and g['dau_duong']==[],f'gh={t.ghep(p)}, markers={g["dau_duong"]}')
except t.TinHieuChotCa as e:print('DO:'+label+':'+str(e));sys.exit(3)
except Exception as e:print('HONG:'+label+':'+type(e).__name__+':'+str(e));sys.exit(4)
print('DAT:'+label)
