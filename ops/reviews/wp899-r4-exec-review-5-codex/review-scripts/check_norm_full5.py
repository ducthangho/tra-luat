from pathlib import Path
import os,sys,json,subprocess
R=Path(__file__).resolve().parent;root=R.parent
code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
p=subprocess.run([sys.executable,'-B','-c',code],capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(R/'norm_equivalent.py')))
a=json.loads(p.stdout);z={'name':'n_goi_strip_run','command':[sys.executable,'-B','-c',code],'rc':p.returncode,'cases':a,'rank':'SONG_SOT' if len(a)==48 and all(rc==0 for c,rc,o in a) else 'KHAC'}
(R/'norm-full5.json').write_text(json.dumps(z,ensure_ascii=False,indent=2));print(z['rank'],len(a),[(c,rc) for c,rc,o in a if rc])
