# Review MÃ lượt 6 — PR #689 / packet #677 (DOT-BIEN-L-BIEN-CONG-KHAI)

- reviewer: **Claude Opus 5.5** (subagent). Effort "max" là TỰ KHAI trong chỉ thị — KHÔNG đặt được, KHÔNG ĐO ĐƯỢC.
- nhãn assurance: **`advisory_review`** (reviewer cùng họ Claude với executor)
- reviewed_sha: `4dc226bc7d256472fa5354089825a342835d2ccc` (đo: `git -C cay-kho rev-parse HEAD`); cha `66ec303` (lượt 5 PASS)
- merge-base: `c16bec639efa0077def4916c25c3e0c17f68dcaa` (đo `git merge-base HEAD c16bec6…` ⇒ chính nó); baseline A8 `89fc4fac…`
- spec r8 sha256 đo lại: `4dfbfd69e161d55aa28f2685741cdcf11fcd5171438081e9eb63815c69bb4094` — khớp PROMPT (`4dfbfd69…4094`)
- `diff-luot6.patch` sha256 `56a2c6ef…5f79` = sha256 của `git diff 66ec303..4dc226b` (byte-exact, đo) — chỉ `t154`, `+20/−11`.
- Môi trường: Linux, python3.11.15 (mặc định), 3.12 và 3.13 CÓ mặt; PyYAML 6.0.1; ruff 0.15.8. Windows thật: KHÔNG ĐO ĐƯỢC.
- Bắt đầu đo 09:18Z 30-09 (`date -u`); hạn cứng 10:15Z; lease g5 hết hạn `2026-09-30T10:48:00Z`.

Nhật ký tăng dần bên dưới.

## Đợt đo 1 — nghiệm thu tĩnh (A7, A8, ruff F) trên 4dc226b — 09:26Z

| mục | kết quả | phép đo |
|---|---|---|
| A7(1) | ĐẠT | `git diff --name-only c16bec6...4dc226b` ⇒ đúng `ops/lease_publish_test.py` |
| A7(2) | ĐẠT, **còn 4 dòng** | `git diff --numstat c16bec6...4dc226b` ⇒ `596 15` (khớp lời khai executor +596/−15); lượt 6 `66ec303..4dc226b` ⇒ `20 11` |
| A8 | ĐẠT | `a8.py` (cắt AST kèm decorator) `_chay_buoc_dang` + mọi `t51`–`t68` (kể cả `t55a/t55b`) ở `89fc4fa` vs `4dc226b` ⇒ `so khoi 18 18 ten bang True`, `lech []` |
| ruff F | delta 0 | ruff 0.15.8 `--select F --no-cache` trên `git show <rev>:ops/lease_publish_test.py`: c16bec6 = 89fc4fa = 66ec303 = 4dc226b = 9 lỗi (7×F401, 2×F541); `diff` tập (mã, thông điệp) c16bec6 vs 4dc226b rỗng |
| `git diff --check c16bec6...4dc226b` | rc=0 | |

Worktree tạm (detached, tạo trong MỘT lệnh, cùng bước): `wt6.OKH3/{full,moi,moi_e1}@4dc226b`, `wt6.OKH3/{cu,cu_e1}@66ec303`.
Toàn suite python3.12 trên `full` chạy nền từ 09:25:42Z (kết quả ở đợt đo sau).

## Hướng 1 — chẩn đoán có ĐÚNG không (log cổng + mã) — 09:32Z

**Kết luận: ĐÚNG.** `int('')` ở lượt con [A] của t125 trên 66ec303 đến từ ĐÚNG đường E1 (fixture `t63_`/`t66_`), do cháu
ghi tệp PID không nguyên tử. Bốn phép đo độc lập:

1. **Loại trừ theo mã (66ec303).** Trong đồ thị gọi của `t154` chỉ có MỘT `int(...)` không được bọc:
   E1 `pid = int(pid_tep.read_text(encoding="utf-8"))` (không `strip`) sau vòng chờ CHỈ đợi `exists()`. `don_chau` cũ
   nuốt `(OSError, ValueError)`; mọi `int()` của launcher mà `_giet_ca_cay`/`_khoa_danh_tinh`/`_giet_cay`/`_chup_cay`/
   `_thanh_vien_nhom`/`_con_song` dùng đều nằm trong `except (OSError, ValueError, IndexError)` (`.claude/dev/launcher.py:350-464,
   :467-551, :629-661`). Thông điệp `invalid literal for int() with base 10: ''` khớp đúng `int('')` trên tệp rỗng.
2. **Hồ sơ thời gian của log cổng.** `cong-tai-cho-66ec303.log:1035-1037`: [A] vào t154 08:16:32Z, ra `2.443s DO`. Chiều 1
   và chiều 2 mỗi chiều có `con_dap(cho=1.0)` ⇒ ≥ 2,0 s trước khi tới E1, nên 2,443 s đặt cú chết ở đầu E1. [B] (song song,
   `4.953s QUA`) và lượt đứng riêng (`:1347`, `4.919s QUA`) xanh ⇒ phụ thuộc thời điểm, không phải lỗi logic.
3. **Cửa sổ "tệp CÓ mà RỖNG" có thật ở tần suất tự nhiên** (không chèn trễ). `wt6.OKH3/race/race.py` chạy ĐÚNG mã cháu
   trích bằng AST từ `launcher_test.py` (như t154), đọc theo ĐÚNG nhịp mã cũ (chờ `exists()` 0,05 s rồi `read_text`):
   tải nhẹ ⇒ `t63_ RONG=0/150`, `t66_ RONG=0/150`; **tải CPU (8 vòng bận / 4 lõi + suite nền) ⇒ `t63_ RONG=4/300`,
   `t66_ RONG=4/300`** (≈1,3 % mỗi lần đọc; E1 đọc hai fixture). Nhịp đọc chặt (bận) ⇒ `RONG=138/150`, `141/150` — cửa sổ
   giữa `open('w')` (O_TRUNC tạo tệp) và lúc đóng/xả ở cuối câu lệnh là quan sát được. Lời khai executor "không tái hiện được
   ở tần suất tự nhiên" chỉ đúng cho CA t154 trọn vẹn: 96 lượt `--chi-ca=t154_` trên 66ec303 dưới tải ⇒ 96/96 QUA (xem "Chưa đo được").
4. **Chèn trễ tái tạo ĐÚNG chữ ký.** Cháu E1 `open → flush → sleep 1.0 → write` (bản sao `cu_e1`) ⇒ `01_E1tre_goc | rc=1 |
   2.820s DO | ValueError: invalid literal for int() with base 10: ''` — cùng lớp, cùng thông điệp, cùng mốc ~2,4–2,8 s.

**Còn đường đọc không nguyên tử nào khác trong tệp?** KHÔNG (đo bằng đọc + grep `int(.*read_text|st_size|exists()` và mọi vòng
`time.sleep(`): ngoài t154 chỉ có `_theo_duoi_va_in` (`:4527-4544`) đọc tệp đang được ghi, và nó đọc NHỊ PHÂN, giữ phần dòng
dở trong `du` tới dấu `\n` — nguyên tử theo dòng do thiết kế; `t125.doc` chỉ đọc `A/B.out` SAU `p.wait()`. Nhịp tim `nhip`
của t154 đọc bằng `st_size` (không parse), tệp chỉ lớn dần ⇒ không có trạng thái trung gian sai.
Ngoài tệp (NGOÀI write set, ghi nhận): `.claude/dev/launcher_test.py:1288-1293, :1348-1353, :1401-1406` (t63/t67/t66) có
đúng mẫu `exists()` rồi `int(read_text().strip())`; ở đó cửa sổ hẹp hơn vì `chay(...)` đồng bộ đã chạy tới hạn chót trước khi đọc.

## Hướng 2 — bản vá có đúng + có răng không (chèn lỗi + đột biến trên BẢN SAO) — 09:33Z

Giàn: `wt6.OKH3/race/sinh.py` sinh bản sao (mọi phép thay phải khớp ĐÚNG số lần kỳ vọng, không thì dừng); `mot.sh` chạy
`python3 -B <tệp> --chi-ca=t154_` với `timeout`, ghi rc, dòng `<<< ra`, dòng `!!! do`. Chèn E1 vào `.claude/dev/launcher_test.py`
của worktree `cu_e1`/`moi_e1` (4 chỗ chuỗi cháu, t154 đọc t63_/t66_); chèn E2 vào `_MA_CHAU_T154` của bản sao `ops/_inj_*.py`.
Lệnh: `xargs -P 6 -L 1 ./mot.sh < matran.txt` (09:29:42Z→09:30:55Z) ⇒ `matran.out`. (Từ lượt HINT/K/`'0'` về sau `mot.sh` chạy
con dưới `setsid -w` để cú `kill(0)` không lan sang giàn; 18 ô dưới đây chạy TRƯỚC thay đổi ấy, không ô nào chạm `kill(0)`.)

| # | kịch bản | 66ec303 (gốc) | 4dc226b (vá) |
|---|---|---|---|
| 01/02 | E1 trễ 1 s giữa `open('w')` và ghi | **ĐỎ** `2.820s` `ValueError: invalid literal for int() with base 10: ''` | **QUA** `7.465s` |
| 04/05 | E2 trễ 1 s (cháu t154) | QUA `7.226s` | QUA `7.197s` |
| 06/07 | E2 chiều 1 ghi rác `'x'` mãi | QUA `5.475s` (nuốt lỗi, không dọn cháu) | **ĐỎ** `15.038s` "fixture hỏng: cháu chiều 1: tệp PID không thành số nguyên sau 15.0 s (đọc cuối: 'x')" |
| 08/09 | E2 chiều 2 ghi rác `'x'` mãi | QUA `5.150s` | **ĐỎ** `16.082s` "…cháu chiều 2: … (đọc cuối: 'x')" |
| 10/11 | E2 chiều 1 RỖNG mãi | QUA `5.105s` | **ĐỎ** `15.055s` "…cháu chiều 1: … (đọc cuối: '')" |
| 13/12 | E2 chiều 1 ghi byte KHÔNG phải UTF-8 (`b'\xff'`) | QUA `5.090s` | **ĐỎ** `0.060s` `UnicodeDecodeError` — KHÔNG qua `bang`, xem L2 |

Đột biến trên 4dc226b (mỗi cái gỡ MỘT chốt):

| # | đột biến | kịch bản | kết quả | so với bản vá |
|---|---|---|---|---|
| 03 | **M_E1** E1 về mã cũ (`exists()` + `int(read_text())`) | E1 trễ | **ĐỎ** `2.713s` `ValueError … ''` | bản vá QUA ⇒ phát hiện — nhưng bằng ngoại lệ VÔ CAN (chữ ký lỗi gốc), không bằng assertion của ca |
| 14 | **M_E2a** bỏ `so1 = doc_pid(...)`, đọc ở `finally` + nuốt lỗi (hành vi cũ) | chiều 1 rác | **QUA** `5.113s` | bản vá ĐỎ `bang` ⇒ chốt có răng (bỏ sót DỌN im lặng ↔ ĐỎ có lý do; verdict nhịp tim của mutant vẫn đúng — L3) |
| 15 | **M_E2b** như trên cho chiều 2 | chiều 2 rác | **QUA** `5.158s` | bản vá ĐỎ `bang` ⇒ có răng |
| 16 | **M_han** `bang(True, …)` thay cho hạn | chiều 1 rác | **TREO** rc=124 tại 60 s, không dòng `ra` | bản vá ĐỎ ở 15 s ⇒ hạn có răng |
| 17 | **M_re** `if nd: return int(nd)` (bỏ kiểm số nguyên) | chiều 1 rác | ĐỎ `0.062s` `ValueError … 'x'` | bản vá ĐỎ bằng `bang` ⇒ đổi LỚP lỗi (phát hiện qua lớp ngoại lệ) |
| 18 | M_E2a | E2 trễ | QUA `7.140s` | = bản vá: trễ E2 KHÔNG phân biệt được chốt E2 (đọc cũ ở cuối vốn đã an toàn) |

Kết luận hướng 2:
- Bản vá ĐÚNG: gốc đỏ / vá xanh trên chữ ký thật (01/02); rác/rỗng mãi ⇒ ĐỎ bằng `bang` có nhãn đường vào trong ~15 s, không
  treo, không xanh giả (07/09/11) — ngoại lệ: byte không phải UTF-8 (12, L2).
- CÓ RĂNG dưới chèn lỗi cho cả năm chốt (E1, E2a, E2b, hạn, regex). Nhưng: (a) E2a/E2b KHÔNG vá một verdict sai — gốc chỉ bỏ
  sót việc DỌN cháu (cháu tự huỷ sau 30 s), verdict đo bằng nhịp tim không phụ thuộc tệp PID (04/06/08/10/13 đều QUA đúng
  nghĩa). Lời khai commit "E2a/E2b, trước đây nuốt lỗi ⇒ **xanh giả**" rộng hơn phép đo (L3). (b) Mọi chiếc răng chỉ sống
  NGOÀI suite: không ca nào của suite khoá `doc_pid` (L1).
- Hạn 15 s không làm chậm/treo: `lap.sh` 36 lượt mỗi vế dưới tải (4 vòng bận + suite nền + 6 lượt song song): 66ec303
  **36/36 QUA, tb 6,412 s, max 7,489 s**; 4dc226b **36/36 QUA, tb 6,405 s, max 7,551 s**. Đường hỏng tối đa +15 s rồi ĐỎ (ca
  dừng ở `bang` đầu tiên); `AB_HAN_GIAY` = 950 s (`:58-59`) còn dư. Trong toàn suite 3.12 (đang chạy, dưới cùng tải ấy):
  `t125 227.204s QUA`, `t154 5.237s QUA`.

## Hướng 3 — hồi quy (toàn suite, mẫu đột biến lượt 4–5, A7/A8/ruff) — 09:35Z

- **Toàn suite python3.12** trên `wt6.OKH3/full` @4dc226b (sạch, không chèn): `env -u GITHUB_ACTOR python3.12 -B
  ops/lease_publish_test.py` ⇒ `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, `rc=0`, `real 7m2.206s` (09:25:42Z→
  09:32:44Z); `grep -c '^@ca'` = 195 ⇒ N/N với N = số `@ca` tĩnh; 0 dòng `ĐỎ`/`BỎ QUA`/`!!! do`. Hai lượt con của t125:
  `[A] 195/195 … bỏ qua=0`, `[B] 195/195 … bỏ qua=0`; `t125 227.204s QUA`, `t154 5.237s QUA`. Lượt này chạy CÙNG LÚC với
  giàn đo hướng 1–2 (vòng bận, 6 lượt t154 song song) ⇒ là phép đo dưới tải, không phải máy rỗi.
- **Mẫu đột biến lượt 4–5** trên 4dc226b, mỗi (đột biến, ca) MỘT tiến trình (`wt6.OKH3/hq/chay_ca.py`: nạp tệp theo đường
  dẫn, `sys.path[0]` = `ops/` như khi chạy script, in lớp ngoại lệ + `isinstance(e, TinHieuChotCa)`). Lượt đầu của giàn ĐỎ cả
  vế nền vì thiếu `sys.path` (`No module named 'bash_nen'`) — lỗi GIÀN, bắt được nhờ chạy vế `nen`, đã sửa rồi chạy lại cả 32 ô:

| đột biến | định nghĩa (tái dựng từ spec Phụ lục A / lượt 4–5) | ô ĐỎ (mọi ô `TinHieuChotCa`, `chot=True`) | ô còn lại |
|---|---|---|---|
| nền | 4dc226b sạch | — | 8/8 QUA |
| `L` | gỡ `DONG_L` (2 dòng chốt `lease_id`) khỏi `ops/lease_publish.py` của worktree `mL` | t195 "M2 tập (i) … lệch: null/Issue/trống: rc=1 goi=[('GET', …/comments)]", t196 "M3a … rc=0 POST=0 bỏ_qua=True", t197 "M3b …" | 5 QUA |
| `C1+L` | t196+t197: `if any(g[1].endswith("/comments") …): r = {**r,"rc":1,"out":""}` trên `L` | t195 (do `L`), **t202** "nối t196 bơm nền: consumer phải trao NGUYÊN VẸN …" | t196/t197 QUA (đúng thiết kế C1) |
| `C2` | `_chay_buoc_dang_that = _boc_io(...)` bọc `functools.wraps`, ghi tệp TRƯỚC khi gọi | **t199** "A9 guard nền: M1: helper mà consumer gọi KHÔNG phải hàm biên dịch từ def duy nhất …" | 7 QUA; tệp `moi/ops/_io_truoc_guard_wraps.txt` được ghi (09:34:51) ⇒ I/O của đột biến CHẠY THẬT |

  Khớp lượt 5 (`L` ⇒ t195/t196/t197; C1+L ⇒ t202; C2 ⇒ t199) và bảng executor (`C1+L→t195,t202`). Diff lượt 6 chỉ chạm
  `t154` (`:6480-6578`), không chạm vùng các ca này — kết quả khớp là điều phải có, đã đo chứ không suy.
- **Răng GỐC của `t154` không bị bản vá làm cùn** (ba đột biến docstring `:6456-6458` tự khai, bản sao `ops/_k_*.py`,
  09:39:38Z→09:39:43Z, `matran_k.out`), cùng thông điệp `bang` ở cả hai vế:
  K1 `_giet_ca_cay` → `p.kill()` trần ⇒ 66ec303 `2.120s`, 4dc226b `2.107s` ĐỎ "`_giet_ca_cay` KHÔNG thu hồi được CHÁU: nhịp còn
  tăng 1->21"; K2 bỏ `start_new_session` ⇒ `0.060s` / `0.054s` ĐỎ "con phải là LÃNH ĐẠO một nhóm RIÊNG …"; K3 killpg vô điều
  kiện ⇒ `2.333s` / `2.364s` ĐỎ "không được giết nhóm khi cùng nhóm runner hoặc con không phải trưởng nhóm".
- A7 (596 ≤ 600), A8 (18 khối byte-exact), ruff F delta 0: xem đợt đo 1.

## L1 — Bản vá race không có ca khoá trong suite: mọi chiếc răng chỉ sống NGOÀI suite

**P4 · mới · hồ sơ (docstring, trong trần) — đóng bằng mã cần chủ kho nới trần A7(2).**

Biểu hiện: `ops/lease_publish_test.py:6483-6492` (`doc_pid`, hàm lồng trong `t154`) và ba lời gọi `:6510`, `:6531`, `:6578`.
Không ca nào của suite đỏ khi gỡ một chốt: `lap.sh` 36 lượt `--chi-ca=t154_` trên 66ec303 (tức M_E1+M_E2a+M_E2b cùng lúc)
dưới tải ⇒ **36/36 QUA**; cửa sổ tự nhiên chỉ ≈1,3 %/lần đọc dưới tải nặng (hướng 1). Răng chỉ đo được bằng chèn lỗi trên bản
sao (hướng 2: 01–18), và bằng chứng của executor ("gốc lệch 5/6, bản vá 0/6; đột biến M1–M5 đều bị bắt") chỉ nằm trong
THÔNG ĐIỆP COMMIT — đúng chỗ CLAUDE.md gọi là "nơi các ca đi chết". Thêm: M_E1 dưới chèn trễ đỏ bằng `ValueError` (chữ ký lỗi
gốc), KHÔNG bằng assertion của ca — theo luật "đột biến chỉ tính giết khi ca đích đỏ bằng assertion của chính nó" thì chốt E1
KHÔNG có phép giết bằng assertion nào, kể cả ngoài suite; đó là bản chất của vá độ bền ("đừng nổ"), nhưng phải khai ra.
Vì sao P4, không P3: vá nằm ngoài mục tiêu spec (chủ kho cho vá trong PR; A5/A11 của spec chỉ áp cho A1–A4/N1–N13); gỡ chốt
chỉ tái tạo một cú ĐỎ hiếm (fail-closed, `t125` báo `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN`), không tạo xanh giả; và A7(2) còn **4 dòng**
(596/600) nên một ca khoá hành vi (chèn trễ vào mã cháu trích từ fixture + tự kiểm `doc_pid`; ƯỚC LƯỢNG ≥ 12 dòng, CHƯA dựng, CHƯA đo) chạm S4 "DỪNG và hỏi".

Phép đo tái lập: `wt6.OKH3/race/lap.sh <wt> <nhãn> 12` ×3 mỗi vế, dưới 4 vòng `python3 -c "while True: pass"`; `matran.out`.

**Hint patch** (`HINT.patch`, hunk docstring `doc_pid`, +1 dòng ⇒ A7(2) 597): thêm câu GIỚI HẠN "chưa ca nào khoá hàm này; răng
chỉ đo bằng chèn trễ/rác trên BẢN SAO (ngoài suite)". Không ca khoá (docstring). Nếu chủ kho nới trần: nhấc `doc_pid` ra mức
module, thêm ca `t203_` (a) tệp rỗng + tiến trình con ghi `42` sau 0,3 s ⇒ trả 42; (b) `x` mãi, `han=0.3` ⇒ `AssertionError` có
"sau 0.3 s" trong ≤ 5 s; (c) chạy fixture E1 với mã cháu được bọc trễ ghi ⇒ QUA. Đột biến phải làm ca ấy ĐỎ: M_E1 (c), M_re
(b, lớp ngoại lệ), M_han (b, cần hạn ngoài bằng luồng), bỏ vòng chờ (a).

## L2 — Hợp đồng đọc của `doc_pid` hẹp hơn lời khai: byte lạ nổ ngay; "0" qua kiểm và thành `os.kill(0, SIGKILL)`

**P4 · (a) mới, (b) mang từ `don_chau` cũ · sửa mã 0 dòng net (trong write set).**

Biểu hiện: `ops/lease_publish_test.py:6488` `tep.read_text(encoding="utf-8")` chỉ bắt `OSError`; `:6490`
`re.fullmatch(r"[0-9]+", nd)`; `:6500` `os.kill(so, SIGKILL)`. Docstring `:6485` khai "hết hạn ⇒ `bang`, không nuốt/treo".
- (a) Tệp PID chứa byte không phải UTF-8 (`b'\xff'`) ⇒ **ĐỎ `0.060s` `UnicodeDecodeError`** (kịch bản 12) — đỏ tức thì, không chờ,
  không qua `bang`. Fail-closed (đỏ, không treo, không xanh), nhưng lệch lời khai. Nhà ghi thật chỉ ghi chữ số ASCII ⇒ lý thuyết.
- (b) Tệp PID chứa `"0"` ⇒ qua kiểm "số nguyên" ⇒ `don_chau(0)` ⇒ `os.kill(0, SIGKILL)` = **giết cả nhóm tiến trình của runner**.
  Đo trong phiên `setsid` cô lập (`_inj_e2_so0_1.py`, chiều 1 ghi `'0'`): **66ec303 rc=137 và 4dc226b rc=137**, log dừng ở
  `>>> vao t154…`, không dòng `<<< ra`, không dòng tổng kết, không lý do: mã thoát khác 0 nên bước vẫn ĐỎ, nhưng MẤT chẩn đoán;
  runner nào chung nhóm với vỏ shell của bước thì cú giết lan cả vỏ (SUY từ ngữ nghĩa `kill(0)`, CHƯA đo ngoài `setsid`).
  Mang từ `don_chau` cũ (`int("0")`
  cũng qua), nhưng lượt này dựng chính cổng kiểm định dạng cho đích giết mà vẫn để lọt. Không nhà ghi thật nào ghi `0` (PID ≥ 2)
  ⇒ tiềm ẩn. CLAUDE.md đã trả giá đúng họ này ("`killpg(<số nhỏ>)` … nhóm của chính vỏ shell gọi ta").

**Hint patch** (`HINT.patch`, hai dòng thay thế, 0 dòng net): `tep.read_bytes().decode("utf-8", "replace")` và
`re.fullmatch(r"[1-9][0-9]*", nd)`. Ca khoá (đo trên `wt6.OKH3/h` = 4dc226b + HINT): chiều 1 ghi `'0'` ⇒ **ĐỎ `15.038s`**
"fixture hỏng: cháu chiều 1: tệp PID không thành số nguyên sau 15.0 s (đọc cuối: '0')"; chiều 1 ghi `b'\xff'` ⇒ **ĐỎ `15.040s`**
"… (đọc cuối: '�')"; `'x'` ⇒ ĐỎ `15.044s` như cũ; E1 trễ ⇒ QUA `7.089s`. Đột biến phải làm ca ấy ĐỎ-SAI: trả regex về `[0-9]+` ⇒
runner rc=137 (đo trên 4dc226b); trả `read_text` ⇒ `UnicodeDecodeError` 0,060 s (đo, kịch bản 12). Hai ca này cũng chỉ sống
ngoài suite (L1).

Toàn suite python3.12 trên `wt6.OKH3/h` (4dc226b + HINT.patch, sạch): `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`,
`rc=0`, `real 6m35.200s` (09:37:10Z→09:43:46Z), 0 dòng `ĐỎ`/`BỎ QUA`; `t125 197.846s QUA` ([A]/[B] 195/195), `t154 5.087s QUA`.
HINT.patch: `git -C cay-kho apply --check` OK; chỉ `ops/lease_publish_test.py` `+4/−3`; A7(2) sau áp `597 15` ≤ 600; ruff F
delta 0 so c16bec6; `git diff --check` sạch; dòng thêm dài nhất 113 ký tự.

## L3 — Lời khai commit "E2a/E2b, trước đây nuốt lỗi ⇒ xanh giả" rộng hơn phép đo

**P4 · mới · hồ sơ (thông điệp commit / mô tả PR — không nằm trong tệp).**

Biểu hiện: thông điệp commit 4dc226b ("don_chau chiều 1/2 (E2a/E2b, trước đây nuốt lỗi ⇒ xanh giả)"). Đo (hướng 2): trên 66ec303,
chiều 1/2 với tệp PID rác/rỗng/không-UTF-8 mãi ⇒ QUA (06/08/10/13) — và QUA ĐÚNG: verdict hai chiều đo bằng NHỊP TIM (`nhip`),
không đọc tệp PID; thứ bị nuốt chỉ là việc DỌN cháu (cháu tự huỷ sau 30 s). Trễ E2 1 s ⇒ gốc QUA (04), vì gốc đọc tệp PID ở
`finally`, SAU khi đã thấy nhịp tim — mà cháu ghi PID TRƯỚC khi đập nhịp. Tức E2a/E2b không phải lỗi verdict và không phải
nguyên nhân của 194/195; bản vá đổi "dọn im lặng thất bại" thành "ĐỎ có lý do" (có răng, 14/15), không sửa một xanh giả.
Kèm: khi `doc_pid` hết hạn, `don_chau(None)` vẫn không dọn — cháu chiều 1/2 sống tới 30 s, cháu E1 (`sleep 60`) chỉ bị `p.kill()`
giết MẸ; y hệt mã cũ, chỉ trên đường hỏng.

**Hint patch**: không sửa mã; khi viết lại mô tả PR/bàn giao, đổi thành "E2a/E2b trước đây NUỐT lỗi đọc ⇒ bỏ sót DỌN cháu
im lặng (verdict không đổi); nay ĐỎ có lý do". Không ca khoá.

## L4 — Ghi nhận mang từ lượt 5 (chưa áp, không chặn)

**P4 · mang · hồ sơ + mã test 2 dòng (đã đề xuất ở lượt 5).** `luot5/HINT.patch` vẫn `git apply --check` sạch trên 4dc226b (rc=0):
L1 lượt 5 (câu giới hạn dò giàn `t202`, `:10899`), L2 lượt 5 (`t199` chưa khai "I/O trong hàm guard"), L3 lượt 5 (`def q(*a)`
`:10962` ⇒ H2 đỏ `TypeError`), L4 lượt 5 (nối sổ `BoQuaNen` #687, trục actor, hợp đồng nhật ký `gh`). Diff lượt 6 không chạm các
vùng ấy nên trạng thái đo ở lượt 5 giữ nguyên; lượt này không đo lại ngoài C1+L/C2 (hướng 3).

## Chưa đo được (nói thẳng)

- Windows thật: KHÔNG ĐO ĐƯỢC (không có máy; lease cấm CI). E2a/E2b chạy trên mọi nền; trên Windows `open()` của Python mở
  chia sẻ đọc nên đọc song song không dính khoá — suy từ tài liệu, chưa đo; `except OSError` vẫn quy mọi lỗi mở về "chờ tiếp".
- Tái hiện TỰ NHIÊN cú đỏ trọn vẹn của CA t154 trên 66ec303: **0/96** lượt (36 `lap.sh` dưới 4 vòng bận + 60 `burst.sh`
  09:43:54Z→09:46:24Z dưới 8 vòng bận, 6 worker; tb 5,953 s, max 6,465 s, 60/60 QUA). Cơ chế thì đo được ở mức lần đọc
  (8/600 dưới tải nặng hơn — lúc ấy có cả t125 nền). Tần suất trên runner CI: KHÔNG ĐO ĐƯỢC. Sau mọi lượt: `ps` không còn
  tiến trình cháu/`me.py` nào sót.
- Model/effort thực chạy của executor và reviewer: KHÔNG ĐO ĐƯỢC từ trong phiên.

## Bảng trạng thái các finding cũ trên 4dc226b

| finding | nguồn | trạng thái | bằng chứng lượt 6 |
|---|---|---|---|
| R1-F1…F8 | lượt 1 | ĐÃ ĐÓNG (giữ) | diff lượt 6 chỉ chạm `t154`; toàn suite 195/195 |
| L1-E1…E13 (N1–N13), L2 trần A7 | lượt 2A | ĐÃ ĐÓNG (giữ); A7(2) nay 596 ≤ 600 | đợt 1; `L` ⇒ t195/t196/t197 `TinHieuChotCa` (hướng 3) |
| L3 nối sổ #687 | lượt 2A | MỞ — P4 (mang) | L4 |
| R2-F1…F8 | lượt 2B | ĐÃ ĐÓNG (giữ) | toàn suite; `L`, C1+L |
| lượt 3 L1–L3, advisory L1–L5 | lượt 3 | ĐÃ ĐÓNG (giữ); callee guard P4 | C2 ⇒ t199 (hướng 3) |
| lượt 3 L4 nối sổ #687 | lượt 3 | MỞ — P4 (mang) | L4 |
| lượt 4 L1 (C1/C1b/C1c) | lượt 4 | ĐÃ ĐÓNG (giữ) | C1+L ⇒ t202 `TinHieuChotCa` "nối t196 bơm nền…" |
| lượt 4 L2 (C2 wraps) | lượt 4 | ĐÃ ĐÓNG (giữ) | C2 ⇒ t199 `TinHieuChotCa`, I/O đột biến chạy thật |
| lượt 4 L4 ghi nhận | lượt 4 | MANG — P4 | L4 |
| lượt 5 L1–L4 (P4) | lượt 5 | MANG — P4, CHƯA áp | `luot5/HINT.patch` `apply --check` rc=0 trên 4dc226b |
| cổng tại chỗ 66ec303 194/195 (`t154` [A] `int('')`) | lý do lượt 6 | **ĐÃ ĐÓNG** cho chữ ký đã thấy | hướng 1 (chẩn đoán đúng) + hướng 2 (01/02: gốc ĐỎ, vá QUA) + toàn suite 195/195 dưới tải |

## Bảng lớp

| lớp | mức | mới / mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 — vá race không có ca khoá trong suite; răng (và M_E1 chỉ đỏ bằng `ValueError`) chỉ sống ngoài suite | P4 | mới | hồ sơ (docstring, +1 dòng); mã chỉ khi chủ kho nới trần A7(2) |
| L2 — `doc_pid`: byte không-UTF-8 ⇒ `UnicodeDecodeError` tức thì; `"0"` qua kiểm ⇒ `os.kill(0, SIGKILL)` giết nhóm runner (rc=137, không dòng tổng kết) | P4 | (a) mới · (b) mang từ `don_chau` cũ | mã test (2 dòng thay, 0 net) |
| L3 — lời khai commit "E2a/E2b … ⇒ xanh giả" rộng hơn phép đo (chỉ bỏ sót DỌN cháu, verdict đúng) | P4 | mới | hồ sơ (thông điệp commit/PR) |
| L4 — P4 của lượt 5 (và ghi nhận lượt 2A/3/4) chưa áp | P4 | mang | hồ sơ + mã test (theo `luot5/HINT.patch`) |

CÙNG HÌNH DẠNG (S2 của lease): hình dạng "giới hạn/bằng chứng chỉ nằm ở bàn giao, chưa nằm trong mã" xuất hiện ở lượt 5
(L2: `t199`) và lượt 6 (L1: răng của `doc_pid` chỉ trong thông điệp commit) — HAI lượt liền, cả hai P4; chưa tới ngưỡng ba.
Không đường vào MỚI nào của đích spec (M1–M5, A1–A11) sống sót trong lượt này.

Tổng: **0 P1 / 0 P2 / 0 P3 / 4 P4**. Chẩn đoán của executor ĐÚNG; bản vá ĐÚNG và có răng dưới chèn lỗi; không hồi quy
(195/195, `bỏ qua=0`; `L`, C1+L, C2 vẫn chết bằng `TinHieuChotCa`); A7(2) 596 ≤ 600, A8 byte-exact, ruff F delta 0.

## Dọn

Bảy worktree tạm `wt6.OKH3/{full,cu,moi,cu_e1,moi_e1,mL,h}` đã `git -C cay-kho worktree remove --force` (09:47:18Z);
`git -C cay-kho worktree list` chỉ còn `cay-kho 4dc226b`; `cay-kho` HEAD `4dc226bc7d25…`, `git status --short` rỗng; không lệnh
`git config` nào. Giàn + log giữ ở `wt6.OKH3/`: `full312.log`, `hint312.log`, `a8.py`, `ruff/`, `race/{race.py,lap.sh,burst.sh,
mot.sh,sinh.py,sinh_phu.py,matran*.txt/.out,lap_*.txt,burst_*.txt,so0_*.out}`, `hq/{chay_ca.py,mot_hq.sh,sinh_hq.py,jobs.txt,hq.out}`.
`HINT.patch` ở gốc $R là GỢI Ý (P4), không chặn; lease g5 hết hạn `2026-09-30T10:48:00Z`.

VERDICT: PASS
