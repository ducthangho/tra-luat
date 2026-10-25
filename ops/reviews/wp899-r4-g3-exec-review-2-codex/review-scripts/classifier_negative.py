import sys,runpy,json,contextlib,io
from pathlib import Path
R=Path(__file__).resolve().parent
m=runpy.run_path(str(R.parent/'ops/ci_provenance_test.py'))
g=m['main'].__globals__; g['DOT_BIEN']=(m['TU_KIEM'][0][:4],); g['TU_KIEM']=()
with contextlib.redirect_stdout(io.StringIO()) as b: rc=m['main']([])
v={'rc':rc,'stdout':b.getvalue()}; (R/'classifier-negative.json').write_text(json.dumps(v,indent=2)+'\n'); print(v)
