verdict: changes_requested
reviewed_sha: 0ce1ad3903321f5e45a753eb1d0714ea9ee2aed8
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: claude-opus-5-5 (Opus 5.5, tự khai)
independent_from_executor_session: true
assurance: review_deferred
review_axes: [spec, standards_security]

> TRẠNG THÁI: HOÀN TẤT 2026-10-01T00:28Z (bắt đầu 2026-09-30T22:04:25Z; ghi tăng dần suốt lượt). Đếm theo LỚP còn mở:
> **P0=0 · P1=0 · P2=1 · P3=1 · P4=6** (BẢNG LỚP). P1 lượt 5 (CUA-UTF8-NGOAI-BANG-CUA) ĐÃ VÁ THẬT; lớp mồ côi (b)(c) ĐÃ VÁ THẬT trên
> POSIX. Còn: P2 nghiệm thu Windows (không vá được bằng mã ở Linux) · P3 đồ giả kernel32 bỏ qua tầng chuyển kiểu ctypes (N_B, N_H sống) ·
> P4×6. Trọn bộ dạng mảnh như CI ở (a) và (b): 415/416 `ok … 1/61` mỗi env + `t2_go_canary` (môi trường) — gom 8/8 xanh khi mảnh 1 có
> `jsonschema`; delta lỗi đột biến so nền = 0. `out/HINT.patch` v2: dry-run rc=0; áp đủ ⇒ +406 (vượt trần 6 — chủ kho quyết).
> Ngưỡng áp: `review_class`/`effective_review_class: sensitive`, `assurance_target: human_audited` (LEASE-g2). Lượt này CÙNG PROVIDER
> ⇒ nhãn tối đa `same_provider_approved`, và nhãn ấy KHÔNG thay mức assurance bắt buộc cho `sensitive` (§8).
> SPEC sha256 đo lại `18504ced…0b88` — KHỚP. PROMPT sha256 `d056687d…3c14` = `prompt.sha256`.
> Máy: 4 lõi, 15 GB RAM, python 3.11.15/3.12.3/3.13.12, git 2.43.0; lúc bắt đầu tải ~0 (máy KHÔNG dùng chung ở mốc 22:08Z — chỉ có
> vòng chờ của phiên điều phối). KHÔNG `jsonschema` (công cụ bắt buộc duy nhất đỏ trong `cong_cu.py kiem-tra`), KHÔNG `shellcheck`
> (không bắt buộc) ⇒ `t2` bỏ qua, `t2_go_canary` KHÔNG ĐO ĐƯỢC — cùng điều kiện lượt 5/executor.
> **Đĩa `/` còn 629 MB (99%)** — `/tmp/claude-0` 26 GB là hiện vật phiên khác (không đụng). Nên rig đặt trong một **tmpfs 7 GB gắn
> TẠI `$R/tam/ram`** (`mount -t tmpfs`, root) — mọi clone/TMPDIR ở đó; log ghi đĩa ở `$R/tam/log`. Tháo khi xong (SNAPSHOT cuối).
> Rig: `tam/ram/{n,l5,h}` = clone `kho.git` @`fc852ff`/`8757a84`/`0ce1ad3` dựng trong CÙNG một lệnh (22:13:53–22:14:13Z,
> `core.abbrev 7`); `cmp` h = cay-kho (2 tệp); sha256 `cong_cu_test.py`: h `05dce551…`, l5 `fd959d71…` (= số lượt 5), n `cb295ee1…`.
> 16 clone mảnh `tam/ram/m{a,b}/s{0..7}` @`0ce1ad3` + 2 clone `gate` `tam/ram/g{a,b}`. Script: `tam/cu/chay_manh.sh`, `chay_gate.sh`.
> 22:15:51Z khởi chạy 16 mảnh (8 env CI (a) + 8 env (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`, qua `__main__` ⇒ đi nhánh
> phóng lại THẬT), mỗi mảnh `CONG_CU_TEST_TIEN_TRINH=1`, tách phiên (`setsid`) để trần 2 giờ của tác vụ nền không cắt; 22:18:32Z khởi
> chạy job `gate` (a)/(b) (`CONG_CU_TEST_BAN_KINH=manh`). Công cụ đo: `tam/cu/chay_ca.py` (nạp importlib, `_chay_1_ca` CỦA tệp),
> `tam/cu/mot_db.py` (`_do_mot` + `_ket_luan_ban_ghi` CỦA tệp) — luôn chạy `-X utf8`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR trong tmpfs.

## SNAPSHOT ĐẦU/CUỐI (§8.2)

| đối tượng | đầu (22:05:04Z) | cuối | ghi chú |
|---|---|---|---|
| `cay-kho` HEAD / tree | `0ce1ad3903321f5e45a753eb1d0714ea9ee2aed8` / `904f887f05400d7387478817dd91d44743f97416` | (00:27:47Z, cuối) `0ce1ad3903321f5e45a753eb1d0714ea9ee2aed8` / `904f887f05400d7387478817dd91d44743f97416` | — |
| `cay-kho` `status --porcelain --ignored` / `diff` / `diff --cached` | 0 dòng / 0 B / 0 B | (00:27:47Z, cuối) 0 dòng / 0 B / 0 B | `GIT_OPTIONAL_LOCKS=0` từ lệnh thứ 3 |
| `cay-kho` mục index (sha256 `ls-files -s`) | `94befac6ce1d5c18…` = cây HEAD; mtime index 20:37:22Z (trước phiên) | (00:27:47Z, cuối) `94befac6ce1d5c18…`, mtime 20:37:22Z | lệnh khảo sát thứ 2 (`git status --short`, chưa có `GIT_OPTIONAL_LOCKS=0`) KHÔNG ghi index — mtime giữ 20:37:22Z |
| `kho.git` | `for-each-ref` sha256 `16d9e232985ca14b…` | (00:27:47Z, cuối) `16d9e232985ca14b…` | — |
| `~/.gitconfig` | sha256 `75239ed3763a89e3…`, mtime 22:03:33Z (trước phiên) | (00:27:47Z, cuối) `75239ed3763a89e3…`, mtime 22:03:33Z | — |
| `~/.cache/pip` | — | (00:27:47Z) tệp mới hơn mốc bắt đầu: 0 | pip luôn `--no-cache-dir` |
| tmpfs `$R/tam/ram` | gắn 22:12Z (7 GB) | tháo 00:27:05Z; `mount \| grep rv671-l6` ⇒ 0 dòng | thư mục rỗng còn lại trong `$R/tam` |

Giới hạn: snapshot chỉ chứng minh không có delta quan sát được ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Không lệnh
nào của lượt này chạy bộ ca hay ghi trong `cay-kho`/`kho.git` (chỉ đọc: `git -C cay-kho …` với `GIT_OPTIONAL_LOCKS=0`, `git clone kho.git`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

> Commit mới từ lượt 5 (`8757a84`): chỉ `0ce1ad3` (`git diff --numstat 8757a84 0ce1ad3` ⇒ `122 15 ops/cong_cu_test.py`; `bash_nen.py`
> không đổi). sha256 AST `8757a84` = `0ce1ad3` TỪNG BYTE cho `_ep_utf8`, `_BIEN_UTF8`, `_NAP_UTF8`, `t49`, `t60`, `t61`, **`t62`**, `t63`,
> `main`, `_main_gop` (⇒ lời khai "`t62` không đổi dòng nào": KHỚP). Vá 6 đổi: khối phóng lại → `_phong_lai`; thêm `_k32_gia` + `t64`;
> cửa UTF-8 thành `_in_tu_kiem_che_do_utf8` trong `_CUA` (= HINT lượt 5 hunk 2–3); chú thích AST đầu tệp (= HINT lượt 5 hunk 1).
> Nhãn §8: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ` (+ `TÁI PHÁT`). Mọi bằng chứng do lượt này tự đo trên bản sao tạm.

| lớp (slug ổn định) | nguồn | hạng cũ | nhãn trên `0ce1ad3` | bằng chứng tự đo |
|---|---|---|---|---|
| CUA-UTF8-NGOAI-BANG-CUA | lượt 5 `8757a84` | P1 | **ĐÃ VÁ THẬT** | `tam/cu/mot_db.py` (gọi `_do_mot`+`_ket_luan_ban_ghi` CỦA tệp) trên head: `f25_cua_moi_vi_tri` ⇒ `ok … giết đúng 't52_…' · bán kính 1/61`; `f13_dispatcher_nuot`, `f25_bo_chot_doi_so_la`, `f27_entry_drop`, `f27_entry_rc` ⇒ `ok … 1/61` (f28×4 + A/B l5/nền: xem BẢNG ĐO). Cửa nay đi qua `cua`/`_CUA` ⇒ N6 (dò mọi vị trí) không còn biểu diễn riêng được. Đột biến C1 (gỡ khoá khỏi `_CUA`) / C2 (cửa thoát 0): BẢNG ĐỘT BIẾN |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | lượt 3 `e46f569` | P3 | **ĐÃ VÁ THẬT trên POSIX cho (b)(c)** + **VÁ SINH LỖI MỚI (nhỏ)**; Windows KHÔNG ĐO ĐƯỢC | HƯỚNG 1: `8757a84` (u8=0) kill-9 còn 2, SIGTERM còn 3, SIGTERM bộ ca ⇒ 241; `0ce1ad3` 0 sống mọi kịch bản, PID bộ ca = PID harness, rc -9/-15/-2/-15. HƯỚNG 2: cờ/argv/cwd/stdin/`-m`/symlink/dấu cách giữ nguyên; **mới: đóng fd 1/2 lúc gọi ⇒ `AttributeError` ở dòng xả đệm, rc=1** (đường cũ chạy) — finding TU-PHONG-LAI-KHONG-TRONG-SUOT (d) [P4] |
| NGHIEM-THU-WINDOWS-CON-THIEU | lượt 1 → nay | P2 | **CHƯA VÁ — KHÔNG ĐO ĐƯỢC ở Linux** | hiện vật lượt này (BAO_CAO/DUONG_VAO vòng 6) không có log/receipt Windows nào cho `0ce1ad3`; BAO_CAO §6 tự khai "Job Object THẬT … KHÔNG ĐO ĐƯỢC ở đây". Nhánh Windows của `_phong_lai` là MÃ MỚI chưa từng chạy trên Windows |
| LOI-KHAI-RONG-HON-PHEP-DO | lượt 1–3; tái phát `8757a84` | P4 | **TÁI PHÁT (lần 2, do chính vá 6)** | chú thích `:15-16` vá 6 vừa ghi "38 Call … 5 `{**os.environ}` … 18 biến" (số của `8757a84`, HINT lượt 5); `tam/cu/dem_env.py` trên `0ce1ad3` ⇒ **39** Call {Name 19, dict(Name) 1, moi_truong 12, dict(os.environ) 3, `{**os.environ}` **4**}; khác `8757a84`: MẤT `subprocess.run(env={**os.environ, _DAU…})` (khối phóng lại cũ), THÊM `popen(lenh, env=env)` (`_phong_lai`) + `subprocess.Popen(…, env=env)` (`t64`). Tính chất (mọi `env=` truy về `os.environ`) vẫn đúng |
| TEN-CA-LECH-SPEC | lượt 2/3 | P4 | theo quyết định chủ kho (khai ở PR) — thân PR KHÔNG ĐO ĐƯỢC | `t52_import` 0 lần, `def t60_import_bash_nen_khong_in_gi_ra_stderr` 1 lần; nay có thêm `t64` (spec không có) |
| T49-CO-CHE-HOAN-BO-QUA | advisory `bd6ad5d` | đóng | ĐÃ VÁ THẬT (giữ) | `bo_qua_va` 0 lần; AST `t49`/`t63` = `8757a84` |
| CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG | lượt 1 → `c5f3da0` | đóng (Linux) | ĐÃ VÁ THẬT (giữ) | AST `t49`/`t63` không đổi; M49a/M49d trên head: BẢNG ĐỘT BIẾN |
| T62-GHI-PYC-VAO-CAY | lượt 4 | đóng | ĐÃ VÁ THẬT (giữ) | `t62`+`t64` một mình, clone mới, con KHÔNG có `PYTHONDONTWRITEBYTECODE` ⇒ 0 `.pyc`, `status --ignored` rỗng |
| UTF8-BO-SOT-BO-DOC | lượt 1 | đóng | ĐÃ VÁ THẬT (giữ) | vòng CA của 8 mảnh env (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` (qua execve): `60/60 đạt; tổng=61, bỏ qua=1` |
| CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 | lượt 1–3 | đóng | ĐÃ VÁ THẬT (giữ) — xem BẢNG ĐỘT BIẾN (M61a–g, R1–R10 đã đổi mỏ neo theo `_phong_lai`) | |
| CON-TRO-CA-CU | lượt 1 | đóng | ĐÃ VÁ THẬT (giữ) | `t60b` 0 lần |
| (slug cũ lượt 2–4 không có trong bảng lượt 5) `PHONG-LAI-THIEU-QUAN-SAT` (l2 P2-C) · `PHONG-LAI-STDIN-RC0` (l2 P3-B) · `T61-DO-DUOI-LOCALE-C` (l2 P3-C) · `UTF8-QUAN-SAT` (l3) · `PHONG-LAI-MO-COI` (tên nợ l4) | lượt 2–4 | đóng / đã gộp | ĐÃ VÁ THẬT (giữ) | nối slug: = `TU-PHONG-LAI-CHI-KHOA-CO-UTF8` (R1–R10 giết đúng nhãn) · = `t62` (6) (R7 ⇒ "(6) … rc=0 stdout=0") · đo lại đúng env lượt 2 `LC_ALL=C PYTHONCOERCECLOCALE=0 PYTHONUTF8=0`: `t60 t61 t62 t64` xanh × 3.11/3.12/3.13 · = `CA-KHOA-UTF8-THIEU-QUAN-SAT` · = biểu hiện (b) của `TU-PHONG-LAI-KHONG-TRONG-SUOT` (HƯỚNG 1) |

## BẢNG LỚP
| slug lớp | finding/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| NGHIEM-THU-WINDOWS-CON-THIEU | (1) không §6.1–6.3 Windows cho head; (2) giả thuyết B chưa đo; (3) mảnh/gom #668 trên Windows; (4) mô phỏng nền từ chối `\xff` ⇒ `t63` ĐỎ OAN (tái hiện trên head); (5) MỚI: nhánh Job Object chưa từng chạy trên Windows; (6) MỚI: thời lượng `t64` trên Windows | **P2** | lượt 1 → `0ce1ad3` | (1)–(3),(5),(6) không vá được bằng mã; (4) đo Windows trước (spec §2B/S2), hướng vá sẵn ở lượt 5 | KHÔNG ĐO ĐƯỢC ở Linux; (4) mô phỏng `tam/ram/gitgia/git` |
| DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES (MỚI) | N_B (truyền struct thay `byref`) và N_H (`byref(gh, 16)`) SỐNG trên đồ giả, ctypes thật hỏng; luật ABI viết tay (`argtypes is not None`, `_obj`); lời khai "cách gọi API … ĐÓNG" | **P3** | lượt 6, `0ce1ad3` | MỘT gốc: đồ giả không đi qua tầng chuyển kiểu ctypes ⇒ vá chung: API giả = hàm C thật (`CFUNCTYPE`) (HINT hunk 3) | lô 2 (nháp `f2`) + lô 3 (cây HINT): N_B ⇒ (w1); W-series giữ nhãn |
| TU-PHONG-LAI-KHONG-TRONG-SUOT | (b) mồ côi, (c) 241 — ĐÓNG trên POSIX; (d) MỚI do vá 6: fd 1/2 đóng lúc gọi ⇒ nổ trước khi phóng; lời khai W14 "tương đương" | **P4** | lượt 3 `e46f569` → vá 6 | (b)(c) đã vá bằng execve; (d): xả đệm bỏ qua `None` (hunk 2, sản phẩm — hướng) + chốt (k4) (hunk 5) | HƯỚNG 1/2; K4/K4b giết đúng từng fd; Windows KHÔNG ĐO ĐƯỢC |
| DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI (MỚI) | `popen` giả `set()` trước khi ghi thành viên ⇒ (w1) đỏ oan khi luồng bị giành đúng chỗ | **P4** | lượt 6, `0ce1ad3` | đổi thứ tự (hunk 3) | phép nới cửa sổ 0,2 s: hiện tại ĐỎ, đảo thứ tự XANH |
| CA-KHOA-T64-TREO-THAY-VI-DO (MỚI) | R11 (mất argv) ⇒ `t64` treo, không đỏ | **P4** | lượt 6, `0ce1ad3` | hẹn giờ dòng đầu (hunk 4) | R11 trên nháp `f3`/cây HINT ⇒ đỏ có tên ≤ ~120 s |
| LOI-KHAI-RONG-HON-PHEP-DO | tái phát lần 2: 38/5/18 → 39/4/20 | **P4** | lượt 1–3; `8757a84`; `0ce1ad3` | bỏ số đếm dễ trôi, giữ tính chất + cách đo (hunk 1) | `tam/cu/dem_env.py` |
| TEN-CA-LECH-SPEC | `t60`–`t64` thay `t52` của spec; `t64` ngoài spec r1 | **P4** | lượt 2/3 | quyết định chủ kho: khai ở PR | thân PR KHÔNG ĐO ĐƯỢC |
| TRAN-DONG-DAT-BANG-NEN (MỚI) | +400 đạt bằng nén: 29 dòng > 118, 6 dòng `;`, 5 walrus ở vá 6 | **P4** | lượt 6, `0ce1ad3` | chủ kho quyết thước đo | đo `tokenize` |
| CUA-UTF8-NGOAI-BANG-CUA | — | đóng | lượt 5 `8757a84` → `0ce1ad3` | — | 9/9 dispatcher `ok … 1/61`; A/B f25: l5 ĐỎ tdg / nền `ok 1/56` |
| T49-CO-CHE-HOAN-BO-QUA · CA-KHOA-STAGING-CHI-DO-DUONG-THANH-CONG · T62-GHI-PYC-VAO-CAY · UTF8-BO-SOT-BO-DOC · CA-KHOA-UTF8-THIEU-QUAN-SAT · TU-PHONG-LAI-CHI-KHOA-CO-UTF8 · CON-TRO-CA-CU | — | đóng (giữ) | lượt 1–5 | — | AST không đổi; M49a/d, M61a–g, M60a, R1–R10, P0/P4 giết đúng nhãn; 0 `.pyc`; vòng CA (b) 60/60 |

Đếm: **8 lớp còn mở** (P2×1 · P3×1 · P4×6); **8 lớp đóng** (tính cả 7 lớp gộp ở dòng cuối). Biểu hiện còn mở: WINDOWS 6 · DO-GIA 2 ·
KHONG-TRONG-SUOT 2 ((d) + lời khai W14) · BAO-HIEU 1 · T64-TREO 1 · LOI-KHAI 1 · TEN-CA 1 · TRAN-DONG 1 = **15**.
Ngưỡng `sensitive` + chỉ thị lượt ("approve chỉ khi không còn P0/P1/P2/P3") ⇒ **changes_requested**, `assurance: review_deferred`.

## BẢNG SĂN

> Mọi phép đo trên bản sao trong `$R/tam/ram` (tmpfs), `PYTHONDONTWRITEBYTECODE=1`, TMPDIR trong tmpfs; log ở `tam/log/`.

```
HƯỚNG 1: mồ côi & mã thoát — đo lại lớp TU-PHONG-LAI-KHONG-TRONG-SUOT (b)(c) trên head, A/B với 8757a84 (cây dựng cùng lệnh)
  giả thuyết : nếu execve không thay được tầng bao thì harness giết PID nó biết vẫn để bộ ca sống / SIGTERM bộ ca ra 241
  lệnh       : python3.12 tam/cu/do_mo_coi.py tam/ram/{l5,h} {kill9,term,int,term_bo_ca} {0,1}
               (phóng `python3.12 -B ops/cong_cu_test.py` trong session riêng, 3 s rồi gửi tín hiệu, đếm tiến trình
               không-zombie còn trong session sau 2 s; log tam/log/mo-coi-l5-h.jsonl; tải máy ~20)
  output     : l5 u8=0: kill9 ⇒ rc=-9, CÒN 2 ('/usr/bin/python3.12 -X utf8 -B ops/cong_cu_test.py' + cháu) · term ⇒ rc=-15,
                        CÒN 3 · int ⇒ rc=-2, 0 · term_bo_ca (pid bộ ca 15472 ≠ harness 15419) ⇒ rc=241
               h  u8=0: kill9 ⇒ -9, 0 · term ⇒ -15, 0 · int ⇒ -2, 0 · term_bo_ca ⇒ pid bộ ca = pid harness (17242) ⇒ -15, 0
               đối chứng u8=1 (cả hai cây, 4 kịch bản): 0 còn sống, rc tự nhiên (-9/-15/-2/-15)
  kết luận   : KHÔNG PHẢI LỖI trên POSIX — lớp (b)(c) đóng trên Linux (số tiến trình còn sống ở nền phụ thuộc thời điểm:
               executor ghi 1–2/1–2, lượt này 2/3 — cùng chiều, không phải con số bất biến). Windows: KHÔNG ĐO ĐƯỢC.

HƯỚNG 2: (i) execve có làm mất gì mà đường subprocess cũ giữ
  giả thuyết : exec thay ảnh có thể làm rơi cờ trình thông dịch/argv/cwd/stdin/fd/đệm, hoặc đổi mã thoát
  lệnh       : tam/cu/do_execve.py + tam/cu/chay_execve.sh — dau_{l5,h}.py = PHẦN ĐẦU THẬT của cong_cu_test.py (cắt tại
               `\nimport yaml\n`, như t64) + đầu dò in sys.flags/orig_argv/argv/cwd/fd/stdin/PL/DAU_SOT; env -i
               LC_ALL=C.UTF-8 PYTHONUTF8=0 (⇒ đi nhánh phóng lại); log tam/log/execve-so-sanh.txt
  output     : S1 `-B -u -s -O -W error::UserWarning -X dev -X faulthandler … a "b c"` · S2 `-I` · S3 đường dẫn có dấu cách
               + chữ Việt, cwd khác · S4 symlink · S5 `-m dau_x` · S7 stdin qua ống · S8 thoát 7 ⇒ l5 = h TỪNG TRƯỜNG
               (flags, orig_argv, argv, cwd, PL=1, DAU_SOT=False, u8=1, stdin 'XYZ', rc 7); S9 tự SIGTERM ⇒ l5 rc=241, h rc=143
               (bash: 128+15 = chết vì tín hiệu — đúng); S12 sitecustomize in trước khi phóng ⇒ cả hai giữ 2 dòng SITE.
               **S10 `>&-` (đóng stdout lúc gọi) ⇒ l5 rc=0 (chạy) · h rc=1 `AttributeError: 'NoneType' object has no
               attribute 'flush'` ở `_phong_lai:49`.** **S11 `2>&-` ⇒ l5 rc=3 (chạy, mã đầu dò) · h rc=1, KHÔNG in gì.**
               Biến thể W14 (bỏ xả đệm, dựng từ dau_h.py): S10 rc=0, S11 rc=3, S12 vẫn 2 dòng SITE (vì `_ep_utf8()` đã
               `reconfigure` ⇒ đã xả đệm trước đó).
               S13 venv (`--system-site-packages` + jsonschema, gọi bằng python của venv): l5 = h ⇒ `u8=1 PL=1`, `sys.prefix` ≠
               `base_prefix`, import được `jsonschema`, `sys.executable` = python của venv (execve giữ argv[0] ⇒ giữ venv).
  kết luận   : LỖI (nhỏ) — execve giữ mọi thứ đường cũ giữ TRỪ khi fd 1/2 đóng lúc gọi: `sys.stdout`/`sys.stderr` là
               `None` ⇒ chính dòng xả đệm nổ trước khi phóng (đường cũ vẫn chạy). Fail-closed (rc=1, không xanh giả) ⇒
               P4. Kèm: lời khai "W14 bỏ xả đệm TƯƠNG ĐƯƠNG" SAI ở đúng góc này (W14 khác hành vi quan sát được, và khác
               theo chiều TỐT hơn). Xem finding TU-PHONG-LAI-KHONG-TRONG-SUOT (d) [P4].

HƯỚNG 3: (ii) chế độ mảnh/gom #668 như CI gọi — đi qua execve đúng không
  giả thuyết : exec có thể làm rơi biến mảnh, để lại tầng bao, hoặc làm worker `--ban-kinh-con` phóng lại/mang dấu
  lệnh       : 16 mảnh THẬT (tam/cu/chay_manh.sh); lúc 22:4xZ đọc /proc/<pid>/{stat,cmdline,environ} của mảnh env (b) và con
  output     : pid 2262 `/usr/bin/python3.12 -X utf8 ops/cong_cu_test.py` — cha = `bash tam/cu/chay_manh.sh b 7` (KHÔNG có tầng
               bao python); env exec: PYTHONUTF8=1 PYTHONIOENCODING=utf-8 CONG_CU_TEST_MANH=7/8 CONG_CU_TEST_MANH_RA=manh/manh-7.txt
               LC_ALL=C CONG_CU_TEST_DA_PHONG_LAI=1; con 17231 (worker): PYTHONUTF8=1, utf-8, MANH giữ nguyên, KHÔNG dấu.
               Như vậy ở pid 2265 (mảnh 0), 2267 (mảnh 2). Số tầng bao `python3.12 ops/cong_cu_test.py` mang PYTHONUTF8=0: 0.
               Vòng CA cả 16 mảnh: `60/60 đạt; tổng=61, bỏ qua=1`. Kết quả bán kính/gom: BẢNG ĐO.
  kết luận   : KHÔNG PHẢI LỖI — một lần exec, argv/env mảnh đi qua, worker không phóng lại, dấu không sót.

HƯỚNG 4: `__file__` không phải tệp và các dạng gọi khác — trên TỆP THẬT (không phải đầu dò), qua execve
  lệnh       : bản sao head + cửa in thêm `PID=`; env -i LC_ALL=C.UTF-8 PYTHONUTF8=0; so PID harness biết với PID cửa in
  output     : tệp · `-m ops.cong_cu_test` · `-I` · `-X utf8=0` ⇒ rc=5 `UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_SOT=0`, PID in ra = PID
               harness (5675/5971/6218/6506 — cùng PID); `cat … | python -B -` ⇒ rc=1 KHONG_PHONG_LAI '<stdin>'; `-c exec(…)` ⇒
               rc=1 KHONG_PHONG_LAI ''; zipapp ⇒ rc=1 KHONG_PHONG_LAI '…/cct.pyz/__main__.py'; 0 `.pyc`
  kết luận   : KHÔNG PHẢI LỖI — và `t62` đo đúng tiến trình CHẠY BỘ CA (cùng PID sau exec; `main()` chạy cùng tiến trình).

HƯỚNG 5: `t60`–`t64` khi đường dẫn kho VÀ TMPDIR mang chữ Việt + dấu cách, 3 phiên bản × 2 môi trường
  lệnh       : git clone --shared … "tam/ram/có dấu cách/kho việt"; TMPDIR="…/thư mục tạm có dấu";
               <py> -X utf8 tam/cu/chay_ca.py <kho> t60_ t61_ t62_ t63_ t64_  × {3.11, 3.12, 3.13} × {thường, LC_ALL=C PYTHONUTF8=0
               PYTHONIOENCODING=ascii}
  output     : 6/6 tổ hợp `TONG {"qua": 5}`; 0 `.pyc` (t64 ghi `dau.py` vào TMPDIR ngoài-ASCII và phóng lại qua execve dưới LC_ALL=C:
               argv surrogateescape → fsencode khứ hồi đúng)
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 6: (iv) `t64` dưới tải + chạy nền: chập chờn? sót tiến trình?
  lệnh       : tam/cu/lap_t64.sh — 30 lần `t64` (chay_ca.py) lúc 16 mảnh + đột biến đang chạy (tải 21–23 / 4 lõi); lần 1 trong
               shell của harness (đo được SIGINT KHÔNG bị lờ — harness bật job control); lần 2 `trap '' INT` (SIGINT=SIG_IGN kế
               thừa, như job nền của shell không tương tác); đếm tiến trình `…/<TMPDIR riêng>/t64-` còn sống sau mỗi lần
  output     : lần 1: 30/30 `qua`, 0,86–1,25 s/ca · lần 2: 30/30 `qua`, `sigint=1` (SIG_IGN) cả 30 lần, sót 0/30
               (cột "sót" của lần 1 bị nhiễm `t64` của 16 mảnh song song — đã sửa phép đếm theo TMPDIR riêng ở lần 2)
  kết luận   : KHÔNG PHẢI LỖI trên head (khớp lời khai "45/45 xanh chạy nền" về chiều; lượt này 60/60).

HƯỚNG 7: (iv') `t64` khi CHÍNH khối phóng lại hồi quy — đỏ, hay treo?
  giả thuyết : `dau = p.stdout.readline()` không hạn chót; hồi quy khiến bản phóng lại KHÔNG in mà chờ stdin ⇒ ca treo, không đỏ
  lệnh       : đột biến R11 (mất argv khi phóng lại): `_phong_lai([sys.executable, "-X", "utf8", *sys.orig_argv[1:]], …` →
               `_phong_lai([sys.executable, "-X", "utf8"], …` trên bản sao; `timeout -s KILL 90 python3.12 -X utf8 chay_ca.py <cây> t64_`
               (rồi t62_); `_phong_con` (worker bán kính) `p.wait()` KHÔNG hạn chót (:7505-7507)
  output     : t64 ⇒ **bị giết ở 90 s, rc=137, không dòng kết quả nào** (bản phóng lại thành REPL đọc ống stdin của `t64`);
               t62 ⇒ `tin_dung_gia` "cửa --tu-kiem-che-do-utf8 không in gì: rc=0 ''" (0,61 s). Không còn REPL mồ côi sau khi giết.
               Hiện 0/416 DOT_BIEN đặt mỏ neo trong phần đầu tệp (trước `import yaml`) và 0 DOT_BIEN nhắm t60–t64 ⇒ bán kính CI
               hiện không chạm đường treo.
  kết luận   : LỖI (nhỏ, chất lượng ca khoá) — một hồi quy "mất argv" làm bộ ca TREO tới trần job (gate 60′ / mảnh 30′) thay vì
               ĐỎ có tên; fail-closed nhưng không chẩn đoán được. Xem finding CA-KHOA-T64-TREO-THAY-VI-DO [P4].

HƯỚNG 8: bố cục `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` (x64 144 B / x86 112 B, cờ offset 16) so tài liệu
  lệnh       : ctypes trên máy này (x86-64: void* 8, size_t 8, align int64 8 — cùng quy tắc với Win64): bản trải phẳng NGUYÊN VĂN
               `_phong_lai:54-55` so bản LỒNG theo winnt.h (BASIC 13 trường + IO_COUNTERS 6×u64 + 4×SIZE_T)
  output     : phẳng: sizeof 144, offset {tg 0, co 16, ws 24, sl 40, aff 48, uu 56, io 64, mem 112}; lồng: EXT 144, BASIC 64, IO 48,
               LimitFlags 16, IoInfo 64, ProcessMemoryLimit 112; `bytes(phẳng(co=0x2000)) == bytes(lồng)` True.
               x86: tính tay theo MSVC (LARGE_INTEGER căn 8, SIZE_T 4): phẳng 0/16/20/28/32/36/48/96 → 112 = lồng (BASIC 44→48 đệm, IO @48,
               4 SIZE_T @96) — KHÔNG ĐO ĐƯỢC bằng máy (không có Windows x86; Linux i386 căn int64 = 4 nên không đại diện).
  kết luận   : KHÔNG PHẢI LỖI (x64 đo được; x86 suy từ quy tắc căn lề). Hằng số: 0x2000 = KILL_ON_JOB_CLOSE, 0x1000 = SILENT_BREAKAWAY_OK,
               lớp 9 = JobObjectExtendedLimitInformation — khớp tài liệu.

HƯỚNG 9: (iii') đồ giả kernel32 — mô phỏng TRẠNG THÁI hay diễn kịch bản; đột biến sản phẩm Windows có bị che không
  giả thuyết : `api()` chỉ dò `argtypes is not None`/`restype is c_void_p`, `dat()` nhận `getattr(p, "_obj", p)` ⇒ lỗi GỌI (khai/đưa
               sai kiểu) không đi qua tầng chuyển kiểu ctypes nên đồ giả không thấy
  lệnh       : lô đột biến 1 (N_A/N_B/N_C trên head) + đối chứng ctypes THẬT: hàm C dựng bằng `ctypes.CFUNCTYPE(<chữ ký Win32>)(cb)`, ép thành
               con trỏ `CFUNCTYPE(c_int)` rồi gán argtypes/restype như sản phẩm làm với WinDLL
  output     : N_B (`gh` thay `byref(gh)`) ⇒ `t64` XANH trên head; ctypes thật ⇒ `ArgumentError: argument 3: TypeError: wrong type`.
               N_A (`(vp, i)`) ⇒ ctypes thật: phía C nhận 0xffffffffffffffff (libffi mở rộng dấu) ⇒ tương đương. N_C (`argtypes=()`)
               ⇒ ctypes thật chuyển đối số thừa `None`→NULL, trả handle đúng ⇒ tương đương. Trên nháp đồ giả `CFUNCTYPE` (`f2`): N_B ⇒ (w1)
               "… (ArgumentError …)"; W6 ⇒ (w1) qua handle `1<<60` bị `c_int` cắt thật.
  kết luận   : LỖI — finding DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES [P3]. Phần TRẠNG THÁI (job/cờ/thành viên/kế thừa) là thật (W1–W4, W7–W13).

HƯỚNG 10: mã thoát 5 của cửa tự kiểm (nay trong `_CUA`) có va chạm; `t5`/SIGPIPE `rc=141` có liên quan PR không
  lệnh       : grep `sys.exit(`/`_MA_TU_KIEM_UTF8`; `git log fc852ff | grep -i sigpipe`; `git show fc852ff:ops/cai_cong_cu.sh`; grep `rc=141` log
  output     : mã 5 chỉ ở cửa UTF-8 (`:8730` — tự `sys.exit` TRƯỚC `sys.exit(0)` của nhánh `_CUA`) và 3 chốt `t62`; các cửa khác 0/9,
               `--gop` 0/1/2, đối số lạ 2, `KHONG_PHONG_LAI` 1. SIGPIPE: `7b308bc` "Merge pull request #681 … cai-cong-cu-sigpipe" nằm
               trong `fc852ff`; `cai_cong_cu.sh:64-66` đã thay `| head -1`; PR không chạm `cai_cong_cu.sh`/`do_sigpipe.sh`; 0 `rc=141`
               trong mọi log của lượt này.
  kết luận   : KHÔNG PHẢI LỖI (không va chạm mã; SIGPIPE là nền cũ đã vá trên master).

HƯỚNG 11: `preexec_fn` của `t64` (và của hunk 5 đề xuất) trong tiến trình có luồng
  lệnh       : <py> -W error::DeprecationWarning: một luồng daemon đang chạy + `subprocess.run(…, preexec_fn=lambda: None)` (3.12, 3.13);
               grep `threading.Thread(|ThreadPoolExecutor|daemon=True` trong tệp
  output     : 3.12.3/3.13.12 ⇒ rc=0, không cảnh báo; cả tệp chỉ tạo luồng trong CHÍNH `t64` (`:3020`, `:3038`), đều join trước Popen kế
  kết luận   : KHÔNG PHẢI LỖI (không có luồng lạ lúc `preexec_fn` chạy; cảnh báo fork-với-luồng của 3.12 chỉ áp cho `os.fork`).

HƯỚNG 12: (P2 lượt 5, biểu hiện 4 — MÔ PHỎNG) nền không nhận tên byte `\xff` vào INDEX ⇒ `t63` có còn ĐỎ oan trên head
  lệnh       : `tam/ram/gitgia/git` (đầu PATH; chỉ can thiệp `update-index --index-info`: bỏ bản ghi chứa `\xff`, in "Ignoring path",
               rc=0; mọi lệnh khác exec git thật); chay_ca.py `t49_ t63_` trên l5 và h
  output     : cả hai cây: `t49` `bo_qua` "KHÔNG ĐO ĐƯỢC: INDEX không nhận tên b'ops/xau_\xff.py'…" (đúng spec §2B) ; `t63` `giet_that`
               "(ops/no_cu.py/rc) bằng chứng stage hỏng mà t49 không BỎ QUA đúng bước (chờ 'no_cu')…"
  kết luận   : LỖI CÓ ĐIỀU KIỆN (mô phỏng; Windows thật KHÔNG ĐO ĐƯỢC) — vẫn mở, thuộc NGHIEM-THU-WINDOWS-CON-THIEU [P2] (4).

HƯỚNG 13: (iv'') đồ giả báo hiệu TRƯỚC khi ghi trạng thái — mầm chập chờn của (w1)
  giả thuyết : `_k32_gia.popen` gọi `k.co.set()` TRƯỚC `[j["tv"].add(con) …]`; luồng chính dậy từ `k.co.wait(15)` là gọi ngay
               `k.cha_chet()` ⇒ luồng (w1) bị giành GIL/CPU đúng giữa hai lệnh thì `cha_chet` không thấy con ⇒ con sống ⇒ (w1) ĐỎ OAN
  lệnh       : bản sao head, NỚI CỬA SỔ để đo (chèn `time.sleep(0.2)` giữa `k.co.set()` và dòng ghi thành viên) ⇒ chay_ca t64_;
               đối chứng: cùng `sleep(0.2)` nhưng `k.co.set()` dời SAU dòng ghi thành viên
  output     : thứ tự hiện tại ⇒ `giet_that` "(w1) cha chết mà con còn sống: job={1: {'co': 8192, 'tv': {'cha', <Popen … returncode: -9 …>}}}"
               (con vào tập thành viên SAU lúc `cha_chet` chạy); thứ tự đảo ⇒ `qua` (1,82 s). Tự nhiên: 0 lần đỏ trong 60 lần + mọi lượt
               đột biến của lượt này (cửa sổ tự nhiên chỉ vài bytecode — cần luồng bị giành đúng chỗ).
  kết luận   : LỖI (nhỏ, chập chờn tiềm ẩn của ca khoá) — finding DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI [P4]; vá = đổi thứ tự (trung hoà dòng).
```

## BẢNG ĐỘT BIẾN

> Công cụ: `tam/cu/dot_bien.py` + `tam/cu/spec_l6.py` (51 đột biến, mỏ neo NGUYÊN VĂN từ `0ce1ad3`, kiểm trước: mọi mỏ neo đếm đúng
> 1). Mỗi đột biến: `git clone --shared tam/ram/h` → thay đúng một lần mỗi mỏ neo → xoá `__pycache__` → `PYTHONDONTWRITEBYTECODE=1`,
> TMPDIR riêng → `python3.12 -X utf8 tam/cu/chay_ca.py` nạp tệp bằng importlib và chạy ca qua `_chay_1_ca` CỦA CHÍNH tệp ⇒
> `GIET_DUNG_NHAN` chỉ khi `TinHieuChotCa` mang đúng tên ca VÀ lý do chứa nhãn chốt chờ. Log: `tam/log/db-l6.jsonl`. Dưới tải 19–23.
> **Tổng lô 1 (head):** 39 giết thật đúng nhãn · 1 giết đúng nhãn kiểu "đỏ oan khi chạy nền" (chứng minh `preexec_fn` gánh (k3)) ·
> 6 sống KỲ VỌNG (R2n, W14, W10 — tương đương theo phép đo của `t64`/`t62`; hai phép ghép "gỡ chốt + đột biến nó bắt" chứng minh
> (k3), (k2) là chốt DUY NHẤT bắt M4, M3; đối chứng head chạy nền) · 3 sống TƯƠNG ĐƯƠNG THẬT (W5 chỉ-trường, N_A, N_C — đo) ·
> **1 SỐNG SÓT thật: N_B (đồ giả che)** — thêm N_H `byref(gh, 16)` chạy riêng trên head: `SONG` (đồ giả che, `tam/log/db-nh.jsonl`) · 1 tín dụng giả kỳ vọng (C1: suite ĐỎ, không xanh). Không đột biến nào làm ca KHÁC đỏ
> (`ca_khac_khong_qua` rỗng ở cả 51). Lời khai executor "37/37 giết đúng nhãn": các đột biến cùng tên tôi tái dựng (M1–M6, W1–W4,
> W6–W13, R1, R3–R10, P0, P4, M61a–g, M60a) đều giết đúng nhãn ⇒ khớp; "3 tương đương" (W10, W14, R2n): W10/R2n khớp, **W14 KHÔNG
> tương đương** khi fd 1/2 đóng lúc gọi (HƯỚNG 2) — khác quan sát được, theo chiều TỐT hơn head.

| đột biến (thay đúng 1 chỗ trên 0ce1ad3) | ca đích | kết quả head — tín hiệu (rút gọn) | phân loại |
|---|---|---|---|
| M1 quay về `subprocess.run(...).returncode` (ca âm bắt buộc) | t64_ | `GIET_DUNG_NHAN` (k1) harness kill() pid 20733 mà tiến trình chạy bộ ca 20800 vẫn giữ pipe sau 10s — MỒ CÔI | giết thật |
| M2 subprocess + chuyển tiếp SIGTERM/SIGINT | t64_ | `GIET_DUNG_NHAN` (k1) harness kill() pid 24260 mà tiến trình chạy bộ ca 24277 vẫn giữ pipe sau 10s — MỒ CÔI | giết thật |
| M3 subprocess + `prctl(PR_SET_PDEATHSIG)` (qua được k1) | t64_ | `GIET_DUNG_NHAN` (k2) SIGTERM tới tiến trình chạy bộ ca 29695 (harness biết 29662) mà harness thấy rc=241, chờ - | giết thật |
| M4 `signal(SIGINT, SIG_IGN)` trước exec | t64_ | `GIET_DUNG_NHAN` (k3) tiến trình chạy bộ ca 4561 LỜ SIGINT/Ctrl-C: 'PID=4561 U8=1 PL=1 INT=0\n' | giết thật |
| M5 POSIX đi nhánh nt | t64_ | `GIET_DUNG_NHAN` (k1) harness kill() pid 6648 mà tiến trình chạy bộ ca 6657 vẫn giữ pipe sau 10s — MỒ CÔI | giết thật |
| M6 nt đi exec | t64_ | `GIET_DUNG_NHAN` (w0) nhánh Windows gọi exec — trên nt `os.exec*` phóng MỚI rồi thoát cha ⇒ MỒ CÔI: [('/usr/bin/ | giết thật |
| R2n `sys.exit(_phong_lai(…) and 0)` (POSIX) | t64_ | `SONG`  | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| W14 bỏ xả đệm | t64_ (+t62_) | `SONG`  | sống ở `t64`/`t62` — nhưng KHÔNG tương đương thật: fd 1/2 đóng lúc gọi thì W14 chạy, head nổ (HƯỚNG 2) — finding TU-PHONG-LAI-KHONG-TRONG-SUOT (d) |
| W1 cờ 0 | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1: {'co': 0, 'tv': {'cha', <Popen: returncode: -9 args: ['/ | giết thật |
| W2 cờ 0x3000 | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1: {'co': 12288, 'tv': {'cha'}}} stderr='' | giết thật |
| W3 lớp 2 | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1: {'co': 0, 'tv': set()}} stderr='cong_cu_test: CANH_BAO_M | giết thật |
| W4 gán Job SAU popen | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1: {'co': 8192, 'tv': {'cha'}}} stderr='' | giết thật |
| W5 CHỈ trường `co` → c_uint64 | t64_ | `SONG`  | sống — TƯƠNG ĐƯƠNG THẬT: struct giống từng byte (144 B, cờ @16, 20–24 là đệm) — khác W5 của executor (u32 64 bit MỌI NƠI ⇒ 152 B, xem W5b) |
| W6 bỏ khai restype/argtypes | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={} stderr='cong_cu_test: CANH_BAO_MO_COI — không gắn được Jo | giết thật |
| W7 nuốt CANH_BAO | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở CreateJobObjectW (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải | giết thật |
| W8 bỏ kiểm Set | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở SetInformationJobObject (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test | giết thật |
| W9 bỏ kiểm Assign | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở AssignProcessToJobObject (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ tes | giết thật |
| W10 bỏ `job and` | t64_ | `SONG`  | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| W11 `except OSError` | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở WinDLL (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải VẪN chạy  | giết thật |
| W12 `.wait() * 0` | t64_ | `GIET_DUNG_NHAN` (w2) Job hỏng ở CreateJobObjectW (nt KHÔNG thử WinDLL: Job THẬT sẽ gắn vào CHÍNH bộ test): phải | giết thật |
| W13 phóng hai lần | t64_ | `GIET_DUNG_NHAN` (w1) cha chết mà con còn sống: job={1: {'co': 8192, 'tv': {<Popen: returncode: -9 args: ['/usr/ | giết thật |
| N_A Assign argtypes `(vp, i)` | t64_ | `SONG`  | sống — tương đương trên x86-64 (ctypes thật: libffi mở rộng dấu `int -1` ⇒ phía C nhận đúng 0xFFFF…FFFF — đo) |
| N_B truyền `gh` thay `byref(gh)` | t64_ | `SONG`  | **SỐNG SÓT — ĐỒ GIẢ CHE**: ctypes THẬT ném `ArgumentError: argument 3: TypeError: wrong type` (đo) ⇒ trên Windows là CANH_BAO + mồ côi; đồ giả `getattr(p, "_obj", p)` nhận cả struct trần. Finding DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES |
| N_C Create argtypes `()` | t64_ | `SONG`  | sống — tương đương (ctypes thật nhận đối số thừa, `None`→NULL, trả handle đúng — đo) |
| R1 khối phóng lại `if False:` | t62_ | `GIET_DUNG_NHAN` chạy làm __main__ với PYTHONUTF8=0 mà tiến trình chạy bộ ca KHÔNG ở chế độ UTF-8: 'UTF8_MODE=0  | giết thật |
| R3 `sys.argv` thay `sys.orig_argv[1:]` | t62_ | `GIET_DUNG_NHAN` (2) cờ `-B` mất ở lần phóng lại: 'UTF8_MODE=1 B=0 DA_PHONG_LAI=1 DAU_SOT=0' | giết thật |
| R4 `.get` thay `.pop` | t62_ | `GIET_DUNG_NHAN` (3) dấu phóng lại còn trong môi trường của bản phóng lại: 'UTF8_MODE=1 B=1 DA_PHONG_LAI=1 DAU_S | giết thật |
| R5 bỏ `-X utf8` | t62_ | `GIET_DUNG_NHAN` (4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc=1 '' 'cong_cu_test: | giết thật |
| R6 bỏ `_DA_PHONG_LAI or` | t62_ | `GIET_DUNG_NHAN` (5) đã mang dấu phóng lại mà vẫn ngoài UTF-8 phải DỪNG, không phóng tiếp: rc=5 'UTF8_MODE=1 B=1 | giết thật |
| R7 bỏ `not isfile` | t62_ | `GIET_DUNG_NHAN` (6) `python -B - --tu-kiem-che-do-utf8 < cong_cu_test.py` ngoài UTF-8 phải DỪNG ồn ào, không ch | giết thật |
| R8 bỏ `__name__ == "__main__"` | t61_ | `GIET_DUNG_NHAN` (e) NẠP cong_cu_test.py mà người nạp bị PHÓNG LẠI — chốt `__main__` mất: rc=0 stdout=b'(0) nap\ | giết thật |
| R9 không đặt dấu | t62_ | `GIET_DUNG_NHAN` (4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc=5 'UTF8_MODE=1 B=1  | giết thật |
| R10 từ chối nhưng thoát 0 | t62_ | `GIET_DUNG_NHAN` (5) đã mang dấu phóng lại mà vẫn ngoài UTF-8 phải DỪNG, không phóng tiếp: rc=0 '' 'cong_cu_test | giết thật |
| P0 t62 bỏ `-B` ở (0) | t62_ | `GIET_DUNG_NHAN` (2) cờ `-B` mất ở lần phóng lại: 'UTF8_MODE=1 B=0 DA_PHONG_LAI=1 DAU_SOT=0' | giết thật |
| P4 t62 bỏ `-B` ở (4) | t62_ | `GIET_DUNG_NHAN` (4) gọi `-X utf8=0` mà không ra UTF-8 (giữ `-B`) sau đúng MỘT lần phóng: rc=5 'UTF8_MODE=1 B=0  | giết thật |
| C1 gỡ khoá `--tu-kiem-che-do-utf8` khỏi `_CUA` | t62_ | `TIN_DUNG_GIA` giàn giáo hỏng (chưa tới chốt nghiệp vụ): cửa --tu-kiem-che-do-utf8 không in gì: rc=2 'er.\n/tm | tín dụng giả — kỳ vọng (fail-closed: suite ĐỎ, không xanh) |
| C2 cửa UTF-8 thoát 0 | t62_ | `GIET_DUNG_NHAN` (1) mã thoát KHÔNG đi qua lần phóng lại: rc=0, chờ 5 | giết thật |
| M60a `r"""`→`"""` (bash_nen, spec §6.3 i) | t60_ | `GIET_DUNG_NHAN` (1) bash_nen.py biên dịch kèm cảnh báo: SyntaxError: invalid escape sequence '\(' (bash_nen.py, | giết thật |
| M61a gỡ reconfigure | t61_ | `GIET_DUNG_NHAN` (a) stdout của tiến trình nạp không mang chữ Việt UTF-8: rc=1 stdout=b'(0) nap\nNAP_OK\n' stder | giết thật |
| M61b gỡ env cho con (spec §6.3 ii) | t61_ | `GIET_DUNG_NHAN` (b) cháu (không `env=`) không in được byte UTF-8 thật: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe | giết thật |
| M61c chỉ stdout | t61_ | `GIET_DUNG_NHAN` (c) stderr của tiến trình nạp không mang chữ Việt UTF-8 THẬT: rc=0 stdout=b'(0) nap\nNAP_OK\n(a | giết thật |
| M61d bỏ PYTHONUTF8 | t61_ | `GIET_DUNG_NHAN` (d) cháu phải ở UTF-8 mode, PYTHONUTF8=1, PYTHONIOENCODING=utf-8: rc=0 stdout=b'(0) nap\nNAP_OK | giết thật |
| M61e con `ascii:backslashreplace` | t61_ | `GIET_DUNG_NHAN` (b) cháu (không `env=`) không in được byte UTF-8 thật: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe | giết thật |
| M61f bỏ hasattr | t61_ | `GIET_DUNG_NHAN` (f) luồng KHÔNG có `reconfigure` làm `_ep_utf8` ném: rc=0 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\ | giết thật |
| M61g `errors="strict"` | t61_ | `GIET_DUNG_NHAN` (g) in surrogate lạc phải ra chữ thoát, không ném: rc=1 stdout=b'(0) nap\nNAP_OK\n(a) ch\xe1\xb | giết thật |
| M49a bỏ `oid.returncode` | t63_ | `GIET_DUNG_NHAN` (hash-object/rc) bằng chứng stage hỏng mà t49 không BỎ QUA đúng bước (chờ 'rc=128/0'): None | giết thật |
| M49d bỏ `ga.returncode` | t63_ | `GIET_DUNG_NHAN` (add/rc) bằng chứng stage hỏng mà t49 không BỎ QUA đúng bước (chờ 'bình_thường'): None | giết thật |
| T64 gỡ chốt (k3) + M4 | t64_ | `SONG`  | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| T64 (k2) nhận cả 241 + M3 | t64_ | `SONG`  | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |
| T64 t64 bỏ `preexec_fn`, chạy dưới SIGINT=SIG_IGN | t64_ | `GIET_DUNG_NHAN` (k3) tiến trình chạy bộ ca 12934 LỜ SIGINT/Ctrl-C: 'PID=12934 U8=1 PL=1 INT=0\n' | giết thật (đỏ oan khi chạy nền — preexec_fn gánh) |
| HEAD head, chạy dưới SIGINT=SIG_IGN (đối chứng) | t64_ | `SONG`  | sống — KỲ VỌNG (tương đương / chứng minh chốt có răng) |

**Lô 2 — cùng các đột biến Windows trên nền đồ giả MỚI (nháp `tam/ram/f2`: mỗi API là hàm C thật qua `CFUNCTYPE`, = HINT hunk 3):**
`tam/log/db-f2.jsonl` — W1, W2, W3, W4, W6 (nay chết bằng handle > 32 bit bị `c_int` mặc định cắt THẬT), W7, W8, W9, W11, W12, W13,
M1, M5, M6 ⇒ giết đúng nhãn như lô 1; W5 chỉ-trường/W10/W14/N_A/N_C ⇒ sống (tương đương, như lô 1); **N_B ⇒ giết bằng (w1)
"… CANH_BAO_MO_COI … (ArgumentError …)"** (lô 1: sống). M60a/M61a/M61b vẫn giết đúng nhãn (đồ giả không chạm `t60`/`t61`).
Lô 3 (cây HINT đầy đủ): xem mục HINT.patch — tự kiểm.

**Ngoài lô (đo riêng):** R11 "mất argv khi phóng lại" (HƯỚNG 7): head ⇒ `t64` TREO (giết ở 90 s), `t62` `tin_dung_gia`; W5b "`u32`
64 bit mọi nơi" (đúng dạng W5 executor mô tả) ⇒ struct 152 B (đo) ⇒ đồ giả lẫn Windows thật từ chối kích thước.
Bán kính các đột biến #668 bởi ca mới: `mot_db.py` 9 đột biến dispatcher ⇒ `ok … 1/61` (không ca #671 nào chết thêm); trọn 416 qua
16 mảnh: BẢNG ĐO.

## BẢNG ĐO
| khẳng định | executor khai | đo được | khớp? |
|---|---|---|---|
| dòng thêm so merge-base `fc852ff` (trần chủ kho ~400) | +400 (thân commit) | `git diff --numstat fc852ff 0ce1ad3` ⇒ `1 1 ops/bash_nen.py` + `399 41 ops/cong_cu_test.py` = **+400/−42** | khớp (đúng trần) |
| PR so master chỉ 2 tệp | có | `git diff --stat fc852ff 0ce1ad3` ⇒ 2 files changed | khớp |
| vá 6 so `8757a84` | (BAO_CAO §2: 113/7 trước khi điều phối áp HINT lượt 5) | `122 15 ops/cong_cu_test.py` (commit) — khác vì phiên điều phối áp thêm HINT lượt 5 + nén chú thích | khớp (hai cây khác nhau, đã khai) |
| "f25_cua_moi_vi_tri ⇒ ok ban kinh 1/61; f13/f25b/f27/f28 1/61" | có | `mot_db.py` trên head: 9/9 `ok … bán kính 1/61`; A/B cùng lệnh: `8757a84` ĐỎ tín dụng giả (`t62`), `fc852ff` `ok … 1/56` | khớp |
| "37/37 đột biến giết đúng nhãn" | có | tái dựng cùng tên trên `0ce1ad3` (mỏ neo của tôi): M1–M6, W1–W4, W6–W13, R1, R3–R10, P0, P4, M61a–g, M60a ⇒ tất cả `GIET_DUNG_NHAN` | khớp |
| "3 tương đương sống (W10, W14, R2n)" | có | W10, R2n: sống, tương đương (khớp). **W14: KHÔNG tương đương** — fd 1/2 đóng lúc gọi: head nổ rc=1, W14 chạy (rc=0/3) | **một phần** (P4) |
| W5 "DWORD 64 bit ⇒ (w1)" | có | W5b (`u32` 64 bit MỌI NƠI ⇒ struct 152 B) bị giết; biến thể chỉ-trường `co` thì tương đương thật (byte giống hệt) | khớp (khác mỏ neo) |
| "(w0)(w1)(w2) trên kernel32 giả giữ trạng thái"; BAO_CAO §3 "cách gọi API + trạng thái mô phỏng ĐÓNG" | có | trạng thái: đúng (W-series); cách gọi API: **N_B sống** (đồ giả không chuyển kiểu ctypes) | **không khớp** (P3) |
| con số AST chú thích đầu tệp "38 Call / 5 `{**os.environ}`" | có (thân commit P4) | `0ce1ad3`: **39** Call, `{**os.environ}` **4**, Name+dict(Name) **20** | **không khớp** (P4 tái phát) |
| bảng mồ côi nền/vá (BAO_CAO §3) | nền: kill-9 còn 1, SIGTERM còn 2, SIGTERM bộ ca ⇒ 241; vá: 0, rc=-15 | lượt này: nền còn 2 / 3 / 241; vá 0 / 0 / -15, pid bộ ca = pid harness | khớp (chiều; số tiến trình phụ thuộc thời điểm) |
| "(k3) 45/45 xanh chạy nền" | có | 30/30 (SIGINT=SIG_IGN thật, `trap '' INT`) + 30/30 (shell harness) dưới tải 21–23; 0 sót | khớp |
| "t62 không đổi dòng nào" | có | sha256 AST `t62` `8757a84` = `0ce1ad3` (`1b80a7b2…`) | khớp |
| "t49 t52 t53 t54 t60-t64 xanh (thường; và LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii qua -X utf8)" | có | vòng CA 16 mảnh (a)/(b) + 2 gate: `60/60 đạt; tổng=61, bỏ qua=1` (t2 — jsonschema); t60–t64 ở đường dẫn chữ Việt+dấu cách × 3 phiên bản × 2 env: 6/6 | khớp |
| ruff `--select F` = nền | có | ruff 0.15.15 `--no-cache --isolated`: tập `fc852ff` = `8757a84` = `0ce1ad3` = {`bash_nen.py` F401 `ast`; `cong_cu_test.py` F841 `ci`} | khớp |
| doctrine-scan sạch | có | `python3.12 -B .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ rc=0 "sạch — đã quét 10 tệp, 0 chỗ chép doctrine" | khớp |
| 0 `.pyc` | có | `t62`+`t64` một mình, con không `PYTHONDONTWRITEBYTECODE` ⇒ 0; mọi lượt đo khác 0 | khớp |
| docstring `_tach_dinh_dang` không đổi byte (spec §2A) | có | `fc852ff` = `8757a84` = `0ce1ad3` = sha256 `3bc957a6…`, 897 ký tự | khớp |
| compile không `SyntaxWarning` | — | `-W error` 2 tệp trên 3.11.15/3.12.3/3.13.12: sạch | khớp |
| mọi dòng thêm ≤ 118 ký tự (lượt 5 đo: có) | — | vá 6: **29 dòng > 118** (max 143); 6 dòng `;`, 5 walrus | quan sát P4 |
| "pha ca: 60/60 đạt" (thân commit) | có | như trên | khớp |
| CI `gate` (`CONG_CU_TEST_BAN_KINH=manh`) trên head — env (a) CI và env (b) qua execve | (không ai khai) | (a) RC=0 · `60/60 đạt; tổng=61, bỏ qua=1` · CỔNG TRÊN CÂY THẬT ĐẠT (nguon_tep=git, blob-index) · TỰ KIỂM SONG SONG (N126) ĐẠT · `SỐ LIỆU: ca=61 · đột biến=416 (giao mảnh) · lỗi đột biến=0` · 1011 s · 0 `.pyc` · status sạch; (b) y hệt, 1008 s | — |
| **trọn bộ dạng MẢNH như CI, env (a) CI** — 8 mảnh THẬT (`PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_MANH=k/8 CONG_CU_TEST_MANH_RA=manh/manh-k.txt`, `TIEN_TRINH=1`), clone riêng `tam/ram/ma/s{k}` @`0ce1ad3`, chạy SONG SONG 22:15:51Z→~23:58Z | (thân commit: "trọn bộ CHƯA chạy hết") | mảnh 0,2–7: RC=0 · vòng CA `60/60 đạt; tổng=61, bỏ qua=1` · 52/52 `ok … bán kính 1/61` · ghi `manh/manh-k.txt` (6109–6149 s dưới tải 18–23); mảnh 1: RC=1 · 51 `ok` + `KHÔNG_ĐO_ĐƯỢC t2_go_canary` (thiếu `jsonschema` — môi trường) ⇒ `[M-loi]`, không ghi tệp. **Bán kính 416: 415 `ok … 1/61` · 1 KHÔNG ĐO ĐƯỢC (môi trường) · 0 ĐỎ**; 0 dòng bán kính nhắc `t60`–`t64` (ca mới không kéo rộng, không tín dụng giả); 0 `rc=141`; `.pyc` 0; status chỉ `?? manh/` | — |
| **trọn bộ dạng MẢNH, env (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii`** — qua `__main__` ⇒ phóng lại bằng execve THẬT ở mỗi mảnh, `tam/ram/mb/s{k}` | — | y hệt (a): 7 mảnh RC=0 52/52, mảnh 1 RC=1 chỉ vì `t2_go_canary` (môi trường); 415 `ok … 1/61` · 1 KHÔNG ĐO ĐƯỢC · 0 ĐỎ; 6093–6149 s | — |
| delta lỗi đột biến so NỀN (spec §6.1 "≤ 0", Linux) | — | head: 1 (`t2_go_canary`, môi trường) ở mỗi env; nền `fc852ff` cùng máy: `mot_db t2_go_canary` ⇒ KHÔNG ĐO ĐƯỢC, loi=1 (cùng nguyên nhân); mọi đột biến còn lại `ok` ⇒ **delta = 0** (lượt 5 trên `8757a84`: +1 do `f25`) | đạt (Linux) |
| gom 7 tệp (thiếu mảnh 1) như job `gate-cong-cu-gop` (`python3.12 ops/cong_cu_test.py --gop manh`, env (a) và (b) — (b) qua execve, argv `--gop manh` giữ nguyên) | — | cả hai: `ĐỎ  gom [G-tap]: tập mảnh [0, 2, 3, 4, 5, 6, 7] ≠ 0..7`, RC=1 — fail-closed đúng thiết kế | — |
| mảnh 1 chạy lại bằng venv (`--system-site-packages` + `jsonschema==4.26.0` đúng pin `ci.yml`, venv đầu PATH), (a) và (b), clone `tam/ram/mv/{a,b}` | — | vòng CA **`61/61 đạt; tổng=61, bỏ qua=0`** (t2 nay ĐO được) · 52/52 `ok … 1/61` kể cả `t2_go_canary → giết đúng 't2_…'` · ghi `manh/manh-1.txt` · RC=0 · 1596 s (tải ~2) · 0 `.pyc`; (b) qua execve giữ python của venv | — |
| **GOM 8/8** như job `gate-cong-cu-gop` (clone sạch @`0ce1ad3`, `python3.12 ops/cong_cu_test.py --gop manh`; 7 tệp mảnh gốc + `manh-1.txt` bản venv; vân tay gom = {sha256 tệp test, HEAD} nên trộn mảnh khác máy/môi trường hợp lệ như CI — KHAI: CI chạy cả 8 mảnh có `jsonschema`) | — | env (a): RC=0 · `GOM MẢNH 8/8` · 416/416 `ok … bán kính 1/61` · 0 ĐỎ · `SỐ LIỆU GOM: ca=61 · đột biến=416 · lỗi đột biến=0`; env (b) qua execve: y hệt, RC=0 (`tam/log/gom-8tep.txt`) | **đạt** (spec §6.5 mô phỏng cục bộ) |

## FINDINGS

### DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES  [P3]  Đồ giả kernel32 của `t64` diễn kịch bản ở tầng ABI (dò CỜ `argtypes is not None`, nhận cả struct trần) ⇒ lỗi GỌI API Windows lọt qua; "cách gọi API … ĐÓNG" rộng hơn phép đo
TỆP/DÒNG: `ops/cong_cu_test.py:2966-2992` (`_k32_gia`: `api()` :2972-2975 trả `f(*a)` khi `goi.argtypes is not None`
và — riêng hai API trả HANDLE — `goi.restype is ctypes.c_void_p`; `dat()` :2977-2980 `c = getattr(p, "_obj", p)`); lời khai: BAO_CAO vòng 6
§3 tiêu đề "Windows: **cách gọi API** + trạng thái mô phỏng ĐÓNG", docstring `_k32_gia` "không diễn kịch bản".
VẤN ĐỀ: phần TRẠNG THÁI của đồ giả là thật (bảng job, cờ đọc từ byte 16..20, thành viên, kế thừa khi phóng, SILENT_BREAKAWAY) — W1–W4,
W7–W13 chết đúng nhãn. Nhưng tầng CHUYỂN KIỂU của ctypes — chỗ lỗi gọi Win32 bằng ctypes thực sự sống — bị thay bằng một luật viết
tay: hàm giả là hàm Python, `argtypes`/`restype` sản phẩm khai chỉ được dò CÓ MẶT, không được áp. Đo: **N_B** (truyền `gh` thay
`ctypes.byref(gh)` cho `SetInformationJobObject`) ⇒ `t64` XANH trên head; cùng lời gọi qua ctypes THẬT (hàm C dựng bằng `CFUNCTYPE`
chữ ký Win32, sản phẩm tự gán argtypes như với WinDLL) ⇒ `ArgumentError: argument 3: TypeError: wrong type` ⇒ trên Windows thật đó là
`CANH_BAO_MO_COI` + không Job ⇒ MỒ CÔI — đúng lớp lỗi vá 6 sinh ra để đóng, và ca khoá của nó xanh. Cùng cơ chế, đo: **N_H** `byref(gh, 16)` (ctypes
thật truyền địa chỉ lệch 16 ⇒ nhân đọc `LimitFlags` sai chỗ = 0 ⇒ mồ côi) ⇒ head `SONG` (`dat` lấy `_obj`, bỏ qua offset). Không phải "khai thiếu" (W6 — bị bắt) mà "khai/đưa SAI" thì
đồ giả mù. Vì mọi hành vi Windows ở đây là KHÔNG ĐO ĐƯỢC, đồ giả là bằng chứng DUY NHẤT trước merge cho nhánh Windows trong CI Linux —
đúng bài học CLAUDE.md "đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch bản", ở chiều ABI.
VÁ Ở ĐÂU: `_k32_gia` (mã TEST — HINT mức mã đầy đủ).
VÁ THẾ NÀO: mỗi API giả là hàm C THẬT: `ctypes.CFUNCTYPE(<chữ ký Win32 thật>)(callback)` rồi ép thành một con trỏ hàm `CFUNCTYPE(c_int)`
trần để SẢN PHẨM tự gán `argtypes`/`restype` — ctypes chuyển kiểu đúng như với WinDLL; handle giả > 32 bit (`1 << 60` trên x64) để
`restype` mặc định `c_int` cắt là hỏng THẬT; `dat` đọc cờ tại ĐỊA CHỈ ctypes truyền sang (`string_at(p + 16, 4)`), kích thước so hằng
tài liệu 144/112. Bỏ các luật viết tay (`argtypes is not None`, `restype is c_void_p`, `_obj`). Giữ nguyên phần trạng thái.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (w1)/(w2). Sau vá: N_B ⇒ (w1) "… CANH_BAO_MO_COI … (ArgumentError …)" (đo trên nháp `f2` và cây HINT); N_H ⇒ (w1) (cây HINT); W6 ⇒ vẫn
(w1) nhưng nay qua handle bị `c_int` cắt thật; W1–W4, W7–W13, M1, M5, M6 ⇒ giết đúng nhãn như cũ (đo, lô 2); W5b ⇒ (w1). Phải VẪN
SỐNG (tương đương thật, đo): N_A, N_C, W5-chỉ-trường, W10.
BẢN VÁ CÓ THỂ ĐẺ RA: (1) lỗi trong lambda giả chạy trong callback ctypes bị in "Exception ignored…" và trả 0 ⇒ trông như API hỏng ⇒
(w1)/(w2) ĐỎ (fail-closed, không xanh giả); (2) trên Windows thật `t64` (w*) cũng chạy đồ giả này: con trỏ `CFUNCTYPE` là cdecl ở cả
hai đầu nên nhất quán (x64 chỉ một quy ước gọi) — KHÔNG ĐO ĐƯỢC ở đây; (3) +13/−13 dòng (trung hoà trần); (4) đồ giả vẫn KHÔNG mô
phỏng kế thừa handle, `BREAKAWAY_OK`, job lồng — những thứ ấy vẫn chỉ đo được trên Windows ((k1) thật).
HINT (hunk nào): hunk 3 (`@@ -2965`, khối `_k32_gia`).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm".
ĐỘ TIN: cao cho khẳng định "đồ giả che N_B" (đo hai chiều: head xanh, ctypes thật ném); vừa cho mức hạng (P3 vì lời khai rộng hơn
phép đo; không có lỗi sản phẩm hiện hành — khai báo ABI hiện tại đúng tài liệu: `(vp,vp)→vp`, `(vp,i,vp,u32)→i`, `(vp,vp)→i`, `()→vp`).

### TU-PHONG-LAI-KHONG-TRONG-SUOT  [P4]  (biểu hiện (d), MỚI do vá 6) fd 1/2 đóng lúc gọi ⇒ dòng xả đệm nổ `AttributeError` TRƯỚC khi phóng (đường cũ chạy); "W14 tương đương" sai ở góc này
TỆP/DÒNG: `ops/cong_cu_test.py:49` (`return sys.stdout.flush() or sys.stderr.flush() or execve(...)`); nhánh Windows `:64`
(`sys.stderr.write(...)` trong `except`); lời khai: BAO_CAO §4 hàng "TƯƠNG ĐƯƠNG … W14 bỏ xả đệm (chưa `print` gì trước exec)",
DUONG_VAO hàng 18.
VẤN ĐỀ: (b) mồ côi và (c) mã 241 của lớp này ĐÃ ĐÓNG trên POSIX (HƯỚNG 1). Nhưng bản vá sinh một biểu hiện mới cùng cơ chế "phóng lại
không trong suốt": khi fd 1 hoặc 2 đóng lúc khởi động (`>&-`, `2>&-`, daemon/harness đóng stdio), Python đặt `sys.stdout`/`sys.stderr`
= `None`; `8757a84` vẫn phóng và chạy (rc=0 / rc=3 của đầu dò), `0ce1ad3` nổ `AttributeError: 'NoneType' object has no attribute
'flush'` (rc=1; với `2>&-` KHÔNG in gì) — HƯỚNG 2 S10/S11. Xả đệm ở đây cũng thừa: `_ep_utf8()` đã `reconfigure` (xả) cả hai luồng, và
S12 (sitecustomize in trước khi phóng) giữ đủ 2 dòng cả khi bỏ xả đệm. Fail-closed (rc≠0), nên P4. Nhánh Windows: `sys.stderr` là
`None` dưới `pythonw`/không std handle ⇒ `sys.stderr.write` trong `except` cũng nổ (suy từ mã; KHÔNG ĐO ĐƯỢC).
VÁ Ở ĐÂU: `_phong_lai` (mã SẢN PHẨM của packet — HINT chỉ là GỢI Ý HƯỚNG) + `t64` (mã TEST — đầy đủ).
VÁ THẾ NÀO: xả đệm bỏ qua luồng `None`: `return any(s.flush() for s in (sys.stdout, sys.stderr) if s) or execve(...)` (một dòng, trung
hoà); nhánh Windows (hướng, không hunk — không đo được): `sys.stderr and sys.stderr.write(…)`.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: `t64` (k4) — POSIX, `for fd in (1, 2)`: chạy phần đầu với `preexec_fn=lambda: os.close(fd)`, đòi rc=0.
Đo trên nháp `f3`: hoàn nguyên dòng head ⇒ `(k4) fd 1 …` (giết đúng nhãn); chỉ bảo vệ stdout ⇒ `(k4) fd 2 …` — mỗi fd một chốt, phân biệt
được bằng đầu vào. W14 (bỏ hẳn xả đệm) ⇒ sống (nay TƯƠNG ĐƯƠNG thật).
BẢN VÁ CÓ THỂ ĐẺ RA: (k4) chỉ POSIX (`preexec_fn`); +4 dòng; +2 tiến trình con mỗi lần `t64` (~0,2 s). `preexec_fn` chạy khi các luồng
đọc của (k1) đã `join` xong.
HINT (hunk nào): hunk 2 (sản phẩm — gợi ý hướng), hunk 5 (test).
ĐÃ THỬ NGHIỆM HINT: xem "HINT.patch — tự kiểm". ĐỘ TIN: cao (A/B cùng lệnh l5/h; W14 đo; (k4) đo có răng từng fd).

### CA-KHOA-T64-TREO-THAY-VI-DO  [P4]  `t64` đọc dòng đầu KHÔNG hạn chót ⇒ hồi quy "mất argv khi phóng lại" làm bộ ca TREO tới trần job thay vì ĐỎ
TỆP/DÒNG: `ops/cong_cu_test.py:3016` (`dau, rc = p.stdout.readline()…`); worker bán kính `_phong_con` `p.wait()` không hạn chót (:7505-7507).
VẤN ĐỀ: mọi chờ khác của `t64` có hạn (join 10/60 s, wait 10 s, co.wait 15 s) trừ dòng đầu. Đo R11 (bỏ `*sys.orig_argv[1:]` khỏi lệnh phóng
lại ⇒ bản phóng lại thành REPL đọc ống stdin của `t64`): `t64` TREO (bị giết ở 90 s, không dòng kết quả); `t62` ⇒ `tin_dung_gia`. Trong CI:
job `gate` (60′) / mảnh (30′) bị huỷ ở trần — đỏ nhưng mất chẩn đoán, tốn trọn trần phút. Hiện 0/416 DOT_BIEN chạm phần đầu tệp nên bán
kính CI không đi vào đường này; nó là đường của một hồi quy TƯƠNG LAI ở khối phóng lại — đúng thứ `t64` sinh ra để khoá.
VÁ Ở ĐÂU: `t64` (mã TEST — đầy đủ). VÁ THẾ NÀO: `(hen := threading.Timer(120, p.kill)).start()` trước `readline()`, `hen.cancel()` sau.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: R11 phải chuyển từ "treo" thành ĐỎ có tên trong ~120 s — đo trên nháp `f3`: `tin_dung_gia` "giàn giáo:
phần đầu không phóng lại sang UTF-8 — không đo gì: ''" sau 120,04 s, 0 tiến trình sót.
BẢN VÁ CÓ THỂ ĐẺ RA: máy quá tải tới mức dòng đầu > 120 s ⇒ `t64` đỏ oan (đo bình thường 0,86–3,3 s dưới tải 20–23: biên ~40×); +2 dòng.
HINT (hunk nào): hunk 4. ĐỘ TIN: cao.

### DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI  [P4]  Đồ giả `popen` báo hiệu (`k.co.set()`) TRƯỚC khi ghi con vào tập thành viên job ⇒ (w1) có cửa sổ đỏ oan
TỆP/DÒNG: `ops/cong_cu_test.py:2983-2985` (`_k32_gia.popen`); người đợi: `t64` `k.co.wait(15); k.cha_chet(); th.join(10)` (:3039).
VẤN ĐỀ: HƯỚNG 13 — nới cửa sổ giữa `set()` và dòng ghi thành viên ⇒ (w1) ĐỎ OAN; đảo thứ tự ⇒ xanh với cùng cửa sổ. Tự nhiên hiếm
(0/60+), nhưng đúng loại chập chờn mà prompt (iv) hỏi: đỏ oan dưới tải trên một ca khoá, không có đột biến nào.
VÁ Ở ĐÂU / THẾ NÀO (mã TEST — đầy đủ, gộp trong hunk 3 vì cùng khối): `k.con.append(Popen(...))` → ghi thành viên → `return k.co.set() or
k.con[-1]` (báo hiệu SAU khi trạng thái đã ghi). Trung hoà dòng.
CA KHOÁ + ĐỘT BIẾN PHẢI CHẾT: không có ca tự động cho một cuộc đua (phép đo là nới cửa sổ, như trên); đột biến "dời `set()` về trước" chỉ
chết dưới cửa sổ nới rộng — nói thẳng: đây là vá theo lập luận thứ tự + một phép nới cửa sổ, không phải ca khoá.
BẢN VÁ CÓ THỂ ĐẺ RA: không đổi ngữ nghĩa khác (`k.exec`/`execve` giả đã ghi trước khi `set()`). HINT: hunk 3 (C3). ĐÃ THỬ NGHIỆM HINT: v2 + nới cửa sổ ⇒ `qua`; lô rút gọn v2 giữ mọi nhãn. ĐỘ TIN: cao (cơ chế + phép nới).

### LOI-KHAI-RONG-HON-PHEP-DO  [P4]  (tái phát lần 2 — do chính vá 6) Con số AST vừa sửa đã trôi trong cùng commit: "38 Call … 5 `{**os.environ}` … 18 biến" nay là 39 / 4 / 20
TỆP/DÒNG: `ops/cong_cu_test.py:15-16`.
VẤN ĐỀ: vá 6 áp HINT lượt 5 hunk 1 (số đo trên `8757a84`) VÀ cùng lúc đổi điểm phóng: bỏ `subprocess.run(env={**os.environ, _DAU…})`,
thêm `popen(lenh, env=env)` (`_phong_lai`) và `subprocess.Popen(…, env=env)` (`t64`). `tam/cu/dem_env.py` trên `0ce1ad3`: 39 Call {Name 19,
dict(Name) 1, moi_truong 12, dict(os.environ) 3, `{**os.environ}` 4}. Tính chất (mọi `env=` truy về `os.environ`/`None`) vẫn đúng; số hạng
sai. Lần thứ BA lớp này rơi vào đúng câu này — "một bất biến còn đúng không chứng minh các số hạng còn đúng".
VÁ Ở ĐÂU: chú thích `:15-16`. VÁ THẾ NÀO (HINT hunk 1): bỏ số đếm, giữ tính chất + cách đo ("AST, mọi Call có `env=`") và nói rõ CỐ Ý
không ghi số vì nó trôi ở mỗi điểm phóng mới. Nếu muốn giữ số: đo trên cây CUỐI và neo SHA.
CA KHOÁ: không (chú thích). BẢN VÁ CÓ THỂ ĐẺ RA: mất con số cho người đọc (đo lại bằng AST); trung hoà dòng. ĐỘ TIN: cao.

### NGHIEM-THU-WINDOWS-CON-THIEU  [P2]  Chưa có nghiệm thu §6 trên Windows neo exact head — và nhánh Windows MỚI của `_phong_lai` chưa từng chạy trên Windows
TỆP/DÒNG: spec §2B, §6.1–6.3; `ops/cong_cu_test.py:50-66` (nhánh `nt`); BAO_CAO §6.
VẤN ĐỀ: giữ (1)–(4) của lượt 5 (không log/receipt Windows cho `c5f3da0`/`8757a84`/`0ce1ad3`; giả thuyết B chưa đo; mảnh/gom #668 trên Windows;
(4) mô phỏng "nền từ chối `\xff`" ⇒ `t63` ĐỎ OAN — TÁI HIỆN lượt này trên CẢ `8757a84` lẫn head: `t49` `bo_qua` đúng spec, `t63`
`giet_that` "(ops/no_cu.py/rc) … chờ 'no_cu'"). MỚI: (5) toàn bộ nhánh Job Object (ctypes, `KILL_ON_JOB_CLOSE`, tự gán TRƯỚC khi phóng,
lồng job dưới `py.exe`/runner) là mã chưa chạy trên Windows lần nào; (k1) thật của `t64` sẽ là lần đo đầu tiên; (6) thời lượng `t64` trên
Windows (tạo tiến trình đắt) trong trần mảnh 30′ — KHÔNG ĐO ĐƯỢC.
VÁ Ở ĐÂU / THẾ NÀO: nghiệm thu (hiện vật) trên máy Windows local neo head SAU khi vá: `python ops\cong_cu_test.py` KHÔNG đặt `PYTHONUTF8`
(đi nhánh Job) ⇒ N/N + danh sách bỏ qua; cùng bộ với `PYTHONIOENCODING=ascii PYTHONUTF8=0`; §6.3 (i)(ii); log staging `t49`; `t64` (k1)
thật; thử `taskkill /F` tiến trình bao trong lúc chạy ⇒ đếm con còn sống. CA KHOÁ: không áp dụng (nghiệm thu). BẢN VÁ CÓ THỂ ĐẺ RA: không.
HINT: không có hunk — KHÔNG vá được bằng mã ở Linux (chủ kho: "Chỉ chạy tại máy"). ĐỘ TIN: cao (đối chiếu hiện vật + mô phỏng tái hiện).

### TEN-CA-LECH-SPEC  [P4]  Ca khoá mang tên `t60`–`t64` thay vì `t52` của spec (quyết định chủ kho: khai ở PR)
TỆP/DÒNG: `ops/cong_cu_test.py:2846` (`t60_…`), `t61`, `t62`, `t63`, **`t64` (mới, spec không có)**; spec §2A/§6.3.
VẤN ĐỀ/VÁ: khai ở thân PR ánh xạ `t52`(spec)→`t60`; "ca khoá UTF-8"→`t61`+`t62`; `t63`, `t64` là ca mới (t64 = lớp mồ côi, ngoài spec r1 —
theo quyết định chủ kho 2026-09-30); `t52`–`t54` trong tệp là của #668. CA KHOÁ/HINT: không. ĐỘ TIN: cao; thân PR KHÔNG ĐO ĐƯỢC.

### TRAN-DONG-DAT-BANG-NEN  [P4]  Trần +400 đạt bằng NÉN mã chứ không bằng thu hẹp — chi phí đọc chuyển sang người duyệt `human_audited`
TỆP/DÒNG: diff `8757a84..0ce1ad3` (vá 6): 122 dòng thêm, trong đó 29 dòng > 118 ký tự (vá 5 + merge: 0), 6 dòng nhiều lệnh (`;` thật theo
`tokenize`), 5 walrus, 1 list-comprehension làm hiệu ứng phụ; BAO_CAO §1 tự khai "441 ⇒ nén … ⇒ 396", thân commit "+400".
VẤN ĐỀ: không sai chức năng, nhưng trần ADR-0044 (nâng lên ~400) tồn tại để giới hạn tải duyệt; nén để lọt trần giữ con số, không giữ
mục đích (vd. `p.kill(); (doc := threading.Thread(target=p.stdout.read)).start(); doc.join(10)` một dòng). Kho không có luật độ dài dòng
(master sẵn 232 dòng > 118), nên đây là quan sát cho chủ kho, không phải vi phạm quy tắc.
VÁ Ở ĐÂU/THẾ NÀO: quyết định chủ kho — hoặc chấp nhận, hoặc đổi thước (vd. đếm câu lệnh logic) cho packet này. HINT lượt này KHÔNG nén
thêm: các hunk 1/2/3 trung hoà dòng bằng thay thế, 4/5 cộng thật +6 (⇒ +406, vượt trần — chủ kho quyết, xem HINT). ĐỘ TIN: cao (đo).

## HINT.patch — tự kiểm

- Tệp: `out/HINT.patch` (**v2 — bản CUỐI**, 112 dòng, sha256 `f45b06691ec6a4fc450100211dd5532f1266dfc89b0c3bdfae0f371c61b019b1`) — 5 hunk,
  MỘT tệp `ops/cong_cu_test.py`, định dạng `git diff --no-prefix` (đường dẫn repo-relative, không `a/`/`b/`); đầu tệp mang nhãn §8
  NGUYÊN VĂN ("chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit") và bảng phân loại hunk. Hunk 3/4/5 là mã
  TEST đầy đủ; hunk 2 chạm `_phong_lai` = MÃ SẢN PHẨM của packet ⇒ CHỈ LÀ GỢI Ý HƯỚNG; hunk 1 là chú thích. Không hunk nào chạm
  `bash_nen.py`, `main()`, `_main_gop()`, `_CUA`, `.github/workflows/**`, hay đường CI gọi (CI đặt `PYTHONUTF8=1` ⇒ không đi `_phong_lai`).
  Ánh xạ: hunk 1 = LOI-KHAI [P4] · 2 = TU-PHONG-LAI (d) [P4] · 3 = DO-GIA-KERNEL32-BO-QUA-TANG-CTYPES [P3] + DO-GIA-BAO-HIEU-TRUOC-TRANG-THAI
  [P4] · 4 = CA-KHOA-T64-TREO-THAY-VI-DO [P4] · 5 = ca khoá (k4) của hunk 2.
- Lệnh tự kiểm BẮT BUỘC (nguyên văn prompt; `tam/ap` clone MỚI từ `kho.git`, trên đĩa; chạy lại cho v2 lúc ~00:01Z):
  ```
  $ git clone -q kho.git tam/ap && git -C tam/ap checkout -q --detach 0ce1ad3 && cd tam/ap && patch -p0 --fuzz=0 --dry-run < ../../out/HINT.patch
  checking file ops/cong_cu_test.py
  dry_run_rc=0
  $ patch -p0 --fuzz=0 < ../../out/HINT.patch    ⇒ patching file ops/cong_cu_test.py · apply_rc=0 · 0 tệp .orig/.rej
  $ cmp ops/cong_cu_test.py <cây HINT v2>          ⇒ trùng từng byte (sha256 tệp 7ecaeb4bb79f91f3…; commit nháp 348484c7 trong tmpfs)
  $ git diff --numstat fc852ff -- ops/           ⇒ 1 1 ops/bash_nen.py · 405 41 ops/cong_cu_test.py ⇒ +406
  ```
- **TRẦN DÒNG**: so head +25/−19. Hunk 1, 2, 3 trung hoà (thay thế) ⇒ áp riêng chúng giữ **+400**; hunk 4 (+2) và 5 (+4) ⇒ áp đủ
  **+406 — vượt trần ~400 của chủ kho 6 dòng ⇒ CHỦ KHO QUYẾT** (nâng thêm 6, hoặc chỉ áp 1–3: khi ấy hunk 2 không có ca khoá và `t64` vẫn
  treo được dưới R11). Dòng thêm dài nhất 125 ký tự (3 dòng > 118, mỗi dòng thay một dòng gốc dài tương đương); token `;` 47 → 46;
  compile `-W error` sạch trên 3.11/3.12/3.13.
- **Trên bản áp v2 `tam/ap`** (`tam/log/kiem-ap-v2.txt`): `t49 t60 t61 t62 t63 t64` ⇒ `TONG {"qua": 6}` ở {thường, `LC_ALL=C PYTHONUTF8=0
  PYTHONIOENCODING=ascii`}; 0 `.pyc`. (R11 v2 + job `gate` env (b) v2: dòng cuối mục này.)
- **Trên cây HINT v2 (`348484c7`)**: `t49 t52 t53 t54 t60`–`t64` ⇒ `qua: 9` × {3.11, 3.12, 3.13} × {thường, env (b)} = 6/6; lô rút gọn 16 đột
  biến (`tam/log/db-v2.jsonl`) ⇒ 14 giết đúng nhãn (N_B, N_H, W5b, W1, W2, W4, W6, W8, W13 ⇒ (w1)/(w2); K4 ⇒ `(k4) fd 1`; K4b ⇒ `(k4) fd 2`;
  M1 ⇒ (k1); M4 ⇒ (k3); M6 ⇒ (w0)) + W10 / đối chứng chạy nền sống; nới cửa sổ 0,2 s trước `k.co.set()` ⇒ `qua` (head cùng phép ⇒ ĐỎ oan).
- **Trên cây HINT v1 (`8e354193` = v2 trừ C3 — thứ tự báo hiệu; mọi kết quả dưới không phụ thuộc C3)**: lô 44 đột biến (`tam/log/db-hint.jsonl`)
  ⇒ 37 giết đúng nhãn (gồm N_B, N_H, W5b ⇒ (w1); K4/K4b ⇒ (k4) từng fd; M1–M6; W1–W4, W6–W9, W11–W13; R1–R10; P0; P4; C2; M60a; M61b;
  bỏ `preexec_fn` chạy nền ⇒ (k3)) · 6 sống kỳ vọng (R2n, W10, W14 — nay tương đương thật —, hai phép ghép "gỡ chốt + đột biến", đối chứng
  chạy nền) · C1 tín dụng giả kỳ vọng · 0 ca khác đỏ. R11 ⇒ `tin_dung_gia` sau 121 s, 0 sót (head: treo). Job `gate` env (b) trên bản áp v1:
  RC=0 · `60/60` · CỔNG TRÊN CÂY THẬT ĐẠT · TỰ KIỂM SONG SONG ĐẠT · lỗi đột biến 0 (957 s). Mẫu bán kính `mot_db`: `f25_cua_moi_vi_tri`,
  `f13_dispatcher_nuot` ⇒ `ok … 1/61`; `t2_go_canary` ⇒ KHÔNG ĐO ĐƯỢC (môi trường, như head) ⇒ ca mới/đồ giả mới không kéo rộng bán kính.
- **v2 trên bản áp `tam/ap`**: R11 (mất argv) ⇒ `t64` `tin_dung_gia` "giàn giáo: phần đầu không phóng lại sang UTF-8 …" sau **120 s**, 0 tiến
  trình sót (head: treo tới khi bị giết); job `gate` env (b) (`CONG_CU_TEST_BAN_KINH=manh`, qua `__main__` ⇒ execve) ⇒ RC=0 · `60/60 đạt;
  tổng=61, bỏ qua=1` · CỔNG TRÊN CÂY THẬT ĐẠT (cổng đọc INDEX ⇒ thay đổi HINT được stage trong bản sao) · TỰ KIỂM SONG SONG ĐẠT · `lỗi đột
  biến=0` · 203 s · 0 `.pyc` · status 1 dòng = chính `M ops/cong_cu_test.py` của HINT.

## KHÔNG ĐO ĐƯỢC

- **Mọi hành vi Windows**: Job Object THẬT (TerminateProcess cha ⇒ handle đóng ⇒ con chết; lồng job dưới runner/`py.exe`; handle không
  kế thừa), `t64` (k1) trên Windows, `sys.orig_argv` qua `py`/venv launcher, Ctrl-C console, MSYS/Cygwin python, thời lượng `t64`/mảnh
  trên `windows-latest`, Git for Windows với tên `\xff`/`\` (spec §8). Bố cục x86 (112 B) chỉ tính tay theo quy tắc căn lề MSVC.
- **CI thật trên GitHub** (không gọi mạng): mọi kết luận mảnh/gom là MÔ PHỎNG cục bộ đúng lệnh + env `ci.yml`. Khác runner: máy này
  KHÔNG có `jsonschema` hệ thống (mảnh 1 gốc: `t2_go_canary` KHÔNG ĐO ĐƯỢC) — đã bù bằng venv có `jsonschema==4.26.0` CHỈ cho lượt chạy lại
  mảnh 1; `shellcheck` vắng (không bắt buộc); `PyYAML` 6.0.1 (CI 6.0.3). `gate-cong-cu-gop (ubuntu-latest)` có trong ruleset chưa: KHÔNG ĐO ĐƯỢC.
- **Thân PR #690 / handoff vòng 6**: ánh xạ tên ca, `hint_provenance` (hunk lượt 5 do phiên điều phối áp) — người đẩy phải khai.
- **Model/effort thật của executor**: thân commit tự khai "Claude Opus 5.5"; BAO_CAO dừng ở mục 7 (agent bị cắt 4 giờ).
- **Thẩm quyền ghi** của phiên tạo `0ce1ad3` (trailer `Claude-Session: …session_014dEtdMqShJhdQ8JfNbEeLU` — phiên lease g1, g2 ghi
  `environment: local` Windows): hiện vật không chứng minh theo chiều nào — chủ kho/người land xác nhận.
- **Sự cố rig trong lượt (khai trước)**: lần kiểm đầu "R11 + lô đột biến trên cây HINT" (23:07–23:20Z) nhân bản cây HINT bằng
  `git clone --shared` khi thay đổi HINT CHƯA commit ⇒ bản sao mang `0ce1ad3` trần, không mang HINT ⇒ R11 "trên cây HINT" thực chất đo
  lại HEAD (treo tới trần 400 s — đúng hành vi head). Phát hiện vì kết quả trái với nháp `f3` (đỏ ở 120 s); kiểm `grep -c "hen :="` trên bản
  sao ⇒ 0. Đã dừng lô sai (1 dòng, đổi tên `tam/log/db-hint-SAI-NEN-head.jsonl`, không dùng), commit cục bộ cây HINT (`8e354193`, không
  ký, config cục bộ; = `tam/ap` từng byte) rồi chạy lại. Các nền `f2`/`f3` đã commit trước khi nhân bản ⇒ lô 2 và các phép đo `f3` hợp lệ;
  mọi lượt chạy thẳng trên thư mục (`chay_ca`/`mot_db` với `cd`) hợp lệ.
- **Rig**: tmpfs gắn tại `$R/tam/ram` (root, `mount -t tmpfs`) — thay đổi bảng mount của máy trong lượt (tháo khi xong); snapshot chỉ
  chứng minh không có delta ở hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên.
