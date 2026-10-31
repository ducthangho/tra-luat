from pathlib import Path
import yaml,json,subprocess,re
b=Path(__file__).resolve().parent.parent;r=b/'cay-kho'
text=(r/'ops/reviews/README.md').read_text();rows=[l for l in text.splitlines() if l.startswith('|') and 'pr1050-review-' in l]
print('NEW_ROWS',len(rows),'UNIQUE',len(set(rows)))
for n in (1,2):
 name=f'pr1050-review-{n}-codex-verdict.md';rec=yaml.safe_load((r/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text());run=json.loads((r/rec['model_reviewer_identity']['run_json']).read_text());toc=[l for l in rows if l.startswith('| [`'+name+'`]')];warnings=[l for l in rows if l.startswith('| `'+name+'`')]
 print('ROUND',n,'TOC_COUNT',len(toc),'CAVEATS_COUNT',len(warnings))
 t=toc[0];counts='/'.join(str(rec[f'so_p{i}']) for i in range(4))
 print('TOC_MATCH', {k:needle in t for k,needle in [('verdict',rec['verdict']),('assurance',rec['assurance']),('counts',counts),('run_id',run['short_id']),('model',rec['model_reviewer_identity']['model']),('head',rec['reviewed_sha'][:7]),('bytes',str(rec['verdict_bytes'])),('round',f'luot **{n}**'),('target','**#1050**')]})
 for c in rec['verdict_usage_caveats']:print('CAVEAT',c['id'],'EXACT_COUNT',sum(c['id'] in l and c['mo_ta'] in l for l in warnings))
 links=re.findall(r'\]\(([^)]+)\)',t);print('LINKS',[(link,(r/'ops/reviews'/link).exists()) for link in links]);print('ROW',t)
 for l in warnings:print('WARNING_ROW',l)
 if n==2:print('HEAD_AT_MERGE_MATCH',subprocess.check_output(['git','-C',str(r),'rev-parse',rec['land_merge_commit']+'^2'],text=True).strip()==rec['reviewed_sha'])
