---
verdict: approve
reviewed_sha: 7c21bf60f062d0076370fc8144e382962cd817ba
so_p1: 0
so_p2: 0
so_p3: 1
so_the_hien: 1
---

# Cross-review WP538 — LƯỢT 2, claude review antigravity

Lượt 1 (`changes_requested`, 0/1/1 trên `f2aa1f9f`) do cùng reviewer này chấm khi executor còn
là **codex**. r4/g4 đổi executor sang **antigravity** vì codex hết quota. Lượt này chấm bản vá
của agy.

## XUNG ĐỘT LỢI ÍCH — khai TRƯỚC

Reviewer là **phiên claude đang điều phối**, không phải tiến trình claude riêng
(`launcher.py doctor` ⇒ `rc=12`, `CHUA_XAC_THUC claude`). Phiên này soạn `spec r4` và ghi hộ
`lease g4` — trong đó có **khối khai ngân sách dòng** mà `PHÁT HIỆN 1` dưới đây nói tới. Tức
tôi đang chấm một con số do chính tôi viết. Khai ra để người đọc tự trừ hao.

Diff WP538 do **agy** viết. Reviewer là **claude**. Khác provider thật.

## PHẠM VI ĐO

`f2aa1f9f` (head lúc cấp g4) → `7c21bf60`. Hai commit:

- `da5e45e` — merge `origin/master` vào nhánh packet (đúng `A-r4-2`, **merge commit**, không
  rebase, không force-push)
- `7c21bf6` — bản vá idiom, **`+4 −1`**, đúng hai tệp `.claude/skills/`

`packet_loop_test.py +299` trong `git diff` là **của master**, không phải của agy: `git show
7c21bf60 --stat` chỉ liệt kê hai tệp SKILL.md.

## CHỐT CHÍNH — con số phải BẰNG nền

```
python3 .claude/dev/idiom_py_test.py   ⇒  rc=0 · nền: 7/7 đạt · BỎ QUA: 0 · 0 dòng ĐỎ
```

Đúng con số `origin/master` cho. Tiêu chí là **đạt nền**, không phải đỡ đỏ hơn — và nó đạt.

Nhắc lại phép đo của lượt 1 để thấy đã đi từ đâu: `f2aa1f9f` cho `5/7`, hai ca đỏ
(`ba_nen_path`, `hop_dong_khoi` 4 khối).

## CỔNG — `rc` đọc TRỰC TIẾP

| cổng | rc |
|---|---:|
| `doctrine-scan` | **0** |
| `adr-song` | **0** |
| `doc-claims-check --strict` | **0** |
| `git diff --check` | **0** |
| `release-verify --strict` | **0** (`ok=true`, `expected == checked == 180`) |
| `bien_nhan_v2` | **0** (TỔNG: ĐẠT) |
| `idiom_py_test` | **0** (7/7) |

`packet_loop_test` cho `rc=1`, 6 ca đỏ — **KHÔNG phải của bản vá**, xem `BẢNG SĂN H5`.

CI tự động trên `7c21bf60` (run `35090041011`), đo lúc viết: `thu-hoi` **success** ·
`gate (ubuntu)` **success** · `gate-packet-loop` **success** cả ubuntu lẫn windows ·
`gate (windows)` và `gate-registry` **còn chạy**. Lane windows chạy vì PR mang **nhãn
`windows`** — lượt tự động theo sự kiện, reviewer KHÔNG gọi tay.

## BẢNG SĂN — sáu hướng

| # | hướng | kết quả | phán |
|---|---|---|---|
| H1 | bốn dòng thêm có NGUYÊN VĂN chuỗi chuẩn không | trích `IDIOM` từ `idiom_py_test.py:55` rồi so từng dòng ⇒ **4/4 KHỚP** tuyệt đối | **SẠCH** |
| H2 | vị trí phép gán có ý nghĩa không, hay chốt chỉ đếm sự có mặt | **đột biến M-b**: chuyển một phép gán xuống SAU lần dùng đầu ⇒ `rc=1`, `work-packet/SKILL.md:62 GÁN_MUỘN`, `6/7` | **SẠCH** — chốt có răng, giết đúng ca và đúng lý do; agy đặt đúng cả bốn |
| H3 | phạm vi ghi | `git show 7c21bf60 --stat` ⇒ đúng 2 tệp, cả hai trong write_set g4 | **SẠCH** — không nở phạm vi, không đụng `idiom_py_test.py` |
| H4 | bản sao `.agents/skills/**` có khối hỏng cùng loại không | quét mọi khối mã có `"$PY"`: **0** `THIẾU_GÁN`, **0** `SAI_DẠNG` | **SẠCH** — không có lớp lỗi song sinh bị bỏ sót |
| H5 | `packet_loop_test` 6 ca đỏ — của ai | cùng **đúng 6 tên ấy** đỏ trên `origin/master`; `comm` hai chiều ⇒ **rỗng cả hai**. Mọi ca khai `ly_do_dung: workspace la git worktree`, `probe.workspace: DO`, `ma_thoat: 14` | **SẠCH** — tạo tác RIG của reviewer (sandbox là `git worktree`), đúng lớp `CLAUDE.md` đã ghi. CI thật xác nhận độc lập: `gate-packet-loop` **success** (CI chạy trong clone) |
| H6 | base drift `thu-hoi rc=12` đã hết chưa | `merge-base --is-ancestor origin/master HEAD` ⇒ **CÓ**; CI `thu-hoi` **success** | **SẠCH** |

Năm hướng SẠCH, và chúng được kê đầy đủ chứ không lược: một kết luận sạch có giá ngang một
phát hiện.

## PHÁT HIỆN

### 1. `khai-ngan-sach-dong-r4-neo-so-cu` — **P3**, 1 thể hiện

`spec r4` khai ngân sách dòng cho ADR-0044 bằng con số **`+772`** (bội số 2,6×), đo trên
`c66415aa..f2aa1f9f`. Trên head hiện tại `c66415aa..7c21bf60` đo lại: **7 tệp, +775 −64**.

Bản vá idiom thêm 4 dòng và bỏ 1, nên con số **đã trôi 3 dòng** so với lúc đóng băng spec.

**Vì sao chỉ P3.** Nội dung lời khai không đổi: vẫn vượt ngưỡng 300, vẫn trên điểm `PLAT-X4`
(+721), lý do "sáu adapter phải trỏ cùng nguồn protocol tại cùng thời điểm" vẫn đứng. Thứ lệch
là **một con số minh hoạ**, và nó lệch theo hướng vô hại.

**Vì sao vẫn ghi ra.** `CLAUDE.md` có đúng bài học này: *"MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG
MINH CÁC SỐ HẠNG CÒN ĐÚNG"* — ba lượt cross-review từng đọc qua một câu như vậy mà không ai
dừng lại, vì soi tính nhất quán nội tại thì nó sạch hoàn toàn. Một con số trong tài liệu không
ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.

**Đây là lỗi của spec r4, tức của chính phiên reviewer này, KHÔNG phải của agy.** agy làm đúng
việc được giao; con số cũ đi vì đặc tả đóng băng trước bản vá. Sửa thì phải qua revision mới
(`§3.2`), nên đây là việc của chủ kho, không phải việc agy phải làm lại.

## KHÔNG ĐO ĐƯỢC

- **`gate (windows)` và `gate-registry` của `7c21bf60`** — còn chạy lúc chấm. Verdict này neo
  vào phép đo TẠI CHỖ của reviewer cộng bốn check đã xong, không neo vào hai check ấy.
- **Hành vi thật trên nền chỉ có `python` hoặc chỉ có `py`.** `idiom_py_test` dựng nền giả cho
  ca `ba_nen_path` và ca ấy ĐẠT; nhưng đó là nền do bộ test dựng, không phải một máy Windows
  thật thiếu `python3`.
- **Danh tính runtime của agy.** Commit mang `Author: ducthangho`, không có header CLI nào
  chứng minh model/effort của agy. Lease g4 khai `model: KHONG_KHAI` nên không có lời khai nào
  bị mâu thuẫn — nhưng cũng không có gì để kiểm.

## KẾT LUẬN

**`approve`** — 0 P1 · 0 P2 · **1 P3** · 1 thể hiện.

Bản vá tối giản và đúng chỗ: `+4 −1`, bốn dòng khớp nguyên văn chuỗi chuẩn, đặt đúng vị trí mà
đột biến chứng minh là có ý nghĩa. Không đụng bộ đo. Không nở phạm vi. Bản sao `.agents/` không
mang lớp lỗi song sinh. Base drift đã giải bằng merge commit đúng cách. Chốt chính về **bằng
nền**, không phải đỡ đỏ hơn.

`P3` không chặn approve: `sensitive` đòi không P1/P2, và ở đây là 0/0. Nó là lỗi của đặc tả do
chính reviewer soạn, ghi ra để chủ kho quyết, không phải để giữ lại bản vá.

**Approve này chỉ phủ thứ tôi ĐO ĐƯỢC** — đọc mã, một đột biến có răng, bảy cổng tại chỗ, và
bốn check CI đã xong. Nó không phủ hai check còn chạy, và không thay nghĩa vụ land.
