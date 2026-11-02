verdict: dang_review
reviewed_sha: eb5e5bf119358babf831d2aec0ee27c7e5896c1f

Đang đối chiếu đặc tả, bằng chứng và chạy lại các phép kiểm tra độc lập. Chưa có kết luận cuối cùng.

## BẢNG ĐO

| Khẳng định | PR khai / SPEC đòi | Đo được | Khớp? |
|---|---|---|---|
| SPEC đóng băng | `22729e93eec0e1c4677a5d6529b81f9f0c46c47f3f605017b7abb337b5e1e270` | `sha256sum SPEC.md` khớp đủ 64 ký tự | Có |
| Exact head | `eb5e5bf119358babf831d2aec0ee27c7e5896c1f` | `git -C cay-kho rev-parse HEAD` khớp; `status --porcelain=v1` rỗng; `core.abbrev=7` | Có |
| N1 adr-song | rc 0 | rc 0; `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1` | Có |
| N1 doctrine-scan | rc 0 | rc 0; `đã quét 10 tệp, 0 chỗ chép doctrine` | Có |
| N1 whitespace | rc 0 | `git diff --check 3e973a0 HEAD`: rc 0, output rỗng | Có |
| N3 không còn tuyên bố ADR-0056 chưa kích hoạt | Không có hit về ADR-0056 | Lệnh `rg` được yêu cầu: rc 1, output rỗng | Có |
| N2 doc-claims-check | Delta HEAD/base = 0 | Cả hai rc 0, `ok=true`, `flags=[]`, 381 advisory; toàn bộ JSON base/head bằng nhau | Có |
| N2 selftest | N/N trên exact head | Executor cung cấp `1731/1731`; lượt độc lập đang chạy | Chờ |
| N5 CI của PR trên head cuối | Check run xanh | Không có hiện vật check run; review offline, không mạng | Không đo được |

Tất cả lệnh Python chạy với `PYTHONDONTWRITEBYTECODE=1`. Base được dựng bằng `git clone --local --no-hardlinks` vào thư mục `mktemp -d`, không dùng `git worktree`. Các phép N1/N2/N3 trên không tính vào sáu hướng săn.

## BẢNG SĂN

### HƯỚNG 1: Nguồn của trích dẫn và ngày xác nhận controller

- Giả thuyết: ADR trích sai câu trả lời hoặc gán ngày 26-10-2026 không có trong comment được cấp.
- Lệnh đã chạy:

```python
from pathlib import Path
import re, html
adr=Path('cay-kho/docs/adr/0056-lease-no-progress-six-hours.md').read_text()
comment=html.unescape(Path('ISSUE835-comment-6407154789.txt').read_text())
quote=re.search(r'— \*"(Không có, phiên điều\s+phối làm tay)"\*', adr).group(1)
quote=' '.join(quote.split())
print('quote =',repr(quote))
print('exact quote in supplied comment =',quote in comment)
print('comment date =',comment.splitlines()[2])
print('reference =',comment.splitlines()[0])
print('controller explanation =', next(s for s in comment.splitlines() if 'Không có automation' in s))
```

Chạy bằng `python - <<'PY' … PY` từ cwd. Chỉ nối khoảng trắng xuống dòng trong câu ADR và giải mã HTML ở bản đọc comment.

```text
quote = 'Không có, phiên điều phối làm tay'
exact quote in supplied comment = True
comment date = 2026-10-26T02:52:53Z
reference = https://github.com/ducthangho/tra-luat/issues/835#issuecomment-6407154789
controller explanation = 1. **"Controller ngoài (dispatcher)" mà mục *Hiệu lực* của ADR-0056 nhắc tới là gì?** → *"Không có, phiên điều phối làm tay"*. Không có automation nào ngoài kho áp ngưỡng 30 phút. Việc thu hồi lease do các phiên điều phối đọc protocol rồi làm tay. Kết hợp với phép đo của chính ADR (không controller nào **trong kho** mang hằng 30 phút), điều kiện "controller đã đồng bộ" quy về việc các phiên điều phối áp 360 phút cho lease mới.
```

- Kết luận: **KHÔNG PHẢI LỖI**. Câu trích và ngày khớp hiện vật. Không khẳng định đo byte hội thoại gốc hoặc thực trạng bên ngoài kho từ một bản đọc API.

### HƯỚNG 2: Lease của packet kích hoạt có bị hưởng 360 phút hồi tố không

- Giả thuyết: câu mới nói lease wp943 vẫn khai 30 trái với lease thật, hoặc packet áp 360 cho chính lease cấp trước merge.
- Lệnh đã chạy bằng `python - <<'PY' … PY` từ cwd:

```python
from pathlib import Path
import re
lease=Path('LEASE.yaml').read_text()
for field in ['lease_id','base_sha','leased_at_utc','heartbeat_required_minutes','heartbeat_minutes']:
    print(re.search(r'^'+field+r':.*$',lease,re.M).group(0))
adr=Path('cay-kho/docs/adr/0056-lease-no-progress-six-hours.md').read_text()
print('ADR states own lease stays 30 =',bool(re.search(r'lease `wp943-r1-g1-claude`[\s\S]*?vẫn khai 30\.',adr)))
print('lease identifies preactivation rule =','lease cap TRUOC moc kich hoat ADR-0056' in lease)
```

```text
lease_id: wp943-r1-g1-claude
base_sha: 3e973a03b151e37cd402e0a723816eeaa8247193
leased_at_utc: '2026-10-26T12:53:00Z'
heartbeat_required_minutes: 30
heartbeat_minutes: 30
ADR states own lease stays 30 = True
lease identifies preactivation rule = True
```

- Kết luận: **KHÔNG PHẢI LỖI**. ADR dòng 43–45 áp 360 cho lease cấp sau merge, giữ 30 cho lease wp943. `heartbeat_minutes` cũng là 30; không nhầm trường nhịp heartbeat với mốc thu hồi.

### HƯỚNG 3: Các bất biến và phép đo lịch sử của ADR có bị thay lén không

- Giả thuyết: sửa trạng thái làm đổi các luật giữ nguyên, số 360 cũ, hoặc ghi đè kết quả đo 19-10/25-10.
- Lệnh đã chạy bằng `python - <<'PY' … PY` từ cwd:

```python
import subprocess, hashlib
p='docs/adr/0056-lease-no-progress-six-hours.md'
b=subprocess.check_output(['git','show','3e973a0:'+p],cwd='cay-kho')
h=subprocess.check_output(['git','show','HEAD:'+p],cwd='cay-kho')
for title in ['Những gì KHÔNG đổi','Không hồi tố','Vì sao sáu giờ']:
    marker=('## '+title+'\n').encode()
    section=lambda x: x.split(marker,1)[1].split(b'\n## ',1)[0]
    x,y=section(b),section(h)
    print(title+': unchanged='+str(x==y)+'; sha256='+hashlib.sha256(y).hexdigest())
start='Đo 19-10-2026'.encode(); end='của từng lease.\n'.encode()
block=lambda x: x[x.index(start):x.index(end)+len(end)]
print('Historical 19-10/25-10 paragraph unchanged =',block(b)==block(h))
print('Historical bases = 062292b2c75be8c316a0cf7347290574efa10861; d2e3052d479d140b7e7b91df41ec4914fab7d544')
```

```text
Những gì KHÔNG đổi: unchanged=True; sha256=86816fefa68f8b2303e2fb53160f8b76dcbf8ab82e280e086e9d1438a92c7262
Không hồi tố: unchanged=True; sha256=7535563630c2979cef13b0b2900d0fec2d51c23b341cdfed2f5687de68385471
Vì sao sáu giờ: unchanged=True; sha256=efb368a9e8aad7bc0b3601d94448bc5e24d29517b62397fad400f536df42141b
Historical 19-10/25-10 paragraph unchanged = True
Historical bases = 062292b2c75be8c316a0cf7347290574efa10861; d2e3052d479d140b7e7b91df41ec4914fab7d544
```

- Kết luận: **KHÔNG PHẢI LỖI**. Ba mục bảo toàn byte; đoạn đo lịch sử cũng bảo toàn byte. Đã đọc lại các bất biến: hạn tuyệt đối, generation/bia mộ/exact head, review SLA +2 giờ và heartbeat 15 phút sau `changes_requested` giữ nguyên.

### HƯỚNG 4: Base đã chứa #834 và cửa accept có bị tác động không

- Giả thuyết: executor bắt đầu trước dependency #834 hoặc thay §4 làm mất điều kiện `accept`.
- Lệnh đã chạy bằng `python - <<'PY' … PY` từ cwd:

```python
import subprocess,hashlib
p='docs/PROTOCOL_DA_PHIEN.md'
read=lambda rev: subprocess.check_output(['git','show',rev+':'+p],cwd='cay-kho')
b,h=read('3e973a0'),read('HEAD')
section=lambda x: x.split(b'## 4.',1)[1].split(b'\n## 5.',1)[0]
print('Protocol section 4 byte-identical =',section(b)==section(h))
print('Section 4 SHA256 =',hashlib.sha256(section(h)).hexdigest())
for i,line in enumerate(h.decode().splitlines(),1):
    if 'accept' in line and 190<=i<=309: print(str(i)+':'+line)
print('Base commit =',subprocess.check_output(['git','show','-s','--format=%H %s','3e973a0'],cwd='cay-kho',text=True).strip())
print('Base is head ancestor =',subprocess.run(['git','merge-base','--is-ancestor','3e973a0','HEAD'],cwd='cay-kho').returncode==0)
```

Output thật, cắt gọn:

```text
Protocol section 4 byte-identical = True
Section 4 SHA256 = 614918d7425823f281d1a251ad59b3d4980a6e14d6cfbb110bb542906c71bb8f
242:`approved_pending` giữa `reviewing` và `accepted`: `approve` có biên nhận ghi sổ rồi vào `approved_pending`; chỉ
243:cửa `accept` (packet #834) đưa sang `accepted`, và chỉ khi packet áp `ADR-0054`, đo được đủ: đầu nhánh lease trên remote
246:một điều kiện thì state giữ nguyên. Packet chưa áp giữ đường `reviewing → accepted`.
Base commit = 3e973a03b151e37cd402e0a723816eeaa8247193 Merge pull request #950 from ducthangho/agent/wp834-g1-claude
Base is head ancestor = True
```

- Kết luận: **KHÔNG PHẢI LỖI**. Dependency có trong base và toàn §4, gồm cửa `accept`, giữ nguyên byte. Không coi việc kích hoạt ADR-0056 là kích hoạt ADR-0054.

### HƯỚNG 5: Mốc kích hoạt có bị biến thành ngày xác nhận hoặc SHA bịa không

- Giả thuyết: văn bản dùng ngày chỉ thị 26-10 thay cho thời điểm merge, hoặc ghi sẵn SHA/giờ chưa xảy ra, khiến lease ở giữa hai mốc bị áp sai.
- Lệnh đã chạy bằng `python - <<'PY' … PY` từ cwd:

```python
import subprocess,re
p=subprocess.check_output(['git','diff','--unified=0','3e973a0','HEAD'],cwd='cay-kho',text=True)
added='\n'.join(x[1:] for x in p.splitlines() if x.startswith('+') and not x.startswith('+++'))
print('Invented 40-hex activation SHA in added text =',re.findall(r'\b[0-9a-f]{40}\b',added))
print('Clock times in added text =',re.findall(r'\b\d{2}:\d{2}(?::\d{2})?(?:Z)?\b',added))
for x in added.splitlines():
    if 'merge' in x or 'Mốc 26-' in x: print(x)
```

Output thật, cắt gọn:

```text
Invented 40-hex activation SHA in added text = []
Clock times in added text = []
  **ĐÃ KÍCH HOẠT VẬN HÀNH** — mốc kích hoạt là merge của PR thi công `wp943` vào `master` (Issue #943).
Mốc 26-10-2026: chủ kho xác nhận **không có controller ngoài** (dispatcher) — *"Không có, phiên điều
chỉ lease cấp SAU mốc kích hoạt (merge của PR thi công `wp943`) khai `heartbeat_required_minutes: 360`;
```

- Kết luận: **KHÔNG PHẢI LỖI**. Đã đọc toàn bộ các dòng thêm, không chỉ dựa vào regex SHA: cả trạng thái ADR, luật áp dụng và dòng §20 đều neo merge wp943; 26-10 là ngày xác nhận không controller ngoài. Chữ “đã kích hoạt” trong nội dung sẽ merge tuân đúng SPEC, không phải bằng chứng packet đã merge tại lúc review.

### HƯỚNG 6: Các câu ngoài hunk còn đúng sau kích hoạt không

- Giả thuyết: đoạn mới đúng riêng lẻ nhưng mâu thuẫn mục *Không hồi tố*, mẫu lease §4, đồng hồ dự phòng, dòng ADR-0017 hoặc trạng thái ADR-0054.
- Lệnh đã chạy từ `cay-kho/`:

```sh
nl -ba docs/adr/0056-lease-no-progress-six-hours.md | sed -n '11,51p'
nl -ba docs/PROTOCOL_DA_PHIEN.md | sed -n '269,297p'
sed -n '1497p;1533,1535p' docs/PROTOCOL_DA_PHIEN.md
```

Output thật, cắt gọn:

```text
28  Ngưỡng mới chỉ áp cho lease **mới cấp sau khi kích hoạt**, và lease ấy khai
29  `heartbeat_required_minutes: 360`. Lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ
30  `heartbeat_required_minutes` đã đóng dấu. Muốn một packet đang chạy hưởng 360 phút thì phải có lease
31  kế nhiệm được cấp quyền riêng sau khi ADR này kích hoạt; không sửa lease cũ tại chỗ.
271 heartbeat_required_minutes: 360   # lease MỚI cấp sau khi ADR-0056 kích hoạt; lease đã cấp giữ số đã đóng dấu
282 Sau 6 giờ (360 phút) không có tiến triển, dispatcher thu hồi lease, tăng generation rồi mới reroute
283 (`ADR-0056`; ngưỡng cũ 30 phút của `ADR-0017`). Ngưỡng này chỉ áp cho lease MỚI cấp sau khi `ADR-0056`
284 kích hoạt vận hành; lease đã cấp — kể cả WP748 g19 — giữ nguyên byte và giữ `heartbeat_required_minutes`
293 hoặc cơ sở giờ mơ hồ thì KHÔNG treo lease; đồng hồ thu-hồi-6-giờ (360 phút, cùng ngưỡng không tiến triển
| `ADR-0017` | GitHub PR là bàn giao chính; canonical độc quyền phát hành | Accepted — câu ngưỡng thu hồi *"30 phút không có tiến triển"* **đã bị thay** bởi `ADR-0056` (2026-10-19) cho lease mới; phần còn lại vẫn hiệu lực | có nhắc: rải khắp — chưa tách được cổng riêng |
| `ADR-0054` | Đẩy nhánh code packet khi đủ điều kiện merge, review offline neo SHA cục bộ, dừng vá khi hết P0/P1/P2 ở mọi class, review tìm theo lớp; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted — chưa kích hoạt, chờ packet máy `MAY-ADR-0054` | **0 cổng** — không bộ đếm số lần đẩy |
```

- Kết luận: **KHÔNG PHẢI LỖI** sau khi đọc cùng các mệnh đề giới hạn phạm vi. §4 dòng 271 và 282–286 vẫn đúng; 293–294 nói “cùng ngưỡng … ở trên”, không tạo ngưỡng mới cho lease cũ. Mục *Không hồi tố* thống nhất với luật mới và ví dụ wp943. Dòng ADR-0017 ghi ngày quyết định ADR-0056 (19-10), không khai đó là giờ kích hoạt; phạm vi “lease mới” được định nghĩa bởi §4/ADR là sau merge. ADR-0054 vẫn chưa kích hoạt, độc lập với ADR-0056. Đoạn ADR 47–51 vẫn là lịch sử thi hành wp835 r3/r4 gắn #835 và các base phía trên, không phải lời khai rằng wp943 r1 có revision 4. Không phát hiện câu ngoài hunk trở thành sai do kích hoạt.

### HƯỚNG 7: Gói diff có giấu thay đổi ngoài phạm vi hoặc vượt trần không

- Giả thuyết: `diff.patch`/`numstat.txt` không phản ánh head thật; có code, lease hay dòng §20 khác bị đổi ngoài write set; vượt 2 tệp/80 dòng thêm.
- Lệnh đã chạy bằng `python - <<'PY' … PY` từ cwd:

```python
from pathlib import Path
import subprocess,hashlib
cmd=lambda *x:subprocess.check_output(['git',*x],cwd='cay-kho')
diff=cmd('diff','3e973a0','HEAD'); stat=cmd('diff','--numstat','3e973a0','HEAD')
print(stat.decode(),end='')
rows=[x.split('\t') for x in stat.decode().splitlines()]
allowed={'docs/PROTOCOL_DA_PHIEN.md','docs/adr/0056-lease-no-progress-six-hours.md'}
print('files =',len(rows),'added =',sum(int(x[0]) for x in rows),'deleted =',sum(int(x[1]) for x in rows))
print('Only two allowed docs =',{x[2] for x in rows}==allowed)
print('diff.patch byte-identical to Git diff =',diff==Path('diff.patch').read_bytes())
print('numstat.txt byte-identical to Git numstat =',stat==Path('numstat.txt').read_bytes())
print('Diff SHA256 =',hashlib.sha256(diff).hexdigest())
print('Hunks:')
for x in diff.decode().splitlines():
    if x.startswith('@@') or x.startswith('diff --git'):print(x)
```

```text
1	1	docs/PROTOCOL_DA_PHIEN.md
11	4	docs/adr/0056-lease-no-progress-six-hours.md
files = 2 added = 12 deleted = 5
Only two allowed docs = True
diff.patch byte-identical to Git diff = True
numstat.txt byte-identical to Git numstat = True
Diff SHA256 = 9846bf43fbdb16ed3b8962b5ab0ae6b34dad0e53411716e337fbe8e91bc72b50
Hunks:
diff --git a/docs/PROTOCOL_DA_PHIEN.md b/docs/PROTOCOL_DA_PHIEN.md
@@ -1532,7 +1532,7 @@ Lệnh tái lập cột ấy nằm trong `ops/HOAN_THIEN_KE_HOACH_20260822.md`
diff --git a/docs/adr/0056-lease-no-progress-six-hours.md b/docs/adr/0056-lease-no-progress-six-hours.md
@@ -3,8 +3,10 @@
@@ -34,8 +36,13 @@ kế nhiệm được cấp quyền riêng sau khi ADR này kích hoạt; không
```

- Kết luận: **KHÔNG PHẢI LỖI**. 2 tệp, +12/−5, dưới trần +80. Ba hunk đúng Trạng thái ADR, Hiệu lực ADR và đúng một dòng ADR-0056 trong §20. Không sửa code, lease, ADR khác, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json` hay các dòng §20 còn lại.
