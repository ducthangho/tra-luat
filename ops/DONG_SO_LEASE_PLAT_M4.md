# ĐÓNG SỔ — lease của `PLAT-M4` (#194 / PR "#204")

**Loại:** append-only. **KHÔNG lease nào bị sửa.** Lý do ở §3.

**Quyết định của người giữ kho, 21-08-2026:** *"Đóng sổ lease #204."*

## 1. Sự việc — đo được

| phép đo | giá trị |
|---|---|
| PR "#204" | `merged: true` · `merged_at 2026-08-21T08:30:01Z` · `merged_by ducthangho` |
| head đã land | `a9e021de28d03e7edc9077b42678f6af22a3b684` |
| commit merge trên `master` | `a7a45119` |
| diff | 2 tệp · +543/−25 — **đúng** write set |
| assurance đạt được | `human_audited` (`ops/reviews/plat-m4-human-audit-ducthangho-verdict.receipt.yaml`) |

Packet `PLAT-M4` đã `landed`. Việc của nó không còn.

## 2. Hệ quả — write set được giải phóng

Lease `plat-m4-exec-2-claude-20260821` khai `write_set`:

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

và `lease_expires_at_utc: '2026-08-22T02:05:00Z'` — **chưa tới hạn** khi tệp này được ghi.
Nhưng lease là quyền GHI cho một packet ĐANG chạy; packet đã land thì quyền ấy đã **tiêu**,
không phải "còn hiệu lực tới 02:05Z". Kể từ tệp này, hai đường dẫn trên **rảnh** cho packet
kế tiếp — không phải đợi đồng hồ.

Cùng lý lẽ cho các lease reviewer của `PLAT-M4` (`-review-1` … `-review-3r4`): lượt review đã
kết thúc bằng verdict và biên nhận, nên chúng cũng đã tiêu.

## 3. Từ vựng KHÔNG có sự kiện "đóng lease" — nói thẳng thay vì bịa ra một cái

Đo trên toàn bộ `ops/leases/*.yaml`: chỉ có hai giá trị `event` —
`executor_lease_granted` (8) và `review_lease_granted` (36). **Không có** `*_released`,
`*_closed`, `*_expired`. `ops/lease_publish.py` cũng **không đọc** trường `event` (grep `event`
trong tệp ấy: RỖNG), nên thêm một giá trị mới sẽ đi qua cổng mà **không phép đo nào** kiểm nó —
một từ vựng không ai cưỡng chế là một từ vựng sẽ trôi.

Vì vậy tệp này là **biên bản**, không phải một sự kiện mới trong schema. Nó đi cùng hình dạng
với `ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md`: append-only, neo bằng số đo, không sửa hồ sơ cũ.

**Nợ để lại (chưa đo được từ phiên này):** hết hạn theo đồng hồ là cơ chế DUY NHẤT hiện có để
một lease thôi hiệu lực. Packet land SỚM hơn hạn — trường hợp thường gặp, không phải ngoại lệ —
thì khoảng giữa "đã land" và "hết hạn" là một quyền ghi còn sống mà không việc nào cần tới. Chốt
đúng phải nằm ở cổng: `lease_publish.py` từ chối cấp lease mới giao write set với một lease chưa
hết hạn, và nhận biết lease đã tiêu qua trạng thái packet. Chưa có; ghi vào đây để lần cấp lease
sau không phải phát hiện lại.
