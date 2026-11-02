import concurrent.futures,json,pathlib,subprocess,sys,time
root=pathlib.Path(__file__).resolve().parents[1]
cases=['a4_qua_han_giet_ca_nhom','a9_loi_gui_tin_hieu_khong_bao_da_dung','a11_subreaper_va_esrch','b10_version_treo_giet_ca_nhom']
jobs=[(v,c) for v in ('head','parent_only','no_kill','a9_default') for c in cases]
def run(job):
 r=subprocess.run(['python3',str(root/'probes/case_worker.py'),*job],capture_output=True,text=True,timeout=180)
 assert r.returncode==0,(job,r.stdout,r.stderr)
 row=json.loads(r.stdout)
 print(json.dumps(row,ensure_ascii=False),flush=True)
 return row
t=time.monotonic()
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: rows=list(pool.map(run,jobs))
(root/'evidence/mutation-matrix.json').write_text(json.dumps(dict(seconds=round(time.monotonic()-t,6),rows=rows),ensure_ascii=False,indent=2)+'\n')
