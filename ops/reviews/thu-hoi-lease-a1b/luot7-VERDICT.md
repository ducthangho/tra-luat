<!-- Verdict codex lượt 7 (gpt-6-astra, reasoning effort xhigh — xác nhận ở header log runtime), codex_cli tại chỗ, trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 15 @ f5a6b1d (spec sha256 73f8a2f2…), base 5c79fa2. Chép nguyên văn từ tệp -o; chỉ bỏ khoảng trắng cuối dòng. Commit lưu tệp này KHÔNG đổi tệp spec. -->
**0 P1 / 0 P2 / 0 P3. Finding lượt 6 đã vá thật trong đặc tả.** Không phát hiện lỗi mới do bản vá.

Review: `advisory_review`, `openai_codex / codex_cli / machine`. Không sửa checkout, không commit. Model/effort chưa được xác minh bằng header runtime.

```text
reviewed_sha:  f5a6b1d222179f9a00d4a6331037e059d25353d8
reviewed_tree: ad1a3e3833ae668a05316e2291c89fcbeebe74d5
base:          5c79fa2c94b328ae3bbbef52a4cfa820fc40bc4a
spec_sha256:   73f8a2f2626f547b7d62b3a93873d9334922b9017d3deaacd2a2d7640ab39fab
```

**Đối chiếu lượt 6:** tại [§7](/tmp/claude-0/-home-user-tra-luat/6d0cd47b-1999-55e6-9ff7-5c7b553ad293/scratchpad/rv/ops/specs/THU-HOI-LEASE-A1b.md:170), lớp “tiền đề chưa có producer/đường nối” nay ghi đúng **3 lượt / 5 finding**, dẫn checkpoint Q19. Các hàng “cơ học” đã có slug nguyên nhân; bộ đếm liên quan đã cập nhật.

Phép đo phân lớp, **rc=0**:

```bash
python3 -B - <<'PY'
import re, collections
from pathlib import Path
s = Path('ops/specs/THU-HOI-LEASE-A1b.md').read_text()
part = s.split('**Phân lớp từng finding')[1].split('## 8.')[0]
findings = collections.defaultdict(list)
rounds = collections.defaultdict(set)
for row in part.splitlines():
    if not re.match(r'\| [LC]\d+ ', row):
        continue
    ids, slug = row.split('|')[1:3]
    slug = slug.strip().split(' (')[0]
    rnd = None
    for item in ids.split(','):
        m = re.fullmatch(
            r'\s*(?:([LC]\d+) )?(F\d+|P[23](?:-[ab\d]+)?)\s*', item)
        rnd = m[1] or rnd
        findings[rnd+' '+m[2]].append(slug)
        rounds[slug].add(rnd)
expected = (
    {f'L7 F{i}' for i in range(1,14)}
    | {f'L8 P2-{i}' for i in range(1,5)}
    | {f'L8 P3-{i}' for i in range(5,9)}
    | {'C5 P2-a','C5 P2-b','C6 P2'})
print('missing:', sorted(expected-findings.keys()))
print('extra:', sorted(findings.keys()-expected))
print('multiple:', {k:v for k,v in findings.items() if len(v)!=1})
print('classified:', len(findings))
PY
```

```text
missing: []
extra: []
multiple: {}
classified: 24
```

Các đối chiếu còn lại:

| Phạm vi | Kết quả |
|---|---|
| Q1–Q18 | **18/18 khớp byte** với các commit nguồn; `git log -S` khớp mốc sinh ô. |
| Q19–Q21 | Q19/Q20 khớp [quyết định mở lại và nâng trần](https://github.com/ducthangho/tra-luat/pull/657#issuecomment-5853920122). Q21 chưa có neo bền, đúng lời khai của spec. |
| Băm/dòng dẫn | Băm lịch sử bản nháp, r9, A1a r2/r3, hai script Q6 và JSON ghim đều khớp. Các dòng code/workflow/protocol được dẫn đã đối chiếu tại đúng mốc. |
| M1–M6 | **6/6** chiếu vào **3** đường §3. Workflow, consumer và seam còn thiếu thuộc packet tiền đề; không phát hiện mục tiêu buộc A1b ghi ngoài write set. |
| A1–A8 | Không phát hiện thêm oracle bất khả thi hoặc chỗ thoả rỗng ngoài nợ đã khai. A5 tách đầu vào production khỏi cặp kết quả của bộ phân loại; A6 phủ đủ năm đường với hợp đồng riêng. |
| Vai/thẩm quyền | Hiện vật executor nằm trong biên nhận thuộc write set; output reviewer ở ngoài nhánh packet; phép đo trước lease thuộc chủ kho/điều phối. |
| §8.8–11 | Lời khai về break-glass, map ref, ranh giới chủ kho/agent và effort phù hợp bằng chứng; không báo lại thành finding. |

Phép đo số hạng A0, mỗi lệnh **rc=0**:

```bash
git diff --numstat 0721811^1 0721811
git rev-list --first-parent --count 0721811..67802bf
git rev-list --first-parent --count 0721811..f5bef3a
```

```text
141     0   .github/workflows/ops-thu-hoi-admission.yml
919     0   ops/lease_publish.py
1327    1   ops/lease_publish_test.py
76
77
```

Đúng **141 + 919 + 1327 = 2387 dòng thêm / 3 tệp**.

Phép dẫn xuất Q6:

```bash
python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py \
  . 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
```

**rc=0**, stderr rỗng; trích kết quả:

```text
mien_lease=89
lease_hop_le=89
cap_hai_chieu=11
vi_pham=[]
BIA_MO_LICH_SU_theo_b=[]
digest=8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48
stdout_sha256=1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61
byte_equal_frozen_json=True
```

Qua REST connector, tái lập được **100 run trước 01:50Z = 89 success + 11 failure**; ruleset vẫn thiếu `thu-hoi`, strict=false, cho merge/squash/rebase và bypass rỗng. Băm thân ba comment khớp lần lượt `5d52ad0b…`, `b76b3052…`, `9a799b34…`. Descriptor có **1379 byte**, băm `f974b6db…`, không newline cuối.

**Giới hạn phép đo:** hai lệnh tự kiểm/ma trận Q6 đã chạy nhưng **failed, rc=1** do kho fixture gọi dịch vụ ký commit bị sandbox chặn; không tính là pass. Log ghim có đúng `35/35`, `27 DUNG`, `0 SAI`, một `DUNG LECH`, nhưng đó chỉ là đối chiếu hiện vật. Annotation Ubuntu và lịch sử **441/441 ref** chưa tái lập độc lập. CI/canary/implementation: **not_run**.

`git diff --check`, diff tracked và diff index đều **rc=0**; HEAD/tree giữ nguyên, chỉ có `.codex/` ignored. Approval này dành cho **bản nháp đặc tả**, chưa xác nhận đủ tiền đề đóng băng hoặc kích hoạt.

VERDICT: APPROVE
