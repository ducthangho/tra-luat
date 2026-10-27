from review_probe import hunt, row

cmd = r"""git log -1 --format='%H %cI %s' --until='2026-08-14T23:59:59+07:00' b38fce83 -- .github/workflows/ci.yml
git show a323974:.github/workflows/ci.yml | nl -ba | sed -n '10,19p;33,52p'
git log --first-parent --format='%h %cI %s' --since='2026-08-14T00:00:00+07:00' --until='2026-08-14T19:00:00+07:00' b38fce83
git show 05170b4:CLAUDE.md | nl -ba | sed -n '138,156p'
python3 - <<'PROBE'
import json
from pathlib import Path
from collections import Counter
count=Counter(); samples=[]
for p in Path('ops').rglob('*.json'):
 try: d=json.loads(p.read_text())
 except (OSError,ValueError): continue
 objs=d if isinstance(d,list) else [d]
 for x in objs:
  if not isinstance(x,dict): continue
  if any(str(x.get(k,'')).startswith('2026-08-14') for k in ('created_at','started_at','run_started_at','updated_at')) and ('jobs' in x or 'event' in x or 'workflow_id' in x):
   samples.append(str(p))
print('ops JSON run-like snapshots for 2026-08-14:',sorted(set(samples)))
PROBE
"""
hunt(11, 'Snapshot 14-08 và lời khai sáu lần đo đầu',
     'Chú thích mới hồi tố sai: ma trận ngày 14-08 đã bỏ vế master, hoặc có thể khẳng định đủ sáu lần đầu từ Git.', [cmd],
     'KHÔNG PHẢI LỖI về lịch sử ma trận — commit thay workflow gần nhất trước cuối 14-08 là a323974 (13-08), còn vế github.ref master. SÁU merge trước 19:00 +07 ngày 14-08 đo được (#98,#100,#101,#102,#104,#105); lời sáu lần đầu đã có tại 05170b4. KHÔNG ĐO ĐƯỢC lịch sử label/dispatch và job Windows thực sự của sáu lượt ấy: không có readback run ngày 14-08 tìm thấy dưới ops, Git không lưu event API. Không dùng lời cũ làm bằng chứng dương cho sự vắng mặt run Windows trước merge; cũng không tự coi là sai khi chưa có dữ liệu.')
row('14-08-2026 ma trận còn master', 'khi ấy có vế master', 'HƯỚNG 11: log --until + git show a323974:.github/workflows/ci.yml L44–50', 'Có')
row('Đợt 14-08 sáu merge / không nhãn, không dispatch / lần Windows đầu', 'sáu lần đo đầu; nay cùng điều kiện không lần nào', 'HƯỚNG 11: 6 merge #98,#100,#101,#102,#104,#105 trong cửa sổ trước 19:00; thiếu run/labels/dispatch readback; hiện tại output os chỉ Ubuntu', 'Số merge trong cửa sổ đo được; “đầu tiên” và không dispatch lịch sử KHÔNG ĐO ĐƯỢC')

cmd = r"""nl -ba CLAUDE.md | sed -n '158,186p;800,811p;945,950p'
nl -ba docs/PROTOCOL_DA_PHIEN.md | sed -n '880,892p;970,983p;1516,1522p'
nl -ba docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md | sed -n '1,5p;15,35p'
python3 - <<'PROBE'
from pathlib import Path
import yaml
ci=yaml.load(Path('.github/workflows/ci.yml').read_text(),Loader=yaml.BaseLoader)
for s in ci['jobs']['gate']['steps']:
 if 'release-verify strict (lane' in s.get('name',''):
  print(s['name'],'if=',s.get('if'),'first run=',s['run'].splitlines()[0])
PROBE
"""
hunt(12, 'Mâu thuẫn trong CLAUDE / protocol / ADR-0049',
     'Câu mới về OS đánh đồng toàn bộ gate PR/master, trái lane LAND; hoặc tuyệt đối hóa không Windows trái gate tại chỗ.', [cmd],
     'KHÔNG PHẢI LỖI khi phân biệt đúng phạm vi: tiêu đề ghi ma trận OS, không khẳng định mọi bước PR/master giống nhau; LAND/WORKER vẫn khác và khớp §deploy 5. API CHỈ CÓ TRÊN MỘT NỀN là bài học lịch sử lane launcher, tự động PR cần nhãn, không chứng minh dispatch không tồn tại. ADR-0049 khớp việc bỏ master và giữ launcher; protocol T3 + ADR yêu cầu gate Windows tại chỗ/trước phát hành, không phải một cò GitHub khác. Vì thế không được mở rộng “KHÔNG BAO GIỜ” thành mọi loại gate/mọi thời điểm: nên ghi rõ gate ci.yml tự động tại snapshot đang xét. Đây cùng hướng thu hẹp phạm vi với câu Windows trên master, không phải phát hiện thêm một workflow Windows ẩn.')
row('Tiêu đề matrix không phân biệt PR/master vs deploy §5', 'chỉ sửa mô tả OS', 'HƯỚNG 12: LAND if ref master / WORKER if ref != master; OS dùng cùng output', 'Không mâu thuẫn: cùng chính sách chọn OS không đồng nghĩa cùng bộ bước')
row('API CHỈ CÓ TRÊN MỘT NỀN (L800–811)', 'job Windows chỉ chạy khi PR nhãn windows', 'HƯỚNG 8, 12: launcher tự động PR cần nhãn + paths; dispatch và push là các event khác, bài học lịch sử', 'Không tạo phản ví dụ mới; không đọc câu cũ thành mô tả mọi event')
row('Protocol T3 / ADR-0049 / “KHÔNG BAO GIỜ”', 'gate mã PR thường không Windows sau merge', 'HƯỚNG 12: protocol L884 có Windows+Linux, ADR L19 có gate deploy tại chỗ; không phải trigger của ci.yml', 'Chỉ đúng trong phạm vi CI tự động hiện tại; cần giữ phạm vi đó khi diễn đạt')
