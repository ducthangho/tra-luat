from pathlib import Path
import shutil,subprocess,sys,os,json,hashlib
R=Path('.review').resolve(); root=R.parent
for f in ('bootstrap.py','adapt_prior.py','replay_prior_all.py','remaining_prior.py','close_prior.py','repair_legacy_anchors.py','frontier.py','frontier2.py','frontier_cases.py','prove_frontier.py','prove_last.py','remaining_survivors.py','mode_probe.py','snapshot.py','run.py','audit_mutants.py'):
 shutil.copy2(root/'.review-input/r4-luot3'/f,R/f)
# Bootstrap is read-only to the candidate and populates only this scratch.
subprocess.run([sys.executable,'-B',str(R/'bootstrap.py')],check=True)
subprocess.run([sys.executable,'-B',str(R/'adapt_prior.py')],check=True)
for d in [R,R/'prior1',R/'prior2']:
 for p in d.glob('*.py'):
  if p.name in ('setup_current.py','bootstrap.py'): continue
  s=p.read_text().replace('45/45','47/47').replace('44/45','46/47').replace('125/125','155/155')
  # Header is now canonicalized in tach_buoc; re-anchor old probes transparently.
  s=s.replace('_gio(b["gio"][:19] + "Z")','_gio(b["gio"])').replace('_gio(buoc[0]["gio"][:19] + "Z")','_gio(buoc[0]["gio"])')
  p.write_text(s)
subprocess.run([sys.executable,'-B',str(R/'snapshot.py'),'start'],check=True)
# Raw full/delta bytes for this round, without changing Git config.
for args,name in [(['diff','ba222ffd1615f0d74b59985b9612f725211b62f5','HEAD'],'full.patch'),(['diff','HEAD^','HEAD'],'delta.patch')]:
 p=subprocess.run(['git',*args],capture_output=True,check=True);(R/name).write_bytes(p.stdout)
print('SETUP DAT')
