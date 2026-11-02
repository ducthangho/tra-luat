from pathlib import Path
from collections import Counter
import subprocess,json,re,yaml
S=Path(__file__).resolve().parent; R=S/'cay-kho'; E=S/'evidence'; P='ops/reviews/README.md'; B='fb74c6eca742205acc0af9bb7ea89da94f15aa21'
def git(*a):return subprocess.check_output(['git',*a],cwd=R)
def raw(ref):return git('show',ref+':'+P)
def rows(ref):return Counter(x for x in raw(ref).decode().splitlines() if x.startswith('| '))
b=rows(B); h=rows('HEAD'); added=list((h-b).elements()); removed=list((b-h).elements()); errors=[]
if removed or len(added)!=4: errors.append('base row conservation')
d=yaml.safe_load((R/'ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml').read_text()); stem=Path(d['verdict_path']).name
new=[x for x in h.elements() if stem in x]; caveat=[]
for c in d['verdict_usage_caveats']:
 expected=f"| `{stem}` | `{c['id']}` | {c['mo_ta']} |"; ok=expected in added; caveat.append({'id':c['id'],'exact_row_match':ok})
 if not ok:errors.append('caveat '+c['id'])
index=[x for x in added if '.receipt.yaml' in x]; tokens=[stem,'pr1075-review-1-codex-verdict.receipt.yaml','**`approve`**','cross_approved','PR **#1075**','luot **1**','0/0/0/0','71490d5a','gpt-6-astra','53d670c','907c474','13376','pr1075-review-1-codex/']
if len(index)!=1 or not all(t in index[0] for t in tokens): errors.append('index row')
stripped=b''.join(x for x in raw('HEAD').splitlines(keepends=True) if stem.encode() not in x); equal=stripped==raw(B)
if not equal:errors.append('README not byte-equal after removing new rows')
merges=[]
for c in ['e137f8c','3a3aac5']:
 parents=git('show','-s','--format=%P',c).decode().split(); cr=rows(c); pr=[rows(p) for p in parents]; missing=[list((p-cr).elements()) for p in pr]; merges.append({'commit':c,'parents':parents,'parent_rows':[sum(p.values()) for p in pr],'merge_rows':sum(cr.values()),'missing_from_parents':missing})
 if any(missing): errors.append('merge lost rows '+c)
 # Artifact directory + receipt + flat verdict must be untouched from first parent.
 paths=['ops/reviews/pr1075-review-1-codex','ops/reviews/pr1075-review-1-codex-verdict.md','ops/reviews/pr1075-review-1-codex-verdict.receipt.yaml']
 delta=git('diff',parents[0],c,'--',*paths); merges[-1]['PR_artifact_delta_bytes']=len(delta)
 if delta:errors.append('merge modified PR artifacts '+c)
r={'base_rows':sum(b.values()),'head_rows':sum(h.values()),'removed':removed,'added_count':len(added),'added':added,'new_rows_count':len(new),'caveats':caveat,'without_new_rows_equal_base_bytes':equal,'merges':merges,'errors':errors}
(E/'readme.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(r,ensure_ascii=False,indent=2)); assert not errors
