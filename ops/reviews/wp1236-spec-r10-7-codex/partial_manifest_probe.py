import json
from generate_review import *
a=[json.loads(x) for x in (W/'m1.jsonl').read_text().splitlines()]
p={x['id']:x for x in map(json.loads,Q.with_name('pilot_c2d606b_kq.jsonl').read_text().splitlines()) if 'id' in x}
mid=next(x['id'] for x in a if p[x['id']]['giet']==['a201_loi_khai'])
rows=[m if m['id']==mid else {k:v for k,v in m.items() if k!='src'} for m in a]
(W/'partially_reconstructed_manifest.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows))
n,r,out=run('partially_reconstructed',['chay',W/'partially_reconstructed_manifest.jsonl',M/'ops/gate_output_doi_chieu_test.py','--goc',G,'--ra',W/'partially_reconstructed_kq.jsonl','--song-song','1'])
(W/'partial_manifest_probe.json').write_text(json.dumps({'input_rows':len(rows),'rows_with_source':1,'retained_id':mid,'receipt':r,'stdout':out},ensure_ascii=False,indent=2));print(r,out)
