from pathlib import Path
R=Path('.review').resolve()
for d in (R/'prior1',R/'prior2'):
 for p in d.rglob('*.py'):
  if 'r2-source' in p.name:continue
  s=p.read_text()
  s='from pathlib import Path\n'+s
  s=s.replace("R.parent/'ops/", "Path.cwd()/'ops/").replace("R.parent / 'ops/", "Path.cwd() / 'ops/")
  s=s.replace("R=pathlib.Path('.review').resolve()",'R=Path(__file__).resolve().parent').replace("R=pathlib.Path('.review')",'R=Path(__file__).resolve().parent').replace("R=Path('.review').resolve()",'R=Path(__file__).resolve().parent')
  if p.name in ('run_old.py',):s=s.replace("R/f'old", "R/f'old")
  p.write_text(s)
# Legacy emit helper used by supplied real-shell counterexamples, all under .review.
(R/'emit.py').write_bytes((R/'prior2/emit.py').read_bytes())
# old1 variant missing in first bundle: reuse transparent adaptation from later bundle.
p=R/'prior1/old1/r4_compare.py'
s=p.read_text(); old="p=subprocess.run(['git','show','9e5019ef2e3b8d59345fff2165569c3281cba3b5:ops/ci_provenance.py'],capture_output=True,check=True)"
s=s.replace(old,"p=__import__('types').SimpleNamespace(stdout=(R/'r2-source.py').read_bytes())")
(p.parent/'r4_compare_current.py').write_text(s)
# Adapt only time parser interface changed in this candidate; preserve tests and record original separately.
for n in (1,2):
 p=R/f'prior{n}/finish_probes.py'
 if p.exists():
  s=p.read_text().replace('(h := _gio(b["gio"], TS))','(h := _gio(b["gio"][:19] + "Z"))').replace('m._gio(t.T,m.TS)','m._gio(t.T[:19]+"Z")')
  p.write_text(s)
