from pathlib import Path
import subprocess,json,concurrent.futures
r=Path(__file__).resolve().parents[1]
names=['target-equality-oracle','zip-target-oracle','install-contract-oracle','real-pip-oracle','real-nlm-oracle','absence-oracle','run-user-extra']
def run(name):
 cmd=['python3','-u',str(r/'probes'/(name+'.py'))];p=subprocess.run(cmd,capture_output=True,text=True,timeout=240,cwd=r)
 out=p.stdout+p.stderr;(r/'evidence'/(name+'-round12.log')).write_text(out)
 summary=out.splitlines()[-1] if out.splitlines() else ''
 print(name,p.returncode,summary,flush=True);return dict(name=name,command=cmd,rc=p.returncode,summary=summary)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:rows=list(pool.map(run,names))
(r/'evidence/contracts-round12.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:
 f.write('\nHƯỚNG 9: hợp đồng cài, đích và native venv/NLM\n  giả thuyết : rc0 nhưng không cài, thiếu ghim, launcher cũ hoặc cao hơn đích vẫn được ĐẠT.\n  lệnh       : `python3 -u probes/run-contracts-round12.py` (gọi các driver riêng liệt kê trong evidence/contracts-round12.json).\n  output     : '+'; '.join(f"{x['name']}: rc{x['rc']}, {x['summary']}" for x in rows)+'\n  kết luận   : '+('KHÔNG PHẢI LỖI trong bộ oracle này.' if all(x['rc']==0 for x in rows) else 'KHÔNG ĐO ĐƯỢC đầy đủ: phải xem log và assert độc lập.')+' Pip thật chạy với PIP_NO_INDEX=1 trên wheel local tự tạo; HTTP/npm là fixture. Không chứng nhận gói upstream/Windows.\n')
assert all(x['rc']==0 for x in rows), rows
