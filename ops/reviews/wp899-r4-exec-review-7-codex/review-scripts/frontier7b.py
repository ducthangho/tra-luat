from pathlib import Path
import runpy,sys,os,json,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent;g=runpy.run_path(str(R/'frontier7.py'));src=g['src'];out=R/'frontier7b';out.mkdir(exist_ok=True)
M=[('job_suffix_no_dot_pure','r"(?: \\(.*\\))?"','r"(?: \\([^.\\n]*\\))?"'),('name_run_crlf_first_line','v.split("\\n")[0]','v.split("\\n")[0].rstrip("\\r")')]
rs=[]
for n,a,b in M:
 assert src.count(a)==1;p=out/(n+'.py');p.write_text(src.replace(a,b));cmd,q,cs=g['cases'](p);ks=[c for c,rc,o in cs if rc==3 and o.startswith('DO:'+c+':')];bad=[(c,rc,o) for c,rc,o in cs if rc and not(rc==3 and o.startswith('DO:'+c+':'))]
 z={'name':n,'old':a,'new':b,'source':str(p),'command':cmd,'rc':q.returncode,'cases':cs,'killed':ks,'other_errors':bad,'rank':'GIET+NEM' if ks and bad else 'GIET' if ks else 'TIN_DUNG_GIA' if bad else 'SONG_SOT'};rs.append(z);(out/'results.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2));print(n,z['rank'],flush=True)
