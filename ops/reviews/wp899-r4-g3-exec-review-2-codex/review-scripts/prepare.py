from pathlib import Path
import json, subprocess,sys
R=Path('.review').resolve()
for n in (1,2):
 d=R/f'old{n}'; d.mkdir(exist_ok=True)
 for name in ('review_cases.py','probes.py','r4_compare.py','composite_case.py','boundary_case.py','new_probes.py'):
  p=Path(f'.review-input/r3-luot{n}/review-scripts')/name
  if p.exists():
   s=p.read_text().replace('root=R.parent','root=Path.cwd()').replace('root = R.parent','root = Path.cwd()')
   (d/name).write_text(s)
(R/'emit.py').write_bytes(Path('.review-input/r3-luot2/review-scripts/emit.py').read_bytes())
for name in ('audit_mutants.py','preflight.py','classifier_negative.py'):
 s=Path('.review-input/r3-luot2/review-scripts',name).read_text()
 if name=='preflight.py': s=s.replace('dc657149941f9db3ab2afc6fb6462ba4827bf18f','ba222ffd1615f0d74b59985b9612f725211b62f5')
 (R/name).write_text(s)
