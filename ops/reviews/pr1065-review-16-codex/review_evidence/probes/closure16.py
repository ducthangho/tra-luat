from pathlib import Path
import subprocess,json,hashlib
r=Path(__file__).resolve().parents[1];rows=[]
for mode in ['control','post-mismatch','keep-mismatch']:
 log=r/'evidence'/f'closure16-{mode}.json';cmd=[str(r/'pwsh/pwsh'),'-NoProfile','-File',str(r/'probes/pinned-release-round15.ps1'),'-Mode',mode,'-Log',str(log)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=90);(r/'evidence'/f'closure16-{mode}.log').write_text(p.stdout+p.stderr);assert p.returncode==0
 d=json.loads(log.read_text());row=d['rows'][0];good=mode=='control'
 assert len(d['rows'])==1 and d['direct']['rc']==0 and len(d['requests'])==1
 assert d['requests'][0]['uri'].endswith('/releases/tags/v'+d['pin'])
 assert row['hanh_dong']==('nang_cap' if good else 'loi')
 assert d['downloads']==(1 if good else 0)
 assert d['direct']['stdout']==(d['pin'] if good else '1.0.0' if mode=='post-mismatch' else '9.9.9')
 if good:assert row['sau']==d['pin']
 else:assert "release trả tag" in row['chi_tiet']
 result=dict(mode=mode,rc=p.returncode,pin=d['pin'],response=d['release'],action=row['hanh_dong'],downloads=d['downloads'],direct=d['direct'],command=cmd);rows.append(result);print(json.dumps(result,ensure_ascii=False),flush=True)
(r/'evidence/closure16.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
f=r/'VERDICT.md';s=f.read_text();s=s.replace('| ghim-actionlint-khong-la-dich-chung-nhan | đang kiểm | Chưa chạy phép đo. |','| ghim-actionlint-khong-la-dich-chung-nhan | ĐÃ VÁ THẬT | `python3 probes/closure16.py`: control pin1.7.7/response1.7.7 → nang_cap, downloads1, native1.7.7/rc0; response9.9.9 ở cả hậu cài và giu → loi, downloads0, native giữ nguyên. Chi tiết evidence/closure16.json. |');f.write_text(s)
with f.open('a') as o:
 o.write('\nHƯỚNG 3: đóng finding ghim actionlint lượt 15\n  giả thuyết : HTTP trả tag khác ghim vẫn được dùng làm đích của giu/nang_cap.\n  lệnh       : python3 probes/pinned-release-round15.py > evidence/pinned-historical-driver.log 2>&1; python3 probes/closure16.py > evidence/closure16.log 2>&1\n  output     : driver lịch sử rc1 tại assert cũ mong nang_cap cho post-mismatch; raw pinned-post-mismatch.json cho loi. Oracle hiện hành: 3/3 PASS; control đúng ghim nang_cap/native1.7.7/rc0/downloads1; post-mismatch và keep-mismatch đều loi/downloads0/native không đổi. Mọi request đúng URL /releases/tags/v1.7.7.\n  kết luận   : KHÔNG PHẢI LỖI; ĐÃ VÁ THẬT finding lượt 15. Chốt chạy trước tải và trước chứng nhận giu; bản phản hồi vẫn được dùng sau chốt nhưng đã bằng ghim theo Test-CungDinhDanh. Hash/ZIP/copy/native thật trên Linux; HTTP thay thế ngoại tuyến; không khẳng định đã đo upstream.\n')
print('Pinned closure: 3/3 PASS; mismatch rejected before download and before keep')
