from pathlib import Path
import shutil
w=Path(__file__).resolve().parent;h=w.parent/'lich_su'
for n in ['excess_probe.py','guard_witnesses.py','b02_targeted.py','distinct_target.py','trace_v2.py','count_audit.py']:
 shutil.copyfile(h/'luot2'/n,w/n)
s=(h/'luot2/probes.py').read_text();start=s.index('for m in json.loads(');end=s.index("(w/'probes-complete.json')",start)
s=s[:start]+s[end:]
(w/'probes.py').write_text(s)
shutil.copyfile(w.parent/'bang_chung/cong-cu/bang_toan_tu.py',w/'bang_toan_tu.py')
print('Historical clause probes retained; B02 and R1-02 direct witnesses run separately without redundant full mutant suites.')
