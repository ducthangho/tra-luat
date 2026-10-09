# Review MÃ lượt 5 — PR #689 / packet #677 (DOT-BIEN-L-BIEN-CONG-KHAI)

- reviewer: **Claude Opus 5.5** (general-purpose, thay cho agent `review-opus-max` chưa được nạp). Effort "max" là TỰ KHAI
  trong chỉ thị — KHÔNG đặt được, KHÔNG ĐO ĐƯỢC.
- nhãn assurance: **`advisory_review`** (reviewer cùng họ Claude với executor)
- reviewed_sha: `66ec303effa344e1e3a3ed60bf2920a2bd8e76fe` (đo: `git -C cay-kho rev-parse HEAD`); chuỗi e55c5e2 → 85124dc → 66ec303
- merge-base: `c16bec639efa0077def4916c25c3e0c17f68dcaa` (đo `git merge-base`); baseline A8 `89fc4fac8cea65979cc2483043dc8cd07a6e8518`
- spec r8 sha256 đo lại: `4dfbfd69e161d55aa28f2685741cdcf11fcd5171438081e9eb63815c69bb4094` — khớp PROMPT
- Môi trường: Linux, python3.11.15 (mặc định), python3.12.3 và 3.13.12 CÓ mặt, PyYAML 6.0.1 cả ba. Windows thật: KHÔNG ĐO ĐƯỢC.
- Bắt đầu đo 07:46Z 30-09 (`date -u`); lease g5 hết hạn `2026-09-30T10:48:00Z`.
- Worktree tạm `wt5.iEzj/{k,k12,m,...}` (detached @66ec303). Đột biến ghi ra tệp test RIÊNG (`ops/_m4_<tên>_test.py`),
  không ghi đè tệp gốc; mỗi (đột biến, ca) một tiến trình con, ghi lớp ngoại lệ + `isinstance(e, TinHieuChotCa)`.

Nhật ký tăng dần bên dưới.

## Đợt đo 1 — nghiệm thu tĩnh (A7, A8, A10) trên 66ec303

| mục | kết quả | phép đo |
|---|---|---|
| A7(1) | ĐẠT | `git diff --name-only c16bec6…(merge-base)...HEAD` ⇒ đúng `ops/lease_publish_test.py` |
| A7(2) | ĐẠT, **sát trần** | `git diff --numstat c16bec6...HEAD` ⇒ `576 4` ≤ 600. Lượt 5 (`85124dc..66ec303`) ⇒ `92 17`. **Còn 24 dòng** tới trần — mọi hint phải vừa trong đó. |
| A8 | ĐẠT | `a8.py` (cắt AST kèm decorator) `_chay_buoc_dang` + `t51`–`t68` ở `89fc4fa` vs HEAD ⇒ `so khoi 16 16 ten bang True`, `lech []`. Vế động `--chi-ca=t5/t6`: trong toàn suite (đợt 2). |
| A10 | ĐẠT | ruff 0.15.8 `--select F --no-cache` trên `git show <rev>:ops/lease_publish_test.py`: c16bec6 = 89fc4fa = 85124dc = 66ec303 = **9 lỗi** (7×F401, 2×F541); `diff` tập (mã, thông điệp) merge-base vs HEAD rỗng ⇒ delta 0. `doctrine-scan` rc=0 (10 tệp, 0 chỗ), `adr-song` rc=0 (50/50), `git diff --check c16bec6...HEAD` rc=0 |

## Đợt đo 2 — toàn suite (A6/A9(a))

- **python3.11** (`wt5.iEzj/k` @66ec303): `python3.11 -B ops/lease_publish_test.py` ⇒ `lease_publish: 195/195 đạt; đã chạy=195,
  bỏ qua=0`, `rc=0`, `real 5m31s`; `grep -c '^@ca'` = 195 ⇒ N/N với N = số `@ca` tĩnh. Không dòng `ĐỎ`/`BỎ QUA` (log `full311.log`).
- **python3.13** (`k12`): `--chi-ca=t199_` ⇒ `1/1 đạt; bỏ qua=0`; `--chi-ca=t202_` ⇒ `1/1 đạt; bỏ qua=0`.
- python3.12 (CI ghim 3.12): xem cập nhật bên dưới.
- **python3.12.3** (`k12` @66ec303, cùng phiên bản CI ghim): ⇒ `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, `rc=0`,
  `real 6m33s`, 0 dòng `ĐỎ`/`BỎ QUA` (`full312.log`). ⇒ chốt so mã byte của t199 KHÔNG vỡ ở 3.12 (và 3.13 cho t199/t202):
  cả hai vế (`f.__code__` và `compile(nguon)`) do CÙNG trình thông dịch biên dịch, nên không phụ thuộc phiên bản.

## Đợt đo 3 — L1 lượt 4 (viết đè CÓ ĐIỀU KIỆN ở consumer) trên 66ec303

Công cụ: `mut.py` + `dot_bien.py` chép từ `rv689-l4/wt4.uqqV/` sang `wt5.iEzj/` (bản gốc không sửa), thêm biến thể lượt 5
(`_c196`, `C1T…C1N`, `H1…H5`, `C2b/C2c/C2g`). Lệnh: `wt5.iEzj/chay_d1.sh` ⇒ `d1.txt`/`d1.jsonl`. Nền `nen`: 8/8 ca `t195_…t202_` XANH.
Mọi "ĐỎ" dưới đây là `TinHieuChotCa` của ca đích (cột `True` trong `d1.txt`).

| đột biến | đơn lẻ | phối | kết luận |
|---|---|---|---|
| C1 (t196+t197: `if any(g[1].endswith("/comments") …): r = {**r,"rc":1,"out":""}`) | t202 ĐỎ "nối t196 bơm nền: consumer phải trao NGUYÊN VẸN …" | `+L`: t196/t197 XANH, **t202 ĐỎ** | **ĐÃ ĐÓNG** |
| C1b (t195 theo `::group::`) | t202 ĐỎ | `+L`: t195 XANH, **t202 ĐỎ** | **ĐÃ ĐÓNG** |
| C1c (t198 theo `::group::`) | t202 ĐỎ | `+A3`: t198/t201 XANH, **t202 ĐỎ** | **ĐÃ ĐÓNG** |
| C1T dò `type(r) is dict` rồi mới đọc `goi` (thẻ mù không bị chạm) | t202 ĐỎ ở lượt dict: "nối t196 bơm {'goi': …}" | `+L`: t202 ĐỎ | đóng (lượt dict) |
| C1I `isinstance(r, dict)` rồi đọc | t202 ĐỎ | `+L`: t202 ĐỎ | đóng — `isinstance` trên thẻ gọi `__getattribute__('__class__')` (đo 3.11/3.12/3.13: bị ghi) |
| C1E đọc trong `try/except BaseException` rồi nuốt | t202 ĐỎ | `+L`: t202 ĐỎ | đóng — `doc` ghi TRƯỚC khi ném |
| C1R sửa TẠI CHỖ `r["rc"]=1`, quyết định, rồi KHÔI PHỤC | t202 ĐỎ "bơm {'rc': 0}" | `+L`: t202 ĐỎ | đóng (ảnh `repr` lúc quyết định) |
| C1P sửa tại chỗ GIỮ `repr` (int con `__ne__`, str con `__contains__`) sau dò `type()` | t202 ĐỎ "…phải M3a: PR, nhận 'XANH'" | `+L`: t196/t197 XANH, **t202 ĐỎ** | đóng — lớp đồng nhất/`repr` MÙ ở đây, lớp KỲ VỌNG của hàng vectơ thật bắt: hai lớp độc lập, đo được |
| **C1N** dò TÊN helper (`__name__ == "_chay_buoc_dang_that"`) rồi viết đè vô điều kiện | 5/5 XANH | `+L`: **t196 XANH, t197 XANH, t202 XANH** (t195 ĐỎ vì C1N chỉ ở M3) | **SỐNG** — lớp executor tự khai (dò giàn) |
| **C1D** dò THỜI GIAN helper (`> 0.02s`) rồi viết đè | 5/5 XANH | `+L`: **t196/t197/t202 XANH** | **SỐNG** — dò giàn, không có trong danh sách ví dụ của docstring |

Phép đo phụ (vì sao `type()` một mình KHÔNG đủ để lọt): `wt5.iEzj/bang_nhau.py` chạy helper THẬT với nguồn đã gỡ `DONG_L`,
so NGUYÊN dict với vectơ của t202: `M2 null/*` 4/4 ô **bằng đúng** `vm2`; `M3 true/PR/…` và `M3 true/Issue/…` **bằng đúng** `vl3`;
các ô còn lại khác (`out` mang giá trị `lease_id` riêng). `vecto.py` (chép từ `l5/`): chuỗi hàm quyết định thật = chuỗi
vectơ ở cả 18 ô + M4 (`KHAC 0`). Hệ quả: mỗi họ có ≥1 ô thật mà (đầu vào, kết quả) TRÙNG hệt một hàng của lượt dict, nên
MỌI viết đè là hàm của (đầu vào, kết quả) — kể cả sau dò `type()` — hoặc kích hoạt ở hàng ấy (bị bắt), hoặc bỏ sót ô ấy
(`L` vẫn đỏ ở ô đó). Chỉ điều kiện nằm NGOÀI (đầu vào, kết quả) — tên/đồng nhất helper, thời gian, khung gọi, môi trường —
mới lọt (C1N, C1D).

## Đợt đo 4 — L2 lượt 4 (t199, gán lại helper) và đường vào lân cận

| đột biến | t199 | ghi chú |
|---|---|---|
| C2 gán lại bằng wrapper `functools.wraps`, ghi tệp TRƯỚC khi gọi | **ĐỎ** "M1: helper mà consumer gọi KHÔNG phải hàm biên dịch từ def duy nhất …" | **ĐÃ ĐÓNG** (lượt 4: 8/8 XANH) |
| C2b như C2 + `del w.__wrapped__` | ĐỎ (cùng dòng) | mã byte lệch |
| C2c GIỮ đối tượng hàm, thay `__code__` bằng mã có I/O, gọi bản sao `FunctionType(code gốc)` | ĐỎ (cùng dòng) | tệp `_io_truoc_guard_code.txt` được ghi (lúc t195 chạy) — tức đột biến CÓ răng thật |
| A9-always / A9-remove / A9-os-only / S4 / N13 | ĐỎ đúng ô S1+S3 / S2 / S3 / "S2 điểm dò tắt" / "S3 điểm dò tắt" | hồi quy A9(b) giữ nguyên; A9-always làm t195–t198,t200 `BOQUA` (đúng thiết kế) |
| **C2g** bọc `_ly_do_bo_qua_workflow` (chính hàm GUARD) bằng wrapper ghi tệp | **XANH** | tệp `_io_trong_guard.txt` được ghi khi chạy RIÊNG `t199_` (xoá tệp → chạy → tệp có lại, mtime 07:54:42Z) — I/O chạy ở cả S2 `nt`. Lớp executor TỰ KHAI ("I/O trong chính hàm guard"), nhưng docstring `t199` KHÔNG ghi giới hạn này (xem L2 dưới). |

**Độ giòn của so mã byte (mục 4):** toàn suite 3.12.3 và 3.11.15 đều 195/195; 3.13.12 t199/t202 xanh. Thêm: chạy `t199` với
`sys.settrace` bật (cách coverage/debugger cài hook) ⇒ XANH ở 3.11/3.12/3.13 (`co_code` không lộ mã đã instrument). Lý do cấu
trúc: hai vế do CÙNG trình thông dịch biên dịch, nên đổi phiên bản Python không làm lệch. Giòn còn lại (không đo, suy từ mã,
đều fail-closed = ĐỎ chứ không xanh giả): `.pyc` cũ khi module được IMPORT (không áp cho `__main__` mà CI dùng); công cụ viết
lại AST lúc import (pytest assertion rewriting — ca không theo tên `test_*` nên pytest không thu). `coverage` không cài: KHÔNG ĐO ĐƯỢC.

## Đợt đo 5 — token mờ có QUÁ CHẶT không (mục 4, cách viết consumer vô hại)

| biến thể consumer (không đổi ngữ nghĩa quan sát) | t195–t198 | t202 |
|---|---|---|
| H1 đổi tên biến + tách một dòng thành năm dòng (t196/t197) | XANH | **XANH** |
| H3 gom (nhãn, kết quả) vào danh sách rồi quyết định ở vòng thứ hai (t195) | XANH | **XANH** (thứ tự giữ nên `phat`/`nhan` khớp) |
| H2 gọi hàm quyết định bằng ĐỐI SỐ TÊN `_lech_tap_ii(nhan, kq=…)` | XANH | **ĐỎ bằng `TypeError`** (không phải `TinHieuChotCa`): "`_q.<locals>.q() got an unexpected keyword argument 'kq'`" |
| H4 thêm `goi` của kết quả vào thông điệp chốt (t198) | XANH | ĐỎ `TinHieuChotCa` "chạm ['__getitem__']" |
| H5 thêm `bang(isinstance(r, dict), …)` phòng vệ (t198) | XANH | ĐỎ `TinHieuChotCa` "chạm ['__getattribute__' …]" |

Kết luận: đổi tên/tách dòng/đổi thứ tự gom — KHÔNG đỏ oan. Đỏ oan có ba dạng, đều FAIL-CLOSED: H4/H5 là luật cố ý
("consumer không được ĐỌC kết quả helper", đã ghi ở docstring `t202`, CHƯA ghi ở docstring `t195`–`t198` — người sửa consumer
sẽ gặp nó lần đầu qua t202); H2 là giòn do cài đặt (`def q(*a)`), đỏ bằng ngoại lệ vô can.

## Đợt đo 6 — hồi quy finding lượt 1–4 (lấy mẫu có chủ đích, gồm phối với L) trên 66ec303

`wt5.iEzj/chay_d2.sh` ⇒ `d2.txt`/`d2.jsonl`, mỗi đột biến chạy đủ 8 ca `t195_…t202_` (phối: tập ca ghi cạnh). `LOI-CHAY` = 0.
Mọi ô ĐỎ là `TinHieuChotCa` của ca đích; không ô nào đỏ bằng ngoại lệ vô can; không `BOQUA` ngoài A9-always.

| nhóm (nguồn) | đột biến | ĐỎ |
|---|---|---|
| N1–N13 (lượt 2A, A11) | N1/N2/N3 · N4 · N5 · N6 · N7 · N8/N9 · N10/N11/N12 · N13 | t195+t202 · t196+t197+t202 · t197+t202 · t196+t202 · t196+t197+t202 · t202 · t201 · t199 (đợt 4) |
| R2-F3 (lượt 2B) | F3 1 chỗ · 2 chỗ · literal+gen | t196+t202 · t202 · t202 |
| R2-F4/F6, NA6 (lượt 2B/3) | F4-rc · F4-rc-va-out · F6-prefix · F6-rc · NA6 · NA6b | t202 (cả sáu) |
| NA1–NA5, NA7/NA7b, NA8, NA11 (lượt 3) | NA1/NA2 · NA3/NA4/NA5/NA8 · NA7/NA7b · NA11 | t195+t196+t197+t202 · t196+t197+t202 · t202 · t199 |
| advisory L4/L5 (lượt 3) | ADV-L4 gh không-JSON · ADV-L5 M3 `rc>0` | t198+t201 · t202 |
| lượt 1 S5/S1b | S5 đọc `HERE/lease_publish.py` · S1b gh chỉ số theo lần gọi | t200 · t201 |
| phối với `L` | F4-rc+L · F4-rc-va-out+L · NA6+L · NA6b+L · NA1+L · NA8+L · F3-2chỗ+L | t195,t196,t197,t202 · t195,t202 · t196,t197,t202 · t195–t197,t202 · t195–t197,t202 · t195–t197,t202 · t195–t197,t202 |
| phối A3/P-prefix | F6-rc+A3 · F6-prefix+P-prefix · NA7+P-prefix | t198+t202 · t202 · t202 |
| L1/L2 lượt 4 | C1+L, C1b+L, C1c+A3, C2 | t202, t202, t202, t199 (đợt 3–4) |

Tập ô ĐỎ của phần giao với bảng lượt 4 (`luot4/VERDICT.md` đợt 2–3) **khớp**; phần giao với bảng executor
(`bang-do-executor/bang_l5.txt`: C1→t202, C1+L→t195,t202, C1b+L→t196,t197,t202, C1c+A3→t202, C2→t199) **khớp** — đo lại, không tin.

Phép thử phụ: consumer ném `BoQuaNen` có điều kiện (C1K+L) ⇒ bộ chạy thật `--chi-ca=t196_` và `--chi-ca=t202_` đều
`ĐỎ … bỏ qua không dẫn xuất được từ runs-on`, `0/1 đạt`, rc=1 — ồn, không lọt (đỏ ở tầng bộ chạy, không phải `TinHieuChotCa`).

## Đợt đo 7 — HINT.patch trên `wt5.iEzj/h` (@66ec303 + patch)

- `git -C cay-kho apply --check HINT.patch` ⇒ OK; chỉ `ops/lease_publish_test.py`, `+8/−3`. Sau khi áp: `git diff --numstat
  c16bec6` ⇒ `581 4` ≤ 600 (A7(2); còn 19 dòng). ruff F: tập lỗi = merge-base (delta 0). `git diff --check` sạch. Dòng thêm ≤ 118 ký tự.
- Toàn suite **python3.12** trên `h`: `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, rc=0, `real 6m46s`, 0 `ĐỎ`/`BỎ QUA`.
- Đột biến trên `h` (`hint.jsonl`): H2 (đối số tên) ⇒ t202 **XANH** (66ec303: `TypeError`); H1 ⇒ XANH; C1+L, C1b+L, C1P+L,
  C1c+A3 ⇒ t202 ĐỎ `TinHieuChotCa` (không mất răng); C2 ⇒ t199 ĐỎ; C1N+L ⇒ t202 XANH (giới hạn đã khai, không đổi). Đột biến
  làm ca khoá của phần mã ĐỎ: gỡ `**kw`/`bind` (tức 66ec303) ⇒ H2 đỏ t202 bằng `TypeError` — đo ở đợt 5.
- Phần docstring của patch chỉ thu hẹp/đặt đúng lời khai, không có ca khoá riêng.

## L1 — Giới hạn đã khai của `t202` (dò giàn) đo được; câu chữ giới hạn chưa khớp phép đo

**P4 · mang (lớp executor tự khai) · hồ sơ (docstring).**

Biểu hiện: `ops/lease_publish_test.py:10887`–`:10890` (docstring `t202`): *"GIỚI HẠN … consumer dò GIÀN (`type()`, tên
helper, môi trường) VÀ viết đè theo đặc trưng không vectơ nào có thì lọt."* Đo (đợt 3):
- `type()` KHÔNG đủ để lọt: C1T/C1P (dò `type()` rồi đọc/sửa) ⇒ t202 ĐỎ; `bang_nhau.py` cho thấy mỗi họ có ô thật TRÙNG HỆT
  một vectơ (M2 null 4/4, M3a true, M3b true) ⇒ viết đè là hàm của (đầu vào, kết quả) không thể né lượt dict mà vẫn phủ mọi ô.
- Thứ lọt THẬT là điều kiện nằm ngoài (đầu vào, kết quả), và KHÔNG cần "đặc trưng" nội dung nào: C1N (tên helper) và C1D
  (thời gian chạy helper > 20 ms) viết đè VÔ ĐIỀU KIỆN theo nội dung ⇒ `+L`: t196/t197/t202 XANH.
Mức: P4 — cả hai đều là consumer CỐ Ý dò giàn (đối kháng), không phải trôi vô tình; lớp đã được khai; lời khai hiện tại
không rộng hơn phép đo về phía "đã đóng" (nó liệt kê thừa `type()`, và "VÀ … đặc trưng" hẹp hơn thực tế một chút).
Rủi ro phụ (không đo được, suy từ mã): tính "ô thật trùng hệt vectơ" phụ thuộc chuỗi thông điệp của `lease_publish.py`; đổi
thông điệp (ví dụ #678) thì tính chất ấy mất âm thầm, t202 vẫn xanh — nhưng chỉ lớp "dò `type()`" bị ảnh hưởng, vì lượt thẻ mù
bắt MỌI lần đọc bất kể vectơ.

**Hint patch** (`HINT.patch`, hunk `@@ -10886`): thay hai dòng giới hạn bằng câu khớp phép đo (dò `type()` rồi đọc cũng đỏ;
lọt = rẽ nhánh theo thứ NGOÀI (đầu vào, kết quả): tên/đồng nhất helper, thời gian chạy, khung gọi, môi trường). Không ca khoá
(docstring). Không đề xuất đóng bằng mã: đóng lớp dò giàn đòi chạy `L` thật trong suite (trái §10.5) — quyết định chủ kho.

## L2 — `t199` không khai giới hạn "I/O trong chính hàm guard"; đo được đường ấy xanh

**P4 · mang (executor khai ở bàn giao, KHÔNG khai trong mã) · hồ sơ (docstring).**

Biểu hiện: `ops/lease_publish_test.py:10744`–`:10746` (docstring `t199`) mô tả chốt "thao tác TRƯỚC guard" (AST + mã byte của
helper) mà không nói phạm vi dừng ở ĐỐI TƯỢNG helper. Phép đo: C2g (`_ly_do_bo_qua_workflow = _boc_guard(...)`, wrapper ghi
tệp) ⇒ `python3 -B mut.py C2g-boc-ham-guard t199_` ⇒ `XANH`, và `ops/_io_trong_guard.txt` được tạo lại bởi chính lượt chạy
t199 (xoá trước, mtime 07:54:42Z sau). A9(b) của spec không đòi đo hàm guard từ bên trong; `_ly_do_bo_qua_workflow` vốn ĐỌC
tệp workflow theo thiết kế — nên không phải lời khai rộng hơn phép đo, mà là giới hạn chỉ nằm trong bàn giao (doctrine: "đừng
để nó nằm trong prompt/mô tả PR").

**Hint patch** (`HINT.patch`, hunk `@@ -10744`): thêm hai dòng GIỚI HẠN vào docstring t199 (I/O trong hàm guard/`BoQuaNen` bị
bọc, lúc import, sửa helper sau khi ca chạy). Không ca khoá. Nếu chủ kho muốn đóng bằng mã: mở rộng phép so mã byte của t199
sang `_ly_do_bo_qua_workflow` (cùng `_ma`) — chưa dựng, chưa đo, nên KHÔNG đưa vào patch.

## L3 — Độ giòn của thẻ mù: đổi cách GỌI hàm quyết định vô hại làm t202 đỏ bằng ngoại lệ vô can

**P4 · mới · mã test (write set) + hồ sơ.**

Biểu hiện: `ops/lease_publish_test.py:10953` `def q(*a)` — thay cho `_lech_tap_i/_lech_tap_ii/_lech_m4` khi t202 gọi consumer.
Hàm thật nhận `kq` theo tên; `q` thì không. Đo (đợt 5): H2 `_lech_tap_ii(nhan, kq=…)` ⇒ t195–t198 XANH, t202 **ĐỎ bằng
`TypeError`** "`q() got an unexpected keyword argument 'kq'`" (cột `False` — không phải `TinHieuChotCa`). Fail-closed nhưng
đỏ vì lý do vô can, đúng loại tín dụng/đỏ giả mà kho đã trả giá. Kèm: luật "consumer không được ĐỌC kết quả helper" (H4 thêm
`goi` vào thông điệp, H5 `isinstance` phòng vệ ⇒ t202 đỏ "chạm …") chỉ ghi ở docstring t202, không ở t195–t198.
Không giòn: đổi tên biến, tách dòng, gom-rồi-quyết (H1, H3 ⇒ XANH).

**Hint patch** (`HINT.patch`, hunk `@@ -10950` + `import inspect`): `def q(*a, **kw)` rồi
`a = tuple(inspect.signature(that[ten]).bind(*a, **kw).arguments.values())`. Ca khoá: `t202` với consumer H2 phải XANH; đột
biến gỡ `**kw`/`bind` (= 66ec303) ⇒ t202 ĐỎ `TypeError` (đo). Các đột biến giết của L1 lượt 4 vẫn chết trên bản patch (đợt 7).

## L4 — Ghi nhận mang từ lượt 4 (không chặn)

**P4 · mang · hồ sơ.** Nối sổ `BoQuaNen` #687 (t202 không đi guard; Windows thật: KHÔNG ĐO ĐƯỢC); trục actor của tọa độ đọc
giá trị KHAI; nhật ký `gh` giả không có hợp đồng (C5); `t202` nhận diện chốt bằng TIỀN TỐ thông điệp (sửa câu chốt ⇒ sửa t202,
fail-closed). Không đo lại lượt này ngoài phần đã có trong đợt 6.

## Mục 1 — L1/L2 lượt 4: trạng thái trên 66ec303

| finding lượt 4 | trạng thái | bằng chứng |
|---|---|---|
| L1 (viết đè có điều kiện lọt t202: C1/C1b/C1c) | **ĐÃ ĐÓNG** (theo lớp, cho mọi điều kiện là hàm của (đầu vào, kết quả)) | C1+L, C1b+L, C1c+A3, C1T, C1I, C1E, C1R, C1P ⇒ t202 ĐỎ `TinHieuChotCa`; `L` gốc chết ở t195/t196/t197 (đợt 3, 6). Còn lại: lớp dò giàn đã khai (L1 lượt 5, P4) |
| L2 (rebind `functools.wraps` vượt AST t199) | **ĐÃ ĐÓNG** (cho mọi thay đổi ĐỐI TƯỢNG helper) | C2, C2b, C2c ⇒ t199 ĐỎ `TinHieuChotCa`. Còn lại: callee của guard (L2 lượt 5, P4) |
| L3 (điều kiện dừng S2) | xem dòng CÙNG HÌNH DẠNG | — |
| L4 (ghi nhận) | MANG — P4 | L4 lượt 5 |

## Bảng trạng thái mọi finding cũ trên 66ec303

| finding | nguồn | trạng thái | bằng chứng (đợt) |
|---|---|---|---|
| R1-F1 guard khi dò tắt | lượt 1 | ĐÃ ĐÓNG | S4 ⇒ t199 "S2 điểm dò tắt: nhận 'IO'" (4) |
| R1-F2 giảm miền M2/M3 | lượt 1 | ĐÃ ĐÓNG | N1–N7, NA1–NA5 (6) |
| R1-F3 chốt mã thoát M3 | lượt 1 | ĐÃ ĐÓNG | ADV-L5, F4-rc (6) |
| R1-F4 mặc định đọc bản neo | lượt 1 | ĐÃ ĐÓNG | S5 ⇒ t200 (6) |
| R1-F5 gh đánh chỉ số lần gọi | lượt 1 | ĐÃ ĐÓNG | S1b ⇒ t201 (6) |
| R1-F6 t70 kiểm kê | lượt 1 | ĐÃ ĐÓNG (t70 không đổi ở `85124dc..66ec303`; xanh trong toàn suite) | (2) |
| R1-F7 tiền tố POST M4 | lượt 1 | ĐÃ ĐÓNG | N8, NA7, NA7b, F6 (6) |
| R1-F8 docstring 12/14 | lượt 1 | ĐÃ ĐÓNG | docstring t195 không đổi ở lượt 5 |
| L1-E1…E13 (N1–N13) | lượt 2A | ĐÃ ĐÓNG | (4, 6) |
| L2 trần A7 | lượt 2A | ĐÃ ĐÓNG (hồ sơ); đo 576 ≤ 600 | (1) |
| L3 nối sổ #687 | lượt 2A | MỞ — P4 | L4 |
| R2-F1, F2, F5, F7, F8 | lượt 2B | ĐÃ ĐÓNG | N1, N7/N4, N10, N1–N3 (6) |
| R2-F3 | lượt 2B | ĐÃ ĐÓNG | F3 ×3 (6) |
| R2-F4 / R2-F6 consumer | lượt 2B | ĐÃ ĐÓNG (cả viết đè có điều kiện) | F4*, F6*, C1*, C1c (3, 6) |
| lượt 3 L1(a) consumer, NA6 | lượt 3 | ĐÃ ĐÓNG | NA6/NA6b ±L, C1b (3, 6) |
| lượt 3 L1(b) tọa độ NA1–NA5, NA8 | lượt 3 | ĐÃ ĐÓNG | (6) |
| lượt 3 L2 NA7 | lượt 3 | ĐÃ ĐÓNG | (6) |
| lượt 3 L3 NA11 I/O trước guard | lượt 3 | ĐÃ ĐÓNG (câu lệnh chèn + đối tượng helper); callee guard: P4 | NA11, C2/C2b/C2c; C2g (4, 6) |
| lượt 3 L4 nối sổ #687 | lượt 3 | MỞ — P4 | L4 |
| advisory L1–L5 | lượt 3 adv | ĐÃ ĐÓNG | như trên; ADV-L4/L5 (6) |
| lượt 4 L1 / L2 | lượt 4 | ĐÃ ĐÓNG | mục 1 |
| lượt 4 L3 điều kiện dừng S2 | lượt 4 | đã chuyển chủ kho (chủ kho cho vá tiếp) | PROMPT |
| lượt 4 L4 ghi nhận | lượt 4 | MANG — P4 | L4 |

## Bảng lớp

| lớp | mức | mới / mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 — giới hạn dò giàn của `t202`: C1N/C1D lọt (đã khai); câu chữ liệt kê thừa `type()`, thiếu "không cần đặc trưng nội dung" | P4 | mang (lớp tự khai) | hồ sơ (docstring) |
| L2 — `t199` không khai "I/O trong hàm guard" (C2g xanh, I/O chạy thật) | P4 | mang (khai ở bàn giao, chưa ở mã) | hồ sơ (docstring) |
| L3 — `def q(*a)` làm t202 đỏ `TypeError` khi consumer gọi `kq=` (H2); luật "không đọc kết quả" chưa ghi ở t195–t198 | P4 | mới | mã test (2 dòng) + hồ sơ |
| L4 — ghi nhận mang từ lượt 4 | P4 | mang | hồ sơ |

Tổng: **0 P1 / 0 P2 / 0 P3 / 4 P4**. A1–A11 của r8 ĐẠT theo lệnh đo của chúng (đợt 1, 2, 3, 4, 6). HINT.patch là GỢI Ý (P4),
không chặn; lease g5 hết hạn `2026-09-30T10:48:00Z`, lượt này kết thúc đo ~08:05Z.

CÙNG HÌNH DẠNG lượt 3–4: KHÔNG — lượt này không có đường vào MỚI nào sống sót ngoài lớp đã khai. L1/L2 lượt 4 đóng theo
LỚP (đo: mọi điều kiện là hàm của (đầu vào, kết quả) đều chết, nhờ ô thật trùng hệt vectơ; mọi thay đổi đối tượng helper đều
chết), không theo ví dụ. Hai đường còn sống (C1N/C1D dò giàn; C2g callee guard) nằm trong giới hạn executor đã khai, cả hai
là thao tác CỐ Ý đối kháng giàn, và không có lời khai nào trong mã rộng hơn phép đo (chỉ câu chữ chưa khít — P4).

Dọn: worktree tạm `wt5.iEzj/{k,k12,m,h}` đã `git worktree remove --force` (log/bảng đo giữ ở `wt5.iEzj/`: `full311.log`,
`full312.log`, `hint-full312.log`, `d1.*`, `d2.*`, `hint.jsonl`, `mut.py`, `dot_bien.py`, `bang_nhau.py`, `vecto.py`). `cay-kho`
không bị sửa: HEAD 66ec303, `git status --short` rỗng; không lệnh `git config` nào có đối số (một lần heredoc không trích dẫn
của chính reviewer vô tình chạy `git config`/`git worktree remove --force` KHÔNG đối số — cả hai chỉ in usage, không đổi gì).

VERDICT: PASS
