from pathlib import Path
import hashlib, re, subprocess, yaml

root=Path(__file__).resolve().parent.parent/'cay-kho'
readme=(root/'ops/reviews/README.md').read_text()
added=[l[1:] for l in subprocess.check_output(['git','-C',str(root),'diff','6db9341','1aae17b','--','ops/reviews/README.md'],text=True).splitlines() if l.startswith('+|')]
print('ADDED_ROWS',len(added),'UNIQUE_ROWS',len(set(added)))
for n in (1,2):
    name=f'pr1050-review-{n}-codex-verdict.md'
    r=yaml.safe_load((root/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text())
    runid=r['model_reviewer_identity']['session_run_id'][:8]
    toc=[l for l in readme.splitlines() if l.startswith('| [`'+name+'`]')]
    cb=[l for l in readme.splitlines() if l.startswith('| `'+name+'` |')]
    assert len(toc)==1
    checks={
      'verdict':r['verdict'] in toc[0], 'assurance':r['assurance'] in toc[0],
      'counts':'/'.join(str(r[f'so_p{i}']) for i in range(4)) in toc[0],
      'run_id':runid in toc[0], 'head':r['reviewed_sha'][:7] in toc[0],
      'bytes':str(len((root/r['verdict_path']).read_bytes())) in toc[0],
      'model':r['model_reviewer_identity']['model_da_chay'] in toc[0],
      'receipt_link':Path(r['verdict_path']).stem+'.receipt.yaml' in toc[0],
    }
    print('ROUND',n,'TOC_ROWS',len(toc),'CAVEAT_ROWS',len(cb),'CHECKS',checks)
    for c in r['verdict_usage_caveats']:
        rows=[l for l in cb if f'| `{c["id"]}` |' in l]
        print('CAVEAT',c['id'],'rows',len(rows),'text_equal',len(rows)==1 and rows[0].split('|')[3].strip()==c['mo_ta'])
    print('ALL_LINKS_EXIST',all((root/'ops/reviews'/link).exists() for row in toc for link in re.findall(r'\]\(([^)]+)\)',row)))
