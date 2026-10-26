from pathlib import Path
import os,json,sys,subprocess
R=Path(__file__).resolve().parent;src=(R.parent/'ops/ci_provenance.py').read_text();out=R/'prior2/extra-r4';rows=[]
for name,old,new,case in [
('gio_thieu_header_lay_rest','(h := _gio(b["gio"]))','(h := _gio(b["gio"]) or a)','c38_ghep_lech_gio'),
('gio_bo_can_duoi','a <= h <= z','h <= z','c38_ghep_lech_gio'),
('gio_bo_can_tren','a <= h <= z','a <= h','c38_ghep_lech_gio'),
('b_bo_ten','if any(not _chuoi(s.get("name")) or','if False and any(not _chuoi(s.get("name")) or','c37_ghep_lech_ten'),
('env_bo_PATH','re.search("GITHUB_(ENV|PATH)",','re.search("GITHUB_ENV",','c42_github_env_cung_job')]:
 assert src.count(old)==1
 p=out/(name+'.py');p.write_text(src.replace(old,new));r=subprocess.run([sys.executable,'-B',str(R.parent/'ops/ci_provenance_test.py'),'--mot-ca',case],capture_output=True,env=dict(os.environ,CI_PROVENANCE_MA=str(p),PYTHONDONTWRITEBYTECODE='1'))
 row={'name':name,'old':old,'new':new,'case':case,'rc':r.returncode,'output':(r.stdout+r.stderr).decode()};rows.append(row)
 assert r.returncode==3 and row['output'].startswith('DO:'+case+':'),row
 print(name,'GIET',case,flush=True)
(R/'legacy-reanchored.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
