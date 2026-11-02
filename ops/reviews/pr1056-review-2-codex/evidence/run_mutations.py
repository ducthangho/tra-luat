from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parent))
from run_gates import run
b=Path(__file__).resolve().parent.parent;c=b/'review-copy';summary={}
flat=c/'ops/reviews/pr1050-review-1-codex-verdict.md';readme=c/'ops/reviews/README.md';receipt=c/'ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml'
original={p:p.read_bytes() for p in (flat,readme,receipt)}
cases=[('mutant-byte',flat,original[flat][:-1]+b' '),('mutant-readme',readme,b''.join(l for l in original[readme].splitlines(keepends=True) if not l.startswith(b'| [`pr1050-review-1-codex-verdict.md`]'))),('mutant-count',receipt,original[receipt].replace(b'\nso_p1: 1\n',b'\nso_p1: 9\n'))]
for label,p,mutated in cases:
 try:
  p.write_bytes(mutated)
  print('MUTATION',label,'path',p.relative_to(c),'before_bytes',len(original[p]),'after_bytes',len(mutated),'different_positions',sum(x!=y for x,y in zip(original[p],mutated)),flush=True)
  summary[label]=run(c,label)
 finally:p.write_bytes(original[p])
(b/'evidence/mutations-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
