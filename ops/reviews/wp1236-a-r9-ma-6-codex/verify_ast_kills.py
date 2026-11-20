import pathlib,json,subprocess,os,sys,concurrent.futures as cf
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo';src={m['k']:m for m in map(json.loads,(w/'executor_regenerated.jsonl').read_text().splitlines())}; prior=[json.loads(l) for l in (w.parent/'quet/kq_moi.jsonl').read_text().splitlines()]; rows=[(x['k'],x['giet'][0]) for x in prior if x['giet']]+[(339,'a217_cli_tham_so_va_ma_thoat')]
d=w/'ast_native_modules';d.mkdir(exist_ok=True)
def run(item):
 k,c=item;p=d/(str(k)+'.py');p.write_text(src[k]['src']);cmd=[sys.executable,'-B',str(r/'ops/gate_output_doi_chieu_test.py'),'--mot-ca',c]
 z=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,TMPDIR=str(w/'tmp'),GATE_OUTPUT_DOI_CHIEU_MA=str(p),PYTHONDONTWRITEBYTECODE='1'),timeout=600)
 return dict(k=k,target=c,rc=z.returncode,stdout=z.stdout,stderr=z.stderr,killed=z.returncode==3 and 'DO:'+c+':' in z.stdout)
with (w/'ast_native_kills.jsonl').open('w') as f,cf.ThreadPoolExecutor(4) as ex:
 for i,x in enumerate(ex.map(run,rows)):
  f.write(json.dumps(x,ensure_ascii=False)+'\n');f.flush()
  if (i+1)%50==0:print(i+1,flush=True)
print('DONE',len(rows),flush=True)
