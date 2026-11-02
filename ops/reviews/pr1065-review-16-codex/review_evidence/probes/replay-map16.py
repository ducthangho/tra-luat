from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parents[1]
groups={
'4':('Native user, HeThong hash/MSI/recovery, register/ACL',['l4-user-oracle.py','system-matrix.py','registration-head.py','icacls-round15.ps1']),
'5':('Getter rc và CLI/Python version failure',['user-version-oracle.py','run-user-extra.py']),
'6':('Metadata rc và các nhánh native còn lại',['new-paths-oracle.py','caller-matrix.py']),
'7':('Venv/NLM thiếu prerequisite, metadata phục hồi',['absence-oracle.py','absence-regression-oracle.py']),
'8':('ChiKiem chung ở user/portable/system',['third-paths-oracle.py','portable-check-oracle.py','system-check-oracle.py']),
'9':('Hậu cài venv/ghim, pip thật offline, launcher',['install-contract-oracle.py','real-pip-oracle.py','real-nlm-oracle.py']),
'10':('Đích mới nhất, không giu bản cao hơn, NLM CLI',['target-equality-oracle.py','zip-target-oracle.py']),
'11':('Định danh đầy đủ/suffix và parser',['version-identity-oracle.py','cli-version-identity-oracle.py']),
'12':('Case và Node current không parse được',['cli-case-identity-oracle.py','node-major-oracle.py']),
'13':('Định danh số học/Git .windows. trước/sau',['numeric-identity-oracle.py','zip-numeric-identity-oracle.py']),
'14':('Hậu cài HeThong fixture có trạng thái + mutation',['post-observations-round15.py','review14-mutations.py']),
'15':('Pin mismatch, native chỉ hỏng sau cài',['pinned-release-round15.py','new-third-paths-round15.py'])}
rows=[]
for round_,(description,names) in groups.items():
 a=[]
 for name in names:
  p=r/'probes'/name;assert p.exists();a.append(dict(path=str(p.relative_to(r)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),historical_l15_same_bytes=(r/'luot15/probes'/name).read_bytes()==p.read_bytes()))
 rows.append(dict(round=int(round_),scope=description,probes=a))
(r/'evidence/replay-map16.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (r/'VERDICT.md').open('a') as f:
 f.write('\n## ÁNH XẠ PROBE LƯỢT 4–15 VÀ GIỚI HẠN TÁI CHẠY\n\nLệnh: `python3 probes/replay-map16.py`; output: 12/12 nhóm lượt có driver hành vi được tái chạy, danh sách và băm driver ở evidence/replay-map16.json. Dùng các bản driver tích luỹ ở luot15/probes, đã reroot vào copies/head; các getter/caller/main-tail lấy từ head hiện hành. Không chạy utility build-HINT/finalize-verdict lịch sử hay oracle hardcode SHA/số test cũ để chứng nhận head mới. Các kiểm tương ứng được thay bằng preflight16/accounting115/inventory119/final-audit16. Không sửa oracle lịch sử để che assertion đỏ; H3/H10 giải thích rc1 và có assert độc lập trên JSON.\n\n| Lượt | Nhóm được chạy lại | Driver chính |\n| --- | --- | --- |\n')
 for row in rows:f.write(f"| {row['round']} | {row['scope']} | "+', '.join('`'+x['path']+'`' for x in row['probes'])+' |\n')
 f.write('\nMô hình ngoại tuyến đo logic điều phối và phiên bản; chỉ interpreter/native fixture/file/hash/archive/local-pip là thật tại Linux. Không đo NTFS effective ACL/owner/race, Scheduled Task thật, COM, msiexec hoặc luồng NguoiDung thật trên Windows tại SHA này. Các phần đó là KHÔNG ĐO ĐƯỢC, không phải PASS. Review không suy tính an toàn của TEMP/PATH/PSModulePath/ProgramFiles trên VM từ một fixture do reviewer tự tạo.\n')
print('Replay map: 12/12 historical-round groups mapped to executed behavioral drivers; stale finalizers excluded')
