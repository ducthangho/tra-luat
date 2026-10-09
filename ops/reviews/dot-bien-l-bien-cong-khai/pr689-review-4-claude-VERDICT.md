# Review MÃ lượt 4 — PR #689 / packet #677 (wp677, DOT-BIEN-L-BIEN-CONG-KHAI)

- reviewer: **Claude Opus 5.5** (general-purpose, thay cho agent `review-opus-max` chưa được nạp). Effort "max" là
  TỰ KHAI trong chỉ thị — KHÔNG đặt được, KHÔNG ĐO ĐƯỢC.
- nhãn assurance: **`advisory_review`** (reviewer cùng họ Claude với executor — KHÔNG phải cross-review khác nền)
- reviewed_sha: `85124dceb17b63b867dc2fb322d06925c67fff07` (đo: `git -C cay-kho rev-parse HEAD`), cha `e55c5e2`
- merge-base với master: `c16bec639efa0077def4916c25c3e0c17f68dcaa` (đo: `git merge-base HEAD origin/master`)
- baseline A8 / start_from_sha: `89fc4fac8cea65979cc2483043dc8cd07a6e8518`
- spec r8 sha256 đo lại: `4dfbfd69e161d55aa28f2685741cdcf11fcd5171438081e9eb63815c69bb4094` (`sha256sum SPEC-r8.md`) — khớp PROMPT
- Môi trường: Linux sandbox, Python 3.11.15, PyYAML 6.0.1, `ruff`/`shellcheck`/`actionlint` CÓ mặt. Windows thật, HTTP GitHub: KHÔNG ĐO ĐƯỢC.
- Worktree tạm (detached): `wt4.uqqV/k` (toàn suite @85124dc), `wt4.uqqV/m` (đột biến @85124dc), `wt4.uqqV/e` (@e55c5e2).
  Đột biến ghi thành tệp test RIÊNG tên khác (`ops/_m4_<tên>_test.py`), không ghi đè tệp gốc; `PYTHONDONTWRITEBYTECODE=1`, `python -B`.
  Mỗi (đột biến, ca) chạy trong tiến trình con gọi ĐÚNG hàm ca, ghi LỚP ngoại lệ + `isinstance(e, TinHieuChotCa)`.

Nhật ký tăng dần bên dưới.

## Đợt đo 1 — nghiệm thu tĩnh (A7, A8, A10)

| mục | kết quả | phép đo |
|---|---|---|
| A7(1) | ĐẠT | `git diff --name-only c16bec63…(merge-base)...HEAD` ⇒ đúng `ops/lease_publish_test.py` (merge-base mới nhất với master theo điều khoản A7) |
| A7(2) | ĐẠT | `git diff --numstat c16bec6...HEAD` ⇒ `501 4` ≤ 600 (Q19). Lượt 4 (`e55c5e2..85124dc`): `+132/−53`. Còn 99 dòng tới trần S4. |
| A8 | ĐẠT | `wt4.uqqV/a8.py`: cắt AST (kèm decorator) `_chay_buoc_dang` + 15 ca `t51`–`t68` ở `89fc4fa` và HEAD ⇒ `so khoi 16 16`, `lech []`. Hunk của diff merge-base: chỉ `@@ -2987` (t70, M6) và `@@ -10449` (khối mới). `--chi-ca=t5`/`t6`: xem đợt đo toàn suite. |
| A10 | ĐẠT | ruff 0.15.8 `--select F --no-cache` trên bản `git show`: HEAD 9 lỗi, merge-base 9, start_from 9; tập (mã, thông điệp) bằng nhau ⇒ delta 0. `doctrine-scan` rc=0 (10 tệp, 0 chỗ), `adr-song` rc=0 (50/50), `git diff --check c16bec6...HEAD` rc=0 |

Ghi chú hồ sơ: lease g5 `lease_expires_at_utc: 2026-09-30T10:48:00Z`; lượt này đo lúc ~06:50Z (`date -u`) — còn hạn,
nhưng mọi bản vá sau lượt này rơi sát hạn (S3 của lease).

## Đợt đo 2 — toàn suite (A6) và nghiệm thu động A1–A5, A9, A11

**A6 — ĐẠT.** Worktree `wt4.uqqV/k` @85124dc: `python -B ops/lease_publish_test.py` ⇒
`lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, rc=0, `real 5m44s`; `grep -c '^@ca'` = 195. `shellcheck`/`actionlint`
có mặt nên t137/t159 không đỏ vì thiếu công cụ (log `wt4.uqqV/full-suite.log`). Bao gồm `t5*`/`t6*` (A8 vế động).

Bộ đột biến: `wt4.uqqV/mut.py` + bảng `wt4.uqqV/dot_bien.py` (mỗi phép thay chuỗi khẳng định ĐÚNG số lần xuất hiện).
Lệnh: `CAY=wt4.uqqV/m python -B wt4.uqqV/mut.py <đột-biến[+…]> t195_,t196_,…,t202_`. Nền: 8/8 ca đích XANH.
Kết quả thô `wt4.uqqV/dot1.txt` / `dot1.jsonl`. "8/8 xanh" = cả tám ca `t195_`…`t202_` XANH (không khai toàn suite).

| mục | kết quả | dòng ĐỎ (rút gọn; mọi dòng là `TinHieuChotCa`) |
|---|---|---|
| A1 | ĐẠT | `L` ⇒ t195 "M2 tập (i): … lệch: null/Issue/trống: rc=1 goi=[('GET', 'repos/o/r/issues/55/comments')] POST=0; …" |
| A2 | ĐẠT (cả hai họ, qua mã thoát) | `L` ⇒ t196 "M3a: … lệch: true/PR/có dấu/còn hạn: rc=0 POST=0 bỏ_qua=True; 1.5/…; ngày/…"; t197 "M3b: … true/Issue/có dấu/hết hạn: rc=0 POST=0 bỏ_qua=True; …" |
| A3 | ĐẠT | gh khỏi PATH ⇒ t198 "M4: chuỗi hợp lệ … phải rc=0; nhận rc=1 … CHAN [8]: KHÔNG ĐO ĐƯỢC loại số hiệu: không gọi được `gh api`" |
| A4 | ĐẠT | gh không lưu POST ⇒ t198 "M4: phải ĐÚNG 1 POST … nhận POST=[]" (+ t201 "sau POST phải còn comment cũ và thêm đúng MỘT") |
| A5 | ĐẠT | mọi đỏ A1–A4 là `TinHieuChotCa` của đúng ca đích; không ca đích nào đỏ bằng ngoại lệ vô can |
| A9(a) | ĐẠT | toàn suite `bỏ qua=0`; t195–t202 chạy thật trên Linux |
| A9(b) | ĐẠT | luôn ném ⇒ t199 "S1 bật/tắt, S3 bật/tắt"; gỡ ⇒ "S2 bật/tắt"; chỉ `os.name` ⇒ "S3 bật/tắt"; S4 (chỉ khi bật dò) ⇒ "S2 điểm dò tắt: nhận 'IO'"; N13 ⇒ "S3 điểm dò tắt: nhận 'chan'". Mỗi dòng đỏ chứa ĐÚNG ô hành vi **và** thêm dòng AST — tức chốt AST mới KHÔNG che/thay chốt hành vi (đo được: phần hành vi của thông điệp vẫn đúng ô) |
| A11 | ĐẠT cho N1–N13 | bảng dưới |

**A11 — N1…N13 dựng lại theo mô tả verdict lượt 2 (A) trên 85124dc:**

| đột biến | ca đỏ (`TinHieuChotCa`) |
|---|---|
| N1 raw ánh xạ→null | t195 (tọa độ) + t202 |
| N2 mọi ô M2 là Issue | t195 + t202 |
| N3 M2 bỏ dấu | t195 + t202 |
| N4 M3 bỏ dấu | t196 + t197 + t202 |
| N5 mọi ô M3 là PR | t197 + t202 |
| N6 mọi ô M3 hết hạn | t196 + t202 |
| N7 ngày→true | t196 + t197 + t202 |
| N8 `in` thay `startswith` | t202 |
| N9 `rc == 1` | t202 |
| N10 GET sau POST exit 1 | t201 |
| N11 cắt body | t201 |
| N12 tác giả `human` | t201 |
| N13 nhánh nt khi tắt dò | t199 "S3 điểm dò tắt: nhận 'chan', phải 'IO'" |

(t202 đỏ ở N1–N7 vì t202 nay gọi CHÍNH t195–t197 qua helper giả mà tọa độ lấy từ đầu vào, nên fixture trôi cũng
làm t202 đỏ — tín dụng thêm, không phải tín dụng giả: thông điệp là "nối t19x bơm nền: phải XANH, nhận 'M2: tọa độ …'".)

## Đợt đo 3 — finding cũ (luot1/2A/2B/3/3-advisory) trên 85124dc

Cùng bộ `mut.py`, kết quả `wt4.uqqV/dot1.txt`. Mọi "ĐỎ" dưới đây là `TinHieuChotCa` của ca đích (cột 5 = `True`).

| đột biến (theo mô tả lượt cũ) | trên 85124dc | dòng ĐỎ rút gọn |
|---|---|---|
| R2-F4 `F4-rc` (`{**helper, "rc":1}` ở t196+t197) | CHẾT | t202 "nối t196 bơm {'rc': 0}: phải M3a: PR, nhận 'XANH'" |
| R2-F4c `F4-rc-va-out` | CHẾT | t202 "nối t196 bơm {'rc': 0} … bơm {'out': 'đã đăng trước đó — bỏ qua'} …" |
| R2-F6 `F6-prefix-t198` | CHẾT | t202 "nối t198 bơm {'dang': []}: phải M4:, nhận 'XANH'; …" |
| R2-F6' `F6-rc-t198` | CHẾT | t202 |
| NA6 `kq["goi"]=[]` trong t195 | CHẾT | t202 "nối t195 bơm {'goi': [('GET', …/comments')]}: phải M2 tập (i), nhận 'XANH'" |
| NA6b `kq["rc"]=1` trong t195 | CHẾT | t202 |
| R2-F3 1 chỗ | CHẾT | t196 (tọa độ) + t202 |
| R2-F3 2 chỗ (`_o_tap_ii` + khoá `_TD_M3`) | CHẾT | t202 "VAI (PR, hết hạn) mà t196/t197 truyền lệch M3a/M3b: {(False, True)} · {(False, True)}" |
| R2-F3' đổi LITERAL `_TD_M3["M3a"]` + generator | CHẾT | t202 (ghim VAI độc lập với `_TD_M3`) |
| NA1 tác giả dấu ≠ bot | CHẾT | t195/t196/t197 tọa độ "(('nguoi-that', …),)" + t202 |
| NA2 dấu không ở đầu thân | CHẾT | t195/t196/t197 + t202 |
| NA3 comment hỏng trước dấu | CHẾT | t196/t197 + t202 |
| NA4 `packet_issue: 56` | CHẾT | t196/t197 "… ('packet_issue=55 (int)', 'trường khác = lease_mau()')" + t202 |
| NA5 tự cấp | CHẾT | t196/t197 + t202 |
| NA7 tiền tố M4 rút ngắn · NA7b bỏ `**` cuối | CHẾT | t202 "M4 tiền tố lệch ở vị trí 14/15/16… vẫn qua"; "…vị trí 17; 18" |
| NA8 `issue_loi=True` ở M3 | CHẾT | t196/t197 (tọa độ có trục `issue_loi`) + t202 |
| NA11 I/O TRƯỚC guard (câu lệnh chèn) | CHẾT | t199 "M1: guard rồi điểm dò phải là HAI câu lệnh ĐẦU TIÊN …" |
| advisory L4 gh in không-JSON | CHẾT đúng lý do | t201 "mọi GET thành công phải in JSON hợp lệ: Expecting value …" (+ t198) |
| advisory L5 M3 `rc>0` thay `rc≠0` | CHẾT | t202 "M3 đối chứng rc=-1" |
| advisory L5 `issue_loi` không ca nào dùng | ĐÓNG (theo hợp đồng gh) | t201 nay gọi GET #57 `issue_loi` ⇒ rc≠0; helper vẫn nhận tham số, không ca biên nào bật nó (trục bổ sung R2-F2 **không** khoá — đúng Q12) |
| luot1 S5 (helper đọc `HERE/lease_publish.py` thay `SCRIPT`) | CHẾT | t200 "M1: mặc định không đọc SCRIPT của cây; rc=0 …" |
| luot1 S1b (gh đánh chỉ số theo lần gọi) | CHẾT | t201 "hai GET liền nhau phải cùng snapshot đúng [[comment cũ]]: … vs [[]]" |
| luot1 S3 / S7 | CHẾT | = ADV-L5/N9 (M3/M4 rc) và N8/NA7 (tiền tố) ở trên |
| luot1 S6 / R1-F6 (t70) | không đo lại | `git diff 1290ebb 85124dc` không có hunk nào trong `t70`; t70 xanh trong toàn suite |

Không đột biến nào trong 42 mục của đợt 1 sống (trừ `P-bo-chot-PR`: đột biến TƯƠNG ĐƯƠNG trên sản phẩm — gỡ nhánh
`/pull/` thì `_kiem_loai_so_hieu` vẫn ném "KHÔNG ĐO ĐƯỢC loại số hiệu" ở chốt kế tiếp, nền vẫn rc≠0; không phải finding).
Nhận xét: bảng executor khai "85124dc 0 sống" — trên phần giao với bảng này, đo lại KHỚP.

## Đợt đo 4 — đường vào MỚI của các chốt lượt 4

Kết quả thô `wt4.uqqV/dot2.txt`, `dot3.jsonl`.

| đột biến | đơn lẻ (8 ca) | phối | kết luận |
|---|---|---|---|
| **C1** t196+t197: `if any(g[1].endswith("/comments") for g in r["goi"]): r = {**r, "rc": 1, "out": ""}` | 8/8 XANH | `+L`: **t196 XANH, t197 XANH, t202 XANH** (t195 vẫn đỏ) | **SỐNG — A2 mất ở CẢ HAI họ** (L1) |
| **C1b** t195: `if "::group::" in kq["out"]: kq = {**kq, "rc": 1, "goi": [], "dang": []}` | 6/6 XANH | `+L`: **t195 XANH, t202 XANH** (t196/t197 đỏ) | **SỐNG — A1 mất** (L1) |
| **C1c** t198: `if "::group::" in r["out"]: r = {… rc 0, 1 POST đúng tiền tố, goi hợp lệ}` | 6/6 XANH | `+A3`: **t198 XANH, t201 XANH, t202 XANH**; `+A4`: t201 ĐỎ | **SỐNG — A3 mất** (A4 còn nhờ t201) (L1) |
| **C2** gán lại `_chay_buoc_dang_that = _boc_io(_chay_buoc_dang_that)` với `functools.wraps`, ghi tệp TRƯỚC khi gọi | 8/8 XANH; tệp `m/ops/_io_truoc_guard_wraps.txt` ĐƯỢC GHI | — | **SỐNG** — chốt AST bị vòng qua vì `inspect.getsource` tự `unwrap` (L2) |
| C3 truyền `env={**mt, "GITHUB_ACTOR": "ke-la"}` cho subprocess (tọa độ đọc `mt`) | t198 ĐỎ "CHAN [4] GITHUB_ACTOR='ke-la'" | `+L`: t196/t197 XANH nhưng t198 vẫn đỏ | chết nhờ đối chứng dương M4 — không phải finding; nhưng trục "actor" của tọa độ đọc giá trị KHAI chứ không phải giá trị GIAO (ghi nhận, P4) |
| C3b actor rỗng cho subprocess | 8/8 XANH | `+L`: t195/t196/t197 ĐỎ | tương đương về độ phân biệt `L`; không finding |
| C4 đổi một trường của `lease_mau()` (event, role, provider, attempts_used 3/9, target_pull_request None, packet_id) | 8/8 XANH mỗi cái | `+L`: t195/t196/t197 ĐỎ cả 7 | so với `lease_mau()` không độc lập, nhưng KHÔNG trường nào đo được che `L`; không finding |
| C5 gh giả chỉ ghi nhật ký cho endpoint `comments` | 6/6 XANH | — | vô hại với `L` (tín hiệu M2 là GET `comments`); nhật ký lời gọi không có hợp đồng ở t201 — P4 ghi nhận |

## L1 — Đường nối helper → consumer của `t202` chỉ đo viết đè KHÔNG điều kiện; viết đè theo đặc điểm của lượt chạy THẬT lọt, mất A1/A2/A3 mà cổng xanh

**P3 · mang (cùng hình dạng R2-F4/R2-F6 lượt 2 → L1a lượt 3), đường vào MỚI · sửa mã test (write set) + thu hẹp lời khai.**

Biểu hiện: `ops/lease_publish_test.py:10864` (`t202`, docstring: *"viết đè quan sát ở consumer phải đỏ ở chốt QUYẾT
ĐỊNH của ca đó"*) và `:10930`–`:10938` (`bang_noi`). Helper giả trả `{"goi": [], "dang": [], "out": "", **nền, **một
chiều sai}` — tức mọi vectơ bơm vào đều KHÁC hình dạng của lượt chạy thật ở hai điểm: `out` không bao giờ chứa
`::group::`, và ở M3 chiều `goi` chỉ được bơm cùng `rc=1` (ô mong XANH). Một consumer viết đè CÓ ĐIỀU KIỆN theo đúng
một trong hai điểm ấy thì không bao giờ kích hoạt dưới helper giả, nhưng kích hoạt dưới helper thật:

| đột biến (MỘT chỗ sửa trong consumer) | đơn lẻ | phối | mất |
|---|---|---|---|
| C1 (t196+t197) `if any(g[1].endswith("/comments") for g in r["goi"]): r = {**r, "rc": 1, "out": ""}` | 8/8 XANH | `+L`: t196 **XANH**, t197 **XANH**, t202 **XANH** | **A2 cả hai họ** |
| C1b (t195) `if "::group::" in kq["out"]: kq = {**kq, "rc": 1, "goi": [], "dang": []}` | 6/6 XANH | `+L`: t195 **XANH**, t202 **XANH** | **A1** |
| C1c (t198) `if "::group::" in r["out"]: r = {…rc 0, 1 POST đúng tiền tố, goi hợp lệ}` | 6/6 XANH | `+A3`: t198/t201/t202 **XANH** | **A3** (A4 còn nhờ t201) |

Phép đo tái lập (từ `wt4.uqqV/`, `CAY=$PWD/m`): `python -B mut.py C1-M3-rewrite-theo-goi+L t195_,t196_,t197_,t202_` ⇒
`t195_ DO TinHieuChotCa …`, `t196_ XANH`, `t197_ XANH`, `t202_ XANH`; `python -B mut.py C1b-M2-rewrite-theo-out+L
t195_,t202_` ⇒ `XANH`/`XANH`; `python -B mut.py C1c-M4-rewrite-theo-out+A3-no-PATH t198_,t201_,t202_` ⇒ `XANH`×3
(thô: `dot2.txt`, `dot3.jsonl`).

Vì sao P3, không P2: viết đè có điều kiện theo `::group::`/`/comments` không phải hình dạng trôi vô tình như R2-F4
(gán hằng); mọi viết đè KHÔNG điều kiện đã bị bắt (đợt 3). Việc `L` chết THẬT vẫn được A1/A2 bảo chứng bằng đột biến lúc
review (đợt 2). Nhưng docstring `t202` khai rộng hơn phép đo — hình dạng `LOI-KHAI-RONG-HON-PHEP-DO` — và đây là lượt
THỨ BA liên tiếp cùng hình dạng "đường nối helper → consumer đo hẹp hơn lời khai" (xem L3).

**Hint patch** (`HINT.patch`, phần `t202`; đã đo): thêm vào `bang_noi` bốn hàng mang **vectơ quan sát THẬT** — chép từ
helper thật trên 85124dc (`wt4.uqqV/h`, chạy `_chay_buoc_dang_that(…, nguon_lease_publish=<SCRIPT bỏ DONG_L>)`):
`L` ở M3 = `rc 0, goi [GET …/comments], out "::group::…\nđã đăng trước đó — bỏ qua\n::endgroup::\nCHAN [9]: …"`; `L` ở M2
= `rc 1, goi [GET …/comments], out "::group::…::error…CHAN [8]: thiếu trường bắt buộc: lease_id"`; A3 ở M4 = `rc 1, dang
[], goi [], out "…CHAN [8]: KHÔNG ĐO ĐƯỢC loại số hiệu: không gọi được `gh api`"`. Mỗi hàng mong đỏ ở đúng chốt quyết định
của ca. Kèm hai dòng docstring thu hẹp lời khai: viết đè theo đặc điểm NẰM NGOÀI các vectơ ấy là giới hạn đã biết.
Không nhúng đột biến `L` chạy thật vào suite: làm thế là cam kết "`L` chết mãi mãi", trái §10.5 (sau #678 `L` được phép
tương đương ở M3) — nếu muốn thì là quyết định chủ kho.
- Ca khoá: `t202`. Đột biến phải làm ca ĐỎ (đã đo trên `wt4.uqqV/h`, mọi đỏ `TinHieuChotCa`): C1+L ⇒ t202 "nối t196 bơm
  {'rc': 0, 'goi': [('GET', …/comments')], 'out': '::group::…"; C1b+L ⇒ t202 "nối t195 bơm {'goi': …, 'out': '::group::…";
  C1c+A3 ⇒ t202 "nối t198 bơm {'rc': 1, 'dang': [], 'goi': [], 'out': '::group::…". Gỡ bốn hàng (= 85124dc) ⇒ ba đột
  biến sống lại (đo ở trên) — tức hàng mới có răng.

## L2 — Chốt AST của `t199` bị vòng qua bằng gán lại helper với wrapper `functools.wraps`

**P3 · MỚI (đường vào của chốt mới lượt 4; cùng họ NA11 lượt 3) · sửa mã test.**

Biểu hiện: `ops/lease_publish_test.py:10784` — `inspect.getsource(_chay_buoc_dang_that)` gọi `inspect.unwrap` trước khi
lấy nguồn, nên sau `_chay_buoc_dang_that = _boc_io(_chay_buoc_dang_that)` (wrapper `@functools.wraps` ghi tệp rồi mới
gọi hàm gốc) nó vẫn trả nguồn của hàm GỐC: `decorator_list` rỗng, hai câu đầu đúng guard/điểm dò ⇒ chốt `:10792` xanh.
Docstring t199 khai *"hàm không có decorator"* — gán lại bằng wrapper là decorator về ngữ nghĩa.

Phép đo: `python -B mut.py C2-wraps-gan-lai t195_,…,t202_` ⇒ 8/8 XANH, và tệp `wt4.uqqV/m/ops/_io_truoc_guard_wraps.txt`
ĐƯỢC GHI trong lúc t199 mô phỏng S2 (`nt` + job chỉ Ubuntu) — thao tác chạy TRƯỚC guard.

**Hint patch** (`HINT.patch`, phần `t199`; đã đo): sau chốt AST,
`f = _chay_buoc_dang_that; if inspect.unwrap(f) is not f or f.__code__.co_name != "_chay_buoc_dang_that": sai.append(…)`.
Ca khoá: `t199`. Đột biến phải ĐỎ: C2 ⇒ t199 "M1: helper bị BỌC/gán lại (`__wrapped__` hoặc `__code__` không phải hàm
gốc)…" (`TinHieuChotCa`, đo trên `wt4.uqqV/h`). Wrapper KHÔNG `wraps` đã bị chốt AST cũ bắt (nguồn trả về là của wrapper).
Rủi ro thực tế thấp (không ai gán lại helper test vô tình) — nên P3, cùng mức NA11 lượt 3.

## L3 — Điều kiện dừng S2 của lease g5 bị kích hoạt: cùng hình dạng finding lượt thứ BA liên tiếp

**P3 · MỚI · hồ sơ/quy trình, không sửa mã.** `LEASE-g5.yaml` `dieu_kien_dung`: *"S2 — … vẫn DỪNG và hỏi nếu cùng một
hình dạng finding lặp lại 3 lượt liên (CLAUDE.md đếm hình dạng)"*. Hình dạng "đường nối helper → consumer đo hẹp hơn lời
khai": lượt 2 (R2-F4/R2-F6, verdict B), lượt 3 (L1a Opus + L1 advisory), lượt 4 (L1 ở trên). Mỗi lượt vá ĐÚNG chỗ được chỉ
và mỗi bản vá CÓ răng ở chỗ nó phủ — đúng `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA`. Họ "thao tác trước guard" là lượt
thứ hai (NA11 lượt 3 → C2 lượt 4).
Hệ quả: executor **không** tự áp HINT.patch như một vòng vá thường; phiên điều phối hỏi chủ kho trước. Câu cần chủ kho
trả lời: tập mối đe doạ "consumer bị viết đè" có dừng ở vectơ quan sát thật (L1 hint) — với giới hạn khai thẳng trong
docstring — hay đòi nhúng đột biến `L` chạy thật vào suite (trái §10.5, cần sửa spec). Kèm: lease g5 hết hạn
`2026-09-30T10:48:00Z` (S3); lượt này đo ~06:50Z.

## L4 — Ghi nhận (không chặn)

**P4 · mới/mang · hồ sơ.**
- Phụ thuộc cài đặt, đều FAIL-CLOSED (đổi thì ĐỎ, không xanh giả): `t202` nhận diện chốt bằng TIỀN TỐ thông điệp
  (`"M2 tập (i)"`, `"M3a: PR"`, `"M4:"`) — sửa câu chữ chốt là phải sửa `t202`; chốt AST ghim nguyên văn guard/điểm dò;
  `t201` ghim `html_url` của gh giả. Chấp nhận được; nên ghi vào docstring để người sửa không ngạc nhiên.
- Trục "actor có thẩm quyền" của tọa độ đọc giá trị KHAI (`mt["GITHUB_ACTOR"]`), không phải giá trị GIAO cho subprocess
  (C3: truyền bản sao env với actor khác ⇒ tọa độ vẫn sạch). Đo: M4 (t198) bắt được ngay (`CHAN [4]`), nên không lọt.
- gh giả không có hợp đồng cho NHẬT KÝ lời gọi (C5: chỉ ghi endpoint `comments` ⇒ 6/6 xanh). Vô hại với `L` hiện tại
  (tín hiệu M2 là GET `comments`); chỉ đáng khoá nếu có đột biến sản phẩm mà tín hiệu nằm ở GET loại số hiệu.
- Mang từ lượt 2–3: nối sổ `BoQuaNen` của #687 — sáu ca t195–t200 đi guard. `t202` KHÔNG đi guard (helper giả) nên trên
  Windows nó chạy thân t195–t198 bằng Python thuần; Windows thật: KHÔNG ĐO ĐƯỢC.
- `C4`: tiền đề "trường khác = `lease_mau()`" không độc lập với `lease_mau()`; đo 7 biến thể trường, không trường nào che `L`.

## Đợt đo 5 — HINT.patch trên bản sao `wt4.uqqV/h` (@85124dc + patch)

- `HINT.patch` (diff áp lên 85124dc; `git -C cay-kho apply --check` ⇒ OK; chỉ `ops/lease_publish_test.py`, `+16/−1`).
  Số dòng thêm so merge-base sau khi áp: `516 4` ≤ 600 (A7(2)); còn 84 dòng tới S4.
- Toàn suite trên `h`: `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, rc=0 (`wt4.uqqV/hint-full-suite.log`).
- ruff F trên bản hint: tập lỗi bằng merge-base ⇒ delta 0; `git diff --check` sạch. Chuỗi `\n` trong literal đo bằng
  `repr()` sau khi ghi: là hai ký tự `\` `n` trong nguồn (không bị giải mã ở tầng công cụ).
- 42 đột biến của đợt 1 chạy lại trên `h` (`hint1.txt`): tập (đột biến, ca, XANH/ĐỎ) **giống hệt** 85124dc
  (`diff dot1_tom.txt hint1_tom.txt` rỗng) — không đột biến cũ nào sống lại; 69 dòng ĐỎ, cả 69 là `TinHieuChotCa`.
- Bốn đột biến sống của L1/L2 trên `h`: C1+L, C1b+L, C1c+A3 ⇒ t202 ĐỎ; C2 ⇒ t199 ĐỎ — đều `TinHieuChotCa`.
- Prototype là GỢI Ý có bằng chứng chạy; không áp vào `cay-kho`. Chịu L3: áp hay không do chủ kho.

## Nhận xét hợp nhất (mục 4 PROMPT) — 85124dc có làm YẾU thứ e55c5e2 đã có không?

Đọc `diff-luot4.patch` và đo: **không thấy chỗ yếu đi**.
- `_toa_do_that`: e55c5e2 dò dấu bằng `re.search` (không neo, không tác giả) → 85124dc `re.match` neo đầu thân + tác giả
  cho MỌI comment cũ; tiền đề e55c5e2 (5 điều kiện gộp) → 85124dc 8 điều kiện có tên + so `lease_mau()`; `issue_loi` tách
  thành trục riêng (trước nằm trong tiền đề) — tương đương về độ phân biệt (NA8 chết ở cả hai cách).
- `_td_m3(la_pr, het_han)` (kỳ vọng dẫn từ tham số) → literal `_TD_M3` + ghim VAI ở t202 — mạnh hơn (F3-2cho, F3-literal chết).
- Chốt AST t199: e55c5e2 tha `import` và không xét decorator → 85124dc dời `import json` xuống sau điểm dò, không tha
  `import`, xét decorator — mạnh hơn (vẫn lọt C2, L2).
- Helper: `cac["55"]["comments"]` → `.get(...)`, `c["body"]` → `str(c.get("body"))`. Đổi một `KeyError/TypeError` vô can
  thành im lặng ở đường ĐỌC. Đã xét hai đường có thể bị che: POST lưu sai khoá/sai kiểu ⇒ t198 (0 POST) và t201 ("comment
  đã lưu phải là dict có id/body/user") vẫn đỏ; tọa độ có "gh phục vụ đúng #55". Không đo được đường nào bị che thêm.
- `_lech_m4` giữ chốt nhật ký lời gọi của e55c5e2; t202 giữ mọi hàng M2/M3/M4 của e55c5e2 và thêm `rc=-1` M3, từng vị trí tiền tố.

## Bảng trạng thái mọi finding cũ trên 85124dc

| finding | nguồn | trạng thái | bằng chứng (đợt) |
|---|---|---|---|
| R1-F1 guard khi dò tắt | lượt 1 | ĐÃ ĐÓNG | S4-probe-only ⇒ t199 "S2 điểm dò tắt: nhận 'IO'" (2) |
| R1-F2 giảm miền M2/M3 | lượt 1 | ĐÃ ĐÓNG | N1–N7, NA1–NA5 chết (2, 3) |
| R1-F3 chốt mã thoát M3 | lượt 1 | ĐÃ ĐÓNG | ADV-L5, F4-rc chết (3) |
| R1-F4 mặc định đọc bản neo | lượt 1 | ĐÃ ĐÓNG | S5 ⇒ t200 (3) |
| R1-F5 gh đánh chỉ số lần gọi | lượt 1 | ĐÃ ĐÓNG | S1b ⇒ t201 (3) |
| R1-F6 t70 kiểm kê | lượt 1 | ĐÃ ĐÓNG (không đo lại; t70 không đổi từ 1290ebb) | (3) |
| R1-F7 tiền tố POST M4 | lượt 1 | ĐÃ ĐÓNG | N8, NA7, NA7b, F6 chết (2, 3) |
| R1-F8 docstring 12/14 | lượt 1 | ĐÃ ĐÓNG | docstring t195 (b) giữ phạm vi 12/14 |
| L1-E1…E13 (N1–N13) | lượt 2 A | ĐÃ ĐÓNG | bảng A11 (2) |
| L2 quyền vượt trần A7 | lượt 2 A | ĐÃ ĐÓNG (hồ sơ) | spec r8 Q19 "≤ 600", lease g5 S4 |
| L3 nối sổ #687 | lượt 2 A | MỞ — P4 ghi nhận | L4 |
| R2-F1, R2-F2, R2-F5, R2-F7, R2-F8 | lượt 2 B | ĐÃ ĐÓNG | N1, N7/N4, N10, (R2-F7: A9 thông điệp "lỗi vô can" không đổi), N1–N3 (2) |
| R2-F3 M3a→M3b | lượt 2 B | ĐÃ ĐÓNG | F3-1chỗ, F3-2chỗ, F3-literal ⇒ t196/t202 (3) |
| R2-F4 consumer rc/out | lượt 2 B | ĐÓNG cho viết đè không điều kiện; đường có điều kiện MỞ | F4-rc, F4-rc-va-out chết; C1 sống (L1) |
| R2-F6 consumer tiền tố t198 | lượt 2 B | ĐÓNG cho viết đè không điều kiện; C1c MỞ | F6 chết; C1c sống (L1) |
| lượt 3 L1 (a) consumer, NA6 | lượt 3 Opus | MỘT PHẦN | F4*, F6*, NA6/NA6b chết; C1/C1b/C1c sống (L1) |
| lượt 3 L1 (b) tọa độ NA1–NA5, NA8 | lượt 3 Opus | ĐÃ ĐÓNG | (3) |
| lượt 3 L2 NA7 | lượt 3 Opus | ĐÃ ĐÓNG | vòng từng vị trí tiền tố (3) |
| lượt 3 L3 NA11 I/O trước guard | lượt 3 Opus | ĐÓNG cho câu lệnh chèn; đường gán lại wrapper MỞ | NA11 chết; C2 sống (L2) |
| lượt 3 L4 nối sổ #687 | lượt 3 Opus | MỞ — P4 | L4 |
| advisory L1 (R2-F4/F6 + t195) | lượt 3 adv | MỘT PHẦN | như lượt 3 L1 (a) |
| advisory L2 (R2-F3 vá hờ) | lượt 3 adv | ĐÃ ĐÓNG | F3-2chỗ ⇒ t202 VAI (3) |
| advisory L3 (dấu bot/tiền đề) | lượt 3 adv | ĐÃ ĐÓNG | NA1–NA5 (3) |
| advisory L4 (gh không-JSON) | lượt 3 adv | ĐÃ ĐÓNG | ADV-L4 ⇒ t201 "phải in JSON hợp lệ" (3) |
| advisory L5 (I/O trước guard; rc âm M3; `issue_loi`) | lượt 3 adv | ĐÓNG (rc âm, `issue_loi` ở t201); I/O trước guard: xem L2 | (3) |

## Bảng lớp

| lớp | mức | mới / mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 — `t202` chỉ đo viết đè không điều kiện; viết đè theo đặc điểm lượt chạy thật lọt (C1/C1b/C1c: mất A2, A1, A3) | P3 | mang hình dạng R2-F4/F6 → lượt 3 L1a; đường vào mới | mã test (write set) + thu hẹp docstring |
| L2 — chốt AST `t199` lọt gán lại bằng wrapper `functools.wraps` (C2) | P3 | mới (họ NA11) | mã test (write set) |
| L3 — điều kiện dừng S2 của lease g5: cùng hình dạng lượt thứ 3 liên tiếp; lease hết hạn 10:48Z | P3 | mới | hồ sơ/quy trình — hỏi chủ kho trước khi áp HINT |
| L4 — ghi nhận: phụ thuộc fail-closed, actor khai≠giao, nhật ký gh không hợp đồng, nối sổ #687 | P4 | mới + mang | hồ sơ |

Tổng: **0 P1 / 0 P2 / 3 P3 / 1 P4**. A1–A11 của r8 ĐẠT theo đúng lệnh đo của chúng (đợt 1–2); L1/L2 là đường vào mới
của chính các chốt lượt 4; L3 là điều kiện dừng của lease.

Worktree tạm còn đăng ký trong `cay-kho/.git/worktrees/` (phiên chính dọn): `wt4.uqqV/k`, `wt4.uqqV/m`, `wt4.uqqV/e`,
`wt4.uqqV/h` — `git -C cay-kho worktree remove --force <đường>`. `cay-kho` không bị sửa (HEAD 85124dc, `git status --short` rỗng).
Lượt này không chạy lệnh `git config` nào; lúc kết thúc `cay-kho/.git/config` có `core.abbrev=7` (local) — KHÔNG do lượt
này ghi, nguồn gốc KHÔNG ĐO ĐƯỢC từ đây; phiên chính kiểm nếu cần.

VERDICT: CHANGES_REQUIRED
