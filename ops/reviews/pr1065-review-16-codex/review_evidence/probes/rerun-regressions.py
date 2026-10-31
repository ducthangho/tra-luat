from pathlib import Path
import subprocess, concurrent.futures, json
r=Path(__file__).resolve().parents[1]
groups=[
 (4,'ChiKiem và prerequisite trên cả hai tầng',['third-paths-oracle','portable-check-oracle','system-check-oracle','absence-regression-oracle']),
 (5,'native/catch/continue và lưới nhật ký lượt 4–7',['l4-user-oracle','user-oracle','user-version-oracle','new-paths-oracle','run-main-tail']),
 (6,'băm, cài HeThong, hậu kiểm và reboot',['system-matrix','caller-matrix']),
 (7,'đăng ký lịch, ACL và reparse',['registration-head']),
]
def run(group):
 n,title,names=group; rows=[]
 for name in names:
  cmd=['python3','-u',str(r/'probes'/(name+'.py'))]
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=240,cwd=r)
  out=p.stdout+p.stderr; (r/'evidence'/(name+'-summary.log')).write_text(out)
  lines=out.splitlines(); summary=' | '.join(lines[-2:])
  if len(summary)>1400: summary=summary[:1400]
  rows.append(dict(name=name,command=cmd,rc=p.returncode,summary=summary))
  print(name, p.returncode, summary,flush=True)
 text=f'\nHƯỚNG {n}: {title}\n  giả thuyết : bản vá gây hồi quy ở đường đã đo các lượt 4–9.\n  lệnh       : '+'; '.join(f'`python3 -u probes/{x}.py`' for x in names)+' (qua `python3 probes/rerun-regressions.py`).\n  output     : '+'; '.join(f"{x['name']}: rc{x['rc']}, {x['summary']}" for x in rows)+'\n  kết luận   : '+('KHÔNG PHẢI LỖI trong tập oracle này.' if all(x['rc']==0 for x in rows) else 'KHÔNG ĐO ĐƯỢC đầy đủ; xem log lỗi và đo lại trước khi kết luận.')+' HTTP/task/icacls/installer là mô hình offline; native fixture/argv/rc và file thật trên Linux. Không suy thành native Windows đã đạt.\n'
 with (r/'evidence/legacy-verdict-discard.md').open('a') as f:f.write(text)
 return rows
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: results=list(pool.map(run,groups))
(r/'evidence/regressions-round12.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
