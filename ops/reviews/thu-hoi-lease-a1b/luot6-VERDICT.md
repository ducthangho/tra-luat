<!-- Verdict codex lượt 6 (gpt-6-astra, reasoning effort xhigh — xác nhận ở header log runtime), codex_cli tại chỗ, trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 14 @ 7af8e0a, base 5c79fa2. Chép nguyên văn từ tệp -o; chỉ bỏ khoảng trắng cuối dòng; đường dẫn tuyệt đối trong liên kết giữ nguyên. -->
Còn **1 P2; 0 P1/P3**. Review là `advisory_review`, `openai_codex / codex_cli / machine`; không sửa tệp, không commit. Model/effort chưa được xác minh bằng header runtime.

```text
reviewed_sha:  7af8e0a7d7b2a35dc8b1db964d574112d235ffc1
reviewed_tree: e2b09695e91cad03f7573c9fc7a9c1cadadfe5cd
base:          5c79fa2c94b328ae3bbbef52a4cfa820fc40bc4a
spec_sha256:   040f3cf045121b153c33db5ddf41819f794063a10d02d6edd8c10c76567fe2d5
```

**[P2] [ops/specs/THU-HOI-LEASE-A1b.md:170](/tmp/claude-0/-home-user-tra-luat/6d0cd47b-1999-55e6-9ff7-5c7b553ad293/scratchpad/rv/ops/specs/THU-HOI-LEASE-A1b.md:170) — Bảng phân lớp mới chưa được phản ánh vào bộ đếm kế thừa; một lớp đã xuất hiện ở ba lượt vẫn ghi một lượt.**

Đây là phần **vá hờ của Claude lượt 8 P2-2**. Dòng 170 ghi lớp “đặc tả hứa thứ tiền đề chưa có producer/đường nối” có **1 lượt / 2 finding**. Nhưng chính bảng mới gán thêm **L7 F3, L7 F7 và L8 P2-1** vào lớp ấy: tổng **3 lượt / 5 finding**. Sai số che ngưỡng checkpoint tại protocol `:1054–1055`; đây không chỉ là nit.

Hai hàng `:180` và `:186` còn gom finding vào “cơ học”, thậm chí khai “không slug nội dung”, trong khi protocol `:748–753` yêu cầu mỗi finding có slug nguyên nhân và mọi tách/gộp lớp có đối chiếu.

Bằng chứng đã chạy:

```bash
python3 -B - <<'PY'
import re
from pathlib import Path
s = Path('ops/specs/THU-HOI-LEASE-A1b.md').read_text().splitlines()
k = 'đặc tả hứa thứ tiền đề chưa có producer/đường nối'
rows = [(i,l) for i,l in enumerate(s,1) if k in l]
for i,l in rows:
    print(i,l)
rounds = {'Codex '+x for x in re.findall(r'A1b lượt (\d+)',rows[0][1])}
rounds.update('Claude '+x for _,l in rows[1:]
              for x in re.findall(r'L(\d+)\s',l))
print('rounds =',sorted(rounds))
print('actual =',len(rounds))
PY
```

Output, **rc=0**:

```text
170 | **"đặc tả hứa thứ tiền đề chưa có producer/đường nối"** (mới) | **1** lượt (2 finding) | A1b lượt 1 F1 (bước đo profile), F2 (wiring production) |
181 | L7 F3 | đặc tả hứa thứ tiền đề chưa có producer/đường nối (break-glass) |
185 | L7 F7, L8 P2-1 | đặc tả hứa thứ tiền đề chưa có producer/đường nối (binding/verifier r9 Q13) |
rounds = ['Claude 7', 'Claude 8', 'Codex 1']
actual = 3
```

**Câu sửa đề xuất:** “Lớp này có **3 lượt / 5 finding**: Codex lượt 1 F1–F2, Claude lượt 7 F3/F7, Claude lượt 8 P2-1; ghi nhận đã chạm ngưỡng checkpoint và dẫn quyết định áp dụng.” Đồng thời gán slug nguyên nhân cho các hàng “cơ học”, rồi tính lại bộ đếm từ các cặp **(lượt, slug)**.

Phép kiểm khóa: đối chiếu đủ finding của từng verdict, mỗi finding đúng một slug; số lượt bằng số lượt phân biệt, không bằng số finding. Nếu muốn tách break-glass và binding thành lớp riêng, phải ghi bảng nối và lý do tách theo protocol, không âm thầm reset lịch sử.

Đối chiếu từng finding của hai lượt trước:

| Finding | Kết quả trên nháp 14 |
|---|---|
| Codex 5 P2-a — `11→0` | **Đã vá thật trong đặc tả:** A5 tách đầu vào production theo hợp đồng khỏi cặp kết quả tiêm tại bộ phân loại. |
| Codex 5 P2-b — thiếu consumer | **Đã vá thật:** T6/A6 đủ năm đường, thêm Q14-diễn giải và mutant riêng cho `body`/`kiem-github`. |
| Claude 8 P2-1 — T7 tự tham chiếu | **Đã vá thật:** tuple chuyển sang A1; T7 yêu cầu packet sở hữu verifier/entry point; M1 dùng T1–T7. |
| Claude 8 P2-2 — phân lớp/đếm lượt | **Vá hờ:** còn finding trên. |
| Claude 8 P2-3 — nới Q18 | **Đã vá thật:** diễn giải giới hạn ở bản nháp lúc hỏi và nêu rõ chỗ lệch “mốc giờ lệch”/“tập rỗng”. |
| Claude 8 P2-4 — thiếu checkpoint mới | **Đã vá thật:** Q19/Q20 và lời khai mở lại review khớp comment bền. |
| Claude 8 P3-5 — mốc T7/lời khai cũ | **Đã vá thật:** bổ sung mốc T7 sau `8bba697` và cập nhật các lời khai liên quan. |
| Claude 8 P3-6 — “Recommended” | **Đã vá thật:** dùng “Theo khuyến nghị”. |
| Claude 8 P3-7 — audit R8(b) | **Đã vá thật:** A5 yêu cầu xác nhận **0 delta R8(b)**. |
| Claude 8 P3-8 — cột/dẫn chiếu/Q6 | **Đã vá thật:** cột commit, hàng `chiếu-vào` và phân biệt r9 Q6 đã sửa. |

Các phép đo bổ sung:

- **Q1–Q18:** so byte với các commit nguồn, **18/18 khớp**. Các băm bản nháp, r9, A1a r2/r3 và hai script dẫn xuất khớp.
- Đọc lại [checkpoint](https://github.com/ducthangho/tra-luat/pull/657#issuecomment-5853593828) và [quyết định nâng trần](https://github.com/ducthangho/tra-luat/pull/657#issuecomment-5853920122): băm thân lần lượt `5d52ad0b…`, `b76b3052…`, khớp đặc tả. **Q21 chưa có neo bền**, đúng lời khai của spec.
- **M1–M6:** đều chiếu vào write set §3. Các phần cần sửa workflow, consumer hoặc seam được giao cho tiền đề; chưa được chứng nhận là đã triển khai.
- **A1–A8:** ngoài finding về sổ lịch sử trên, chưa phát hiện thêm oracle bất khả thi hoặc mâu thuẫn mới. Những giới hạn của A4/A5 và break-glass đã được khai tại §8.8–11; không báo lại chúng.

```bash
git diff --numstat 0721811^1 0721811
git rev-list --first-parent --count 0721811..67802bf
git rev-list --first-parent --count 0721811..f5bef3a
```

Output, mỗi lệnh **rc=0**:

```text
141     0   .github/workflows/ops-thu-hoi-admission.yml
919     0   ops/lease_publish.py
1327    1   ops/lease_publish_test.py
76
77
```

Từng số hạng đúng: **141 + 919 + 1327 = 2387 dòng thêm / 3 tệp**.

```bash
python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py \
  . 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
```

**rc=0**, stderr rỗng; bản in khớp byte JSON đã ghim:

```text
lease_hop_le=89
cap_hai_chieu=11
vi_pham=[]
BIA_MO_LICH_SU_theo_b=[]
digest=8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48
stdout_sha256=1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61
```

`git diff --check`, diff tracked và diff index đều **passed, rc=0**; HEAD/tree không đổi, cuối lượt chỉ thấy `.codex/` ignored. API PR vẫn trả đúng reviewed SHA. Môi trường: Linux, Python 3.11.15.

**Giới hạn:** hai suite tự kiểm/đột biến chỉ đối chiếu log đã ghim, **not_run** trong lượt này; CI/canary/implementation **not_run**. Không tái lập độc lập lịch sử 100/89 run, annotation Ubuntu và 441/441 ref. Không coi những phần ấy là passed.

VERDICT: REQUEST_CHANGES
