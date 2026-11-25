import pathlib,json,subprocess,hashlib,collections,re,sys
W=pathlib.Path(__file__).resolve().parent;R=W.parent/'repo'
a={}
for rev in ('f602325','HEAD'):
 d=W/'ruff'/rev;d.mkdir(parents=True,exist_ok=True)
 for name in ('packet_loop.py','packet_loop_test.py'):
  (d/name).write_bytes(subprocess.check_output(['git','show',rev+':.claude/dev/'+name],cwd=R))
 p=subprocess.run([sys.executable,'-m','ruff','check','--no-cache','--select','F','--output-format','json',str(d)],capture_output=True)
 (W/('ruff_'+rev+'.json')).write_bytes(p.stdout)
 a[rev]={'rc':p.returncode,'diagnostics':collections.Counter(x['code'] for x in json.loads(p.stdout))}
a['symlinks_ops_land']=[x.decode() for x in subprocess.check_output(['git','ls-tree','-r','HEAD','--','ops/land'],cwd=R).splitlines() if x.startswith(b'120000')]
a['spec_blob_hash']=hashlib.sha256(subprocess.check_output(['git','show','f602325:ops/specs/wp1236-r12.md'],cwd=R)).hexdigest()
a['handoff_hash']=hashlib.sha256((W.parent/'bang_chung/handoff.yaml').read_bytes()).hexdigest()
D=W.parent/'bang_chung/luat9/D'
rows=[json.loads(s) for s in (D/'kq.jsonl').read_text().splitlines()]
a['luat9_neo']=rows[0];a['luat9_row_example']=rows[1]
(W/'audit.json').write_text(json.dumps(a,ensure_ascii=False,indent=2));print(json.dumps(a,ensure_ascii=False,indent=2)[:6500])
