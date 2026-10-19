verdict: changes_requested
reviewed_sha: 786bf3baf5afa9a5735d79cc06e8f2ca23cda6bd
spec_sha256: e6c3ec0b80eae1c88a78fde17550f8f4454eba115a8205b69ffef29cbc6d1ce9
model/effort tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), effort max — KHÔNG phải codex. Reviewer độc lập thay cho lượt codex, làm đúng `PROMPT.md` r12 với ba khác biệt phiên điều phối nêu: không sửa `cay-kho/` (chỉ ghi dưới `goi/` và các thư mục `mktemp -d -p "$R"`); không đăng GitHub, không commit/push; mạng chỉ `gh api` GET. Máy đo: Xeon 2,10 GHz, 4 lõi, Linux; Python 3.12.3 trong venv có PyYAML 6.0.3 và jsonschema 4.26.0 (hai gói `ci.yml` ghim).
số lớp: 0 P1 · 1 P2 · 0 P3 (1 lớp)

## KẾT LUẬN

Câu hỏi gốc: làm đúng chữ r12 thì PR #721 có xanh CI một cách hợp lệ (không nới tiêu chí, không mất răng), write set có đủ, và r12 có trung thành quyết định chủ kho không?

- **Năm lớp lượt 11: bốn ĐÃ ĐÓNG, một ĐÓNG MỘT PHẦN.** Ba lớp P3 (`chu-cu-con-lai-…`, `so-khai-lech-…`, `s11-…`) là chữ HINT áp nguyên văn: `patch -p0 --fuzz=0` rc=0, 8/8 hunk, bản sau HINT trùng `4dd4b3a9…e8d2` mà §0 (2) khai; số liệu CI của lớp `so-khai-lech-…` tái lập bằng `gh api` (433 job ở T ∈ [01:10:21Z, 01:12:00Z), 424 ở 00:57Z–01:05Z). Lớp `phu-luc-m-khong-chan-dau-vao-sai` đóng: Phụ lục M r12 khớp băm, chạy được, đối chứng dương trên g1 `bfb4ca3` (hai gốc là clone git có HEAD) rc=0 ở mảnh 1 và mảnh 3, các đầu vào sai của lượt 11 nay ra rc=1. Lớp P2 `a10-khong-ghim-so-o-thu-hep-mien-qua-duoc` đóng cho chiều N68 và bảy cây r12 dựng thêm, nhưng cơ chế còn lọt ở **lưới có sẵn** — xem lớp mới.
- **Ba phần ngoài HINT.** (1) A10 (v): mọi con số tái lập (212 · 60 · 162 · 122 · 456 · 121 khoá; bảy cây T1b–T7 đúng bảng §0 (4)); có răng với các chiều đã liệt kê (T1b–T5, T7 đỏ ở (v); N6 và T6 chỉ đỏ ở (iv); N8 xanh cả hai). **Nhưng chưa có răng ở phần có sẵn của chính lưới `_luoi_noi_main`** — một dòng (+1/−1) bỏ 131 trong 508 khoá của `--tu-kiem-main` mà A10 (i)–(v), A4-b, A4-d, 101/101 đột biến đích `t54` và 66 dò đều xanh, và Phụ lục I cho Δ = 0,830 × Δ_g1 (ĐẠT (i)). (2) Phụ lục M r12: khớp băm, đúng, không tự mâu thuẫn với A9. (3) A9 prose khớp mã.
- **Không tiêu chí nào bị nới.** A1–A3, A5–A8 và M1–M7 không đổi một chữ (`difflib` khối §5, §6: §5 chỉ chạm M8; §6 chỉ chạm A4-g, A9, A10); A4-g chỉ thêm một câu của HINT; M8, A9, A10 chỉ chặt thêm; S1–S10 không đổi, S11 theo HINT; Phụ lục A–L trùng byte r10 và r11 (1145 dòng, `e99226fd…3d2b`), khối "Bảng canh" 54, §2, §3, §7 trùng r11.
- **Trung thành quyết định chủ kho `6073703559`: có** (bảy mục, 1839 byte, sha256 `879d26e7…d6c49`); ngân sách CI `1 / 1 / 2` và lease g2 `0 / 1 / 1` không đổi.
- **Một lần vá văn bản (HINT.patch, 3 hunk, dry-run rc=0) đóng lớp duy nhất**; chỉ sửa chữ đặc tả, không đính mã (Q14).

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `a10-v-chi-ghim-o-moi-bo-o-co-san-van-lot` | P2 | A10 (v) ghim số ô của phần MỚI trong `--tu-kiem-main` (122 khoá `noi698-` và 162 khoá `m3698-` trong 508 khoá) nhưng 179 hàng CÓ SẴN từ #668 của cùng hàm `_luoi_noi_main` và 45 khoá khác không được ghim; cha `t54` (dòng 7047) và con `_in_tu_kiem_main` (dòng 8119) dựng từ CHÍNH hàm ấy. Cây `P1a` = g1 với MỘT dòng (+1/−1) `for n in range(2, 17) for k in range(n)` → `for n in (2, 16) for k in (0, n - 1)` bỏ 131 khoá: `t52·t53·t54` 56/56; (iv) và mọi số (v) bằng g1; A4-b, A4-d như g1; 101/101 đột biến đích `t54` (gồm 12 canh) GIẾT đúng ca đích; 63/63 dò đích `t54` đúng hạng đã khai và 3 dò KHÁC vẫn KHÁC; Phụ lục I (g1, P1a, g1, P1a) Δ 6,91 · 6,95 so 8,33 · 9,32 ⇒ **0,830** (i) ĐẠT, `ty_le` 1,29 · 1,31 (iii) ĐẠT. M8 "Cấm bỏ ô" và "Giữ răng" (r12: "số ô, số kịch bản của ba cửa con bằng g1") rộng hơn phép đo | HINT một nhóm, 3 hunk: A10 (v) thêm phép so tập khoá `KQ` của CẢ BA cửa con (g2 ⊇ g1) và độ dài mọi danh sách/từ điển lồng không nhỏ hơn g1 (trừ `kq["m5b"][0]`); thêm `P1a` vào PHẢI ĐỎ Ở; M8 Cấm nêu "ô có sẵn", Giữ răng nêu đúng phép đo | Đo: cửa con, 56 ca, 101 đột biến, 66 dò, ruff, Phụ lục G, Phụ lục I (4 + 3 lượt xen kẽ, lõi 2,3). Giới hạn: 353 dò đích `t52`/`t53` không chạy trên `P1a` (suy luận: cây chỉ đổi lưới của `t54`); đột biến ngoài lát `t54` không chạy; phép so khoá chặn BỎ ô, không chặn thêm ô giả cho đủ số |

## ĐỐI CHIẾU LƯỢT 11

| lớp lượt 11 | trạng thái r12 | phép đo |
|---|---|---|
| `a10-khong-ghim-so-o-thu-hep-mien-qua-duoc` (P2) | **ĐÓNG MỘT PHẦN.** HINT (iv) áp nguyên văn và có răng: cây N6 (quét M1 cho `D698` ở ba neo, sửa S1 của cha) in `m1` = `[237964, 122268, [], 0]` ≠ `[673234, 122268, [], 0]` ⇒ (iv) ĐỎ, trong khi (v) xanh và suite 56/56. r12 thêm (v) và nó có răng ở sáu chiều (T1b, T2, T3, T4, T5, T7 ĐỎ ở (v); T6 chỉ đỏ ở (iv)); tối ưu hợp lệ N8 xanh ở cả hai. Cơ chế còn lọt ở lưới có sẵn ⇒ **lớp mới `a10-v-chi-ghim-o-moi-bo-o-co-san-van-lot`** (không phải hồi quy của bản vá; là chiều thứ bảy của cùng cơ chế) | `dung_cay.py` + `vec_v.py` + `suite_dau.py`; `goi/log/dot_T.out`, `dot_N6.out`, `dot_N8.out` |
| `phu-luc-m-khong-chan-dau-vao-sai` (P3) | **ĐÃ ĐÓNG.** Đối chứng âm: nền thật + gốc hai lần / `ra` tương đối / `ra` trong cây / gốc nền là g1 / ứng viên là `ops/` của nền / clone khác của nền / gốc rỗng ⇒ rc=1 đúng mục `loi` của bảng §0 (5). Đối chứng dương trên g1: xem BẢNG ĐO | `a9_duong_1`, `a9_duong_3`, `am_*.json`, `a9_gia.out` |
| `chu-cu-con-lai-mau-thuan-voi-chu-r11` (P3) | **ĐÃ ĐÓNG.** Bốn chỗ HINT có mặt nguyên văn trong r12 (§4 hàng "CI trong vòng lặp", A4-g, bảng (B) Q7, A10 (ii)); grep không còn chỗ thứ năm nói CI chạy một lần ngoài hàng "chữ r10, giữ để truy dòng dõi" của §7 | `grep` các cụm; `beyond_hint_wdiff.txt` |
| `so-khai-lech-phep-do-o-1-13-2-va-a10` (P3) | **ĐÃ ĐÓNG.** Số liệu của câu sửa đúng: 424 job thành công ở T = 00:57Z, 01:00Z, 01:05Z; 433 và trung vị theo chỉ số `17,79·17,78·17,60·17,57·17,83·17,60·18,02·17,56` chỉ tái lập ở T ∈ [01:10:21Z, 01:12:00Z); job mảnh cuối của các run khác xong 01:10:21Z, mảnh 5 và mảnh 3 của run `37867333230` xong 01:10:07Z và 01:12:00Z. "Khoảng ba phần tư" = 11,6/15 = 0,773 | `ci_thoi_diem.py`; `ci_jobs_57.json` |
| `s11-chi-bao-ca-cam-khong-bao-ca-het-cach` (P3) | **ĐÃ ĐÓNG.** Hunk 7 của HINT có nguyên văn ở S11; §8 chỉ khác r11 đúng ba chỗ (chỉ-trỏ `§0-r11`, một câu r12 ở S5, S11) | `difflib` khối §8 |

## BẢNG ĐO

Lệnh tái lập: script ở `goi/dung-cu/`, đầu ra thô ở `goi/log/` và `goi/so-lieu/`. "Máy này" = máy đo của lượt này. `venv3.12` = `…/x698/venv3.12/bin/python`.

| khẳng định | đặc tả khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| băm đầu vào | `SPEC.md` `e6c3ec0b…`, HEAD `786bf3ba…` | `sha256sum SPEC.md SPEC-r11.md luot11/* r11-r12.diff`; `git -C cay-kho rev-parse HEAD`; `cmp SPEC.md cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r12.md` rc=0 | có |
| r1–r11 giữ nguyên byte | sha256 dòng dõi ở header | `sha256sum cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r*.md`: 11 băm đều bằng băm header (vd r11 `48ac731f…9bb9`) | có |
| HINT lượt 11 áp nguyên văn | rc=0, 8/8 hunk, 4923 dòng, `4dd4b3a9…e8d2`; bản sao đổi đích `17f330f5…515b` | `patch -p0 --fuzz=0 --verbose` trên bản sao r11: `Hunk #1…#8 succeeded at 1833, 2137, 2423, 2679, 2729, 2760, 3088, 3387`, rc=0; `sha256sum` bản sau = `4dd4b3a9…e8d2`; đổi hai dòng `---`/`+++` ⇒ `17f330f5…515b` | có |
| r12 khác r11+HINT chỉ ở danh sách §0 (7) | 44 chỗ | `wdiff.py SPEC-r11+HINT.md SPEC.md`: 44 khối, đều trong danh sách | có |
| Phụ lục A–L, N, bảng canh, §2, §3, §7 không đổi | trùng byte | khối A–L 1145 dòng `e99226fd…3d2b` ở r10, r11, r12; khối N `3ba04375…`; bảng canh `1016e2bd…`; §2 `bdd3b439…`; §3 `1db6c583…`; §7 `d262aba7…` — r11 = r12 | có |
| Phụ lục M r12 | sha256 `2fe67a92…1845`; `numstat` so r11 `43 7`; ruff sạch; 0 TAB, 0 `\` | `trich_khoi.py SPEC.md M`; `git diff --no-index --numstat`; `venv3.12 -m ruff check --select F` (0.15.15): "All checks passed!" | có |
| tập 419 dò ghép | `5d1a4ada…7bc4` | ghép C+H+J+K+L bằng lệnh của các phụ lục: `c6a4db8b…`, `37b6e8bd…`, `bec92f6e…`, `acb8d897…`, `5d1a4ada…` | có |
| **A9 dương, mảnh 1** (Phụ lục M r12, nền `fc852ff` clone git, g1 `bfb4ca3` clone git, `ra` tuyệt đối ngoài hai cây, lõi 0,1; 13:45:52Z–14:19:07Z) | chưa chạy bản r12 trên g1 (§10) | rc=0, `loi` rỗng; nền 803,6 s tường / 1218,8 s CPU, g1 1238,6 s / 1980,8 s; `cuoi` có `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0` và `MẢNH 1/8: 52/52` (nền) / `59/59` (g1) kèm đường tệp mảnh; `r9` **1,5413**, dự báo **31,09** ≤ 33,75; ở trần cũ 30 (ngưỡng 22,5) ⇒ ĐỎ; `blob_nen` `9edea6b1…`, `blob_ung_vien` `9c628700…`; `git status --short` hai gốc rỗng. `loi_khac_dung` 0,73 (các phép đo song song của chính reviewer ở lõi 2,3) | có (spec 1,5158; lượt 11 1,5500) |
| **A9 dương, mảnh 3** (lõi 2,3; 14:16:44Z–14:51:31Z) | — | rc=0, `loi` rỗng; nền 831,8 s / 1266,3 s CPU, g1 1255,3 s / 2007,7 s; `59/59`; `r9` **1,5091**, dự báo 30,44. `loi_khac_dung` 1,64 (các quét song song ở lõi 0,1). R9 = max(1,5413; 1,5091) = **1,5413**, dự báo **31,09** ≤ 33,75. Chạy hai lệnh một mảnh, không một lệnh `45 1 3` | có (spec 1,5248) |
| A9 âm (cây thật làm nền) | §0 (5): Q5–Q11 | `manh_a9_r12.py` với: nền hai lần cùng cây ⇒ `hai_goc_trung_hoac_long_nhau`+`blob_ung_vien`; `ra` tương đối ⇒ `ra_tuong_doi_hoac_trong_cay`; `ra` trong cây ứng viên hoặc nền ⇒ cùng mục; gốc nền là g1 ⇒ `blob_nen`; ứng viên là `ops/` của nền ⇒ `hai_goc…`+`blob_ung_vien`; ứng viên là clone khác của nền ⇒ `blob_ung_vien`; gốc rỗng ⇒ `blob_ung_vien`; tất cả rc=1 (kèm mục `a9` vì R9 rỗng, như §0 khai) | có |
| A9 cây giả (đổi duy nhất hằng `BLOB_NEN`) | §0 (5): S1, S3, S5 | `a9_gia.py`: ứng viên in đúng hai dòng, không chạy gì ⇒ rc=0, `r9` 0,0 (S1: **ĐẠT, như §0 khai**); in `52/52` thay `59/59` ⇒ rc=1 `cuoi`; không ghi tệp mảnh ⇒ rc=1 `cuoi`; chậm 2,2× ⇒ rc=1 `a9` (dự báo 44,37); nhanh 1,3× ⇒ rc=0 (26,22); k=6 đòi 58/58 | có |
| cửa con trên `git archive 19a2d96` | 212 · 60 · 162 · 122 · 456; E698 121 | `venv3.12 -B ops/cong_cu_test.py --tu-kiem-che-do|main|gom` + `vec_v.py`: `m1` `[673234, 122268, [], 0]`, `luoi` 212, `luoi_git` 60, `m3698-` 162, `noi698-` 122, `ghi698` `[456, [], 0]`, `E698` 121; trên `bfb4ca3`: cùng `m1`, `luoi`, `luoi_git`, `m3698-`, `noi698-`, `ghi698`; E698 **120** (thiếu `lease_publish_test.A9KhongDoDuoc`) | có |
| E698 119 khi có bytecode | 119, thiếu `tokenize.TokenError`, `tokenize.StopTokenizing` | biên dịch sẵn `lease_publish_test` và `bash_nen` vào `ops/__pycache__` rồi chạy cửa che-do: 119; thiếu đúng hai khoá ấy | có |
| bảy cây thu hẹp §0 (4) | bảng T1b–T7, N68 | cây = g1 + đúng một thay thế (`dung_cay.py`): T1b `luoi` 211 · `noi698-` 120 · `ghi698` 455; T2 `m3698-` 144; T3 `luoi_git` 59; T4 E698 110 (thiếu 11 `yaml.*`); T5 `ghi698` 280; T6 `m1[1]` 122192; T7 `m1[1]` 122058 · `noi698-` 116 · `ghi698` 454 + 1 ô lệch; suite 56/56 ở T1b–T6, 55/56 (`t52` ĐỎ) ở T7 và T1 | có, từng số |
| N6 / N8 | N68 chỉ (iv) đỏ | N6: `m1` `[237964, 122268, [], 0]`, mọi số (v) bằng g1, 56/56; N8: `m1` và (v) bằng g1, 56/56, CPU cửa che-do 5,09 → 4,30 s | có |
| lưới có sẵn (lớp P2): thành phần 508 khoá `--tu-kiem-main` | — | 162 `m3698-` + 122 `noi698-` + 135 `noi-k*-n*` + 32 `noi-{du,manh}-w*` + 6 `noi-path-*` + 6 `noi-nen-*` + 45 khác | — |
| **P1a** (g1 + 1 dòng) | — | `git diff --numstat 19a2d96` = `1 1`; cửa con: `m1`, 212 · 60 · 162 · 122 · 456, E698 121 bằng g1; chữ ký cấu trúc `KQ`: che-do và gom BẰNG, main KHÁC 131 khoá; suite `cong_cu_test: 56/56 đạt` (40,1 s); Phụ lục G rc=0; ruff: một `F841 ci` như g1 | (iv), (v), A4-b, A4-d xanh |
| P1a: đột biến đích `t54` | — | `chay_dot_bien.py` (gọi `_do_mot` + `_ket_luan_ban_ghi` của chính tệp test), 101 tên của `t54` trong `DOT_BIEN` (gồm `f42_*`, `f44_*`, 12 canh `w698_*`): 101/101 `ok … giết đúng 't54_…' · bán kính 1/56` (2020,8 s + 2041,6 s, hai tiến trình) | A5 lát t54 xanh |
| P1a: dò đích `t54` | 19 SỐNG khai | `do_dot_bien_r6.py` (419 dò) trên 63 dò đích `t54` (`muc_dich.json`): 59 GIẾT, 4 SỐNG = `t_cf`, `t_tab` (ngoài lớp) và `x_f50_tk_and_bq_ne3`, `x_f50_h_and_bq_ne3` (KHAI); mọi `so_neo` = 1. Ba dò KHÁC (`s_ra_realpath`, `x3_cat_ll_bk` giết thêm `t54`; `x3_wr_ra_lower` tín dụng giả `t52`) vẫn KHÁC | (ii) xanh trên 66 dò đo |
| P1a: CPU cửa `--tu-kiem-main` | — | ba lượt xen kẽ g1/P1a, lõi 0 dùng chung: g1 3,40 · 3,76 · 3,88 s; P1a 2,32 · 2,09 · 2,11 s | −1,3 đến −1,8 s |
| **P1a: Phụ lục I theo công thức (i)** | Δ_g2 ≤ 0,85 × Δ_g1 | `chi_phi_r4.py <ar_fc852ff> <cây>` bốn lượt xen kẽ (g1, P1a, g1, P1a), lõi 2,3: Δ_CPU 8,33 · 6,91 · 9,32 · 6,95; Δ_g1 = 8,33, Δ_P1a = 6,91 ⇒ **0,830**; `ty_le` P1a 1,2919 · 1,3066 (≤ 1,35); `ty_le` g1 1,3435 · 1,3937 (một lượt ĐỎ A4-g, như lượt 11 đã khai) | (i) và (iii) ĐẠT |
| P1a + N8 (`P1a8`) | — | lượt 5–7: Δ 5,63 (g1 8,80 ở lượt 6) · 5,44 ⇒ 5,44/8,33 = **0,653**; cửa con và suite như P1a. Một lô Phụ lục I khác, cây `P1c8` (= `P1a` cộng hàng n = 3, cộng N8): Δ 6,45 · 5,08 so g1 8,67 · 8,91 ⇒ 0,586 | (i) ĐẠT |
| thành phần Δ_g1 trên máy này | — | CPU cửa nền (`ar_fc852ff`): che-do 0,45, main 1,69, gom 4,79 s; g1: 5,09 · 3,87 · 6,82 s | — |
| chủ kho `6073703559` | 1839 byte, bảy mục | `gh api repos/ducthangho/tra-luat/issues/comments/6073703559`: 1839 byte, sha256 `879d26e7…d6c49`; bảy mục khớp r12 (xem dưới) | có |
| #698, PR #721 | 28 comment, mới nhất `6079843708` | `gh api …/issues/698/comments --paginate`: 28, mới nhất `6079843708` (11:20:29Z); PR #721 mở/draft head `19a2d96`; `gh api …/pulls/721` | có |
| write set trên master hiện tại | nền tiếp nối `4beb9d0` | `git diff --name-only 4beb9d0 8b59185 -- ops/cong_cu_test.py .github/workflows/ci.yml ops/ci_duong_nhanh_test.py` rỗng (blob `9edea6b1…`, `1d3c63ff…`, `60fb2e37…` không đổi) | có |

Trung thành gói 1–7: (1) write set 3 tệp, `ci.yml` chỉ dòng `timeout-minutes`, `ci_duong_nhanh_test.py` chỉ phần tử `gate-cong-cu` — §3, M7a/M7b, A4-f, không đổi; (2) trần 30 → 45 — M7a, không đổi; (3) đích Δ_g2 ≤ 0,85 × Δ_g1 — M8, A10 (i), không đổi, chỉ chặt thêm (iv), (v); (4) A9 mảnh 1 và 3, 20,17, 0,75 — A9, Phụ lục M `45 1 3`, không đổi; (5) lượt CI 2 do chủ kho duyệt trước khi đẩy — §7 `1/1/2`, S10, không đổi; (6) lease g2 thay thế g1 hai chiều — `depends_on` (4) chỉ đổi `r11`→`r12`; (7) nợ `tran-gate-cong-cu-uoc-tu-may-khac-wp698` — `land_obligations`, không đổi.

## CHI TIẾT TỪNG LỚP

### 1. `a10-v-chi-ghim-o-moi-bo-o-co-san-van-lot` — P2

**Vị trí.** `SPEC.md` A10 (v) (dòng 2894–2912), §5 M8 "Cấm" (dòng 2529–2535) và "Giữ răng" (2536–2538). Mã g1 (`19a2d96`, `ops/cong_cu_test.py`): `_luoi_noi_main` (dòng 8002), vòng tiêu thụ của cha `t54` (dòng 7047, `for name, mode, ki, ni, path, workers in _luoi_noi_main():`) và của con `_in_tu_kiem_main` (dòng 8119, `noi = {name: … for … in _luoi_noi_main()}`).

**Vấn đề.** r12 rà "mọi chỗ cùng cơ chế" (§0 (4)) và ghim số của bốn lưới cùng `ghi698` và `E698`. Nhưng với **một** lưới, `_luoi_noi_main`, phép ghim chỉ phủ phần MỚI: (v) đếm "số khoá mở đầu `noi698-`" (122) và "`m3698-`" (162) của `--tu-kiem-main`, còn 179 hàng CÓ SẴN từ #668 của chính hàm ấy (135 `noi-k{k}-n{n}`, 32 `noi-{du,manh}-w{w}`, 6 `noi-path-{i}`, 6 `noi-nen-{i}`) và 45 khoá khác (kịch bản nền, trường phụ) không đứng trong phép so nào. Hai lưới còn lại cùng loại (`luoi`, `luoi_git`) thì được ghim THEO TỔNG (212, 60), tức gồm cả phần có sẵn — chỗ bất đối xứng ấy chính là lỗ. Cha và con dựng từ cùng hàm nên bỏ hàng ở hàm thì cả hai phía cùng đổi, `t54` vẫn xanh; M8 "Cấm" nói "bỏ ô" nhưng không có số đếm nào đỏ khi bỏ ô có sẵn. Câu r12 thêm vào M8 "Giữ răng" — "số ô, số kịch bản của ba cửa con bằng g1" — rộng hơn phép đo (năm số cộng `E698`).

**Đo (tái lập được).** Cây `P1a` dựng từ `git archive 19a2d96` (hardlink, thay đúng `ops/cong_cu_test.py`; `goi/so-lieu/P1a_so_voi_g1.diff`, 13 dòng, `git diff --numstat` = `1 1`):

```
-    rows = [(f"noi-k{k}-n{n}", "manh", k, n, "x", 3) for n in range(2, 17) for k in range(n)]
+    rows = [(f"noi-k{k}-n{n}", "manh", k, n, "x", 3) for n in (2, 16) for k in (0, n - 1)]
```

- Ba cửa con (`dung_cay.py`, `do_cay.sh`, `vec_v.py`): `m1` `[673234, 122268, [], 0]`, `luoi` 212, `luoi_git` 60, `m3698-` 162, `noi698-` 122, `ghi698` `[456, [], 0]`, `E698` 121 khoá — **bằng g1 từng số**: (iv) và (v) xanh. Chữ ký cấu trúc của `KQ` (`chu_ky_kq.py`: khoá và độ dài danh sách/từ điển, mọi độ sâu, bỏ độ dài `m5b[0]`): che-do và gom BẰNG g1 (32, 72 khoá); main 508 → 377 khoá, **KHÁC 131 khoá** (`noi-k0-n10`, …).
- Suite: `CONG_CU_TEST_BAN_KINH=manh` ⇒ `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0` (40,1 s). A4-d (Phụ lục G, trên clone `19a2d96` + tệp `P1a`): rc=0, giao rỗng. A4-b (ruff 0.15.15 `--select F`): đúng một `F841 ci`, như g1.
- A5, lát `t54`: 101/101 đột biến đích `t54` GIẾT đúng ca đích, bán kính 1/56 (gồm `f42_k_mod_8`, `f42_n_luy_thua_2`, `f44_nen_*` — những đột biến tôi nghi sẽ SỐNG khi bỏ tam giác — đều vẫn chết; hàng còn lại nào giết chúng, tôi không tách).
- A10 (ii), lát đo: 63/63 dò đích `t54` đúng hạng đã khai (59 GIẾT; 4 SỐNG = đúng bốn tên mà §6 khai: hai ngoài lớp, hai KHAI); ba dò KHÁC vẫn KHÁC. 353 dò còn lại đích `t52`/`t53`: không chạy; suy luận — cây chỉ đổi lưới mà `t54` và cửa `--tu-kiem-main` đọc, nên hạng của dò đích `t52`/`t53` chỉ có thể đổi nếu `t54` từng giết thêm chúng (khi ấy chúng đã là KHÁC trên g1: chỉ ba dò, đã đo).
- A10 (i), đúng công thức (Phụ lục I, bốn lượt xen kẽ g1 – P1a – g1 – P1a, lõi 2,3): Δ_CPU g1 8,33 · 9,32; P1a 6,91 · 6,95 ⇒ **0,830** ≤ 0,85. (iii): `ty_le` P1a 1,2919 · 1,3066. Nhiễu: Δ_g1 qua ba lượt 8,33–9,32 (+11,9 %), `loi_khac_dung` 1,7 (các phép đo song song của reviewer), nên 0,830 chỉ là một lô; lô khác (g1 8,67 · 8,91) với cây `P1c8` cho 0,586.
- Riêng một dòng ấy đã đủ cỡ đích: cửa `--tu-kiem-main` 3,40–3,88 → 2,09–2,32 s (−1,3 đến −1,8 s; M8 "Vì sao 0,85" nói cần bớt 1,58–1,77 s). Cộng một tối ưu hợp lệ N8: 0,653.

**Hậu quả.** (a) Lượt 11 đã chứng minh một executor thiếu vài phần trăm sẽ thấy thu hẹp là cách rẻ nhất và không gì đỏ (N68); r12 đóng chiều ấy nhưng để lại chiều rẻ hơn: bỏ ô CÓ SẴN, ở đúng hàm mà r12 vừa rà. Mỗi hàng bỏ cũng làm `t54` mất khả năng bắt đột biến LẠ về cách `main` truyền `k/N`, và chủ kho cấm đúng điều đó ("không bỏ ô", quyết định 3). (b) Bộ đột biến và bộ dò không cần 131 hàng đã bỏ — mọi đột biến và dò đích `t54` đều vẫn chết nhờ các hàng còn lại — tức hàng bỏ là dư THEO BỘ ĐỘT BIẾN, và "dư theo bộ đột biến" không phải "dư": đột biến lạ về cách `main` truyền `k/N` mất một phần ô bắt nó. (c) Lỗ nằm ở lời khai: M8 "Giữ răng" khai bằng g1 điều (v) không đo.

**Phương án (HINT, một nhóm, 3 hunk).** (1) A10 (v): thêm — với CẢ BA cửa con — tập khoá của đối tượng `KQ` của g2 CHỨA tập khoá của g1 và độ dài mọi danh sách/từ điển lồng (cùng đường khoá, mọi độ sâu) không NHỎ HƠN của g1, trừ `kq["m5b"][0]` (đã có phép chứa riêng); số đo trên g1 32 · 508 · 72 khoá. Một phép so duy nhất phủ mọi hàng/khoá có sẵn của ba cửa con, thay cho việc liệt kê từng lưới; nó chặn BỎ ô, không chặn thêm ô giả cho đủ số (cùng giới hạn đã khai của (iv), (v)). (2) PHẢI ĐỎ Ở: thêm cây `P1a` với các số trên. (3) M8: "Cấm" nêu "ô CÓ SẴN từ #668 của một lưới cha–con dùng chung", "Giữ răng" nêu đúng phép đo (năm lưới và khoá `KQ`). Không đính mã; kiểm bằng `chu_ky_kq.py` (không nằm trong đặc tả).

**Giới hạn.** (1) `P1a` bỏ 131 hàng; một executor chọn bỏ ít hơn hay bỏ ở cửa khác (`gom`, `che-do`: `_luoi_byte`, `bang_env`) cũng qua trừ khi phép so khoá phủ — phép đề xuất phủ cả ba cửa. Tôi chưa dựng cây bỏ ô ở `gom`/`che-do`. (2) 353 dò đích `t52`/`t53` và 369 đột biến đích khác không chạy trên `P1a` (suy luận như trên). (3) Phụ lục I nhiễu (+12 % trên Δ_g1) và chạy khi 2 lõi khác bận; 0,830 là một lô. (4) Tôi không thử `P1a` trên runner. (5) HINT chưa được chạy lại trên cây g2 thật.

## GHI NHẬN KHÔNG THÀNH LỚP

- **A9 chấp nhận R9 = 0,0 khi ứng viên giả in đúng hai dòng và ghi tệp mảnh** (`a9_gia.py` S1: rc=0, `r9` 0,0, dự báo 0,0; r12 §0 (5) đã khai và gọi là "PHẢI XANH"). Không lên lớp: đường giả phải bịa JSON hoặc chạy một tệp test khác `blob_ung_vien` của exact head, mà handoff kiểm; cái mà lượt 11 gọi là lớp (đầu vào gõ nhầm) nay đã đỏ. Nếu muốn chặt hơn: coi `r9` < 1,0 (ứng viên 470 mục không thể nhanh hơn nền 416 mục) là đỏ khi handoff đọc JSON.
- **Trùng nhãn.** Nhãn mẫu `S1`, `S2`, `S3`, `S5` ở bảng §0 (5) trùng nhãn điều kiện dừng S1–S11 và công thức S1/S2 của M1; `T1b`–`T7` trùng ô `T1`–`T5` của M2b. Mỗi chỗ có "(§0)" nên không đổi quyết định nào.
- **Câu "A4-g … CI chỉ chạy MỘT lần (Q7)" còn nguyên** cạnh câu HINT nói nó đã quá hạn: đúng như HINT.
- **Số vòng.** Nếu lượt này còn lớp mở thì r13 là vòng thứ ba của mục việc r11 (r11, r12, r13). Comment `6056465328` từng đặt "tối đa 2 vòng" cho mục việc cũ và `6059148459` cho vượt đúng một lần; không comment nào trong 28 cái đặt trần cho mục việc sau CI lượt 1 (đã đọc 28/28). Ý chủ kho: KHÔNG ĐO ĐƯỢC. Lời nhắc cho phiên điều phối, không phải finding.

## KHÔNG ĐO ĐƯỢC

1. Giây thật trên runner `ubuntu-latest` (2 vCPU), tải runner, tỷ lệ tường từ máy đo sang runner — như spec; chỉ lượt CI 2 đo được.
2. Hạng 419 dò mà handoff g1 đính kèm (A10 (ii) lấy làm chuẩn): không có trong sandbox. Tôi so với bảng khai của spec (19 SỐNG, 3 KHÁC theo tên).
3. 419 dò trọn, A5 trọn 470 đột biến và 54 canh trọn trên `P1a`: chỉ đo lát `t54` (101 đột biến gồm 12 canh; 66 dò). Phần còn lại là suy luận (lớp 1, Giới hạn 2).
4. A9 chạy hai lệnh một mảnh (`1`, rồi `3`) với các phép đo song song của reviewer ở lõi còn lại (`loi_khac_dung` 0,73 và 1,64), không phải một lệnh `45 1 3` trên máy rảnh. Kết luận ĐẠT/ĐỎ không nhạy với mức nhiễu này (dự báo 31,09 so ngưỡng 33,75 và 22,5), con số R9 thì có (1,5091–1,5413 so 1,5158/1,5248/1,5500 của các phép đo khác).
5. A9 với nền THẬT và ứng viên `sys.exit(0)`, và hàng S2 của §0 (5) (gốc nền là cây `git archive`, bản trung gian `10d25e6d…`): không chạy trọn (~13 phút nền mỗi lượt; lần thử `sys.exit(0)` của tôi bị `timeout 60` cắt giữa lượt nền). Chốt (a) đo bằng cây giả (S3, S5, k = 6) và đọc mã; chỉ đo lại các hàng không cần chạy suite thật (Q5–Q11).
6. Python 3.11/3.13 cho (iv), (v); Windows (Q8).
7. Cây bỏ ô ở cửa `gom` và `che-do` (lớp 1, Giới hạn 1).
8. Ý chủ kho về số vòng; việc chủ kho có thật sự gõ comment `6073703559` (`loi_khai_co_neo`, như chính comment tự khai).

## DRY-RUN HINT.patch

`HINT.patch`: một dòng `# lop:` mô tả ở đầu tệp, một khối `---`/`+++` trỏ `ops/specs/ci-g5-cong-cu-va-tiep-r12.md` (không tiền tố), 3 hunk, mỗi hunk đứng sau một dòng `# lop: a10-v-chi-ghim-o-moi-bo-o-co-san-van-lot`; chỉ sửa văn bản đặc tả, không đính mã (Q14); 0 TAB, 0 dấu chéo ngược. Dựng bằng `goi/dung-cu/mk_hint.py` (difflib trên chính `SPEC.md`).

Dry-run trên bản sao `git archive` của `cay-kho` (HEAD `786bf3ba…`, `ops/specs/ci-g5-cong-cu-va-tiep-r12.md` sha256 `e6c3ec0b…1ce9`), thư mục `mktemp -d -p "$R"`:

```
patch -p0 --fuzz=0 --dry-run --verbose < goi/HINT.patch
```
- **rc=0**; `Hunk #1 succeeded at 2526` · `#2 at 2908` · `#3 at 2931`; **3/3 hunk, 0 dòng `fuzz`, 0 dòng `offset`**; tệp đích sau dry-run vẫn trùng r12 (`cmp` rc=0).
- Áp thật trong cây tạm: `patch -p0 --fuzz=0 --verbose` rc=0, 3/3 hunk; tệp sau vá 5135 dòng (r12: 5124; +11), 0 TAB, 0 dấu chéo ngược, không tệp `.orig`/`.rej`; `difflib` so với r12: đúng hai khối thay (2 dòng M8 Cấm, 2 dòng M8 Giữ răng), một khối chèn 7 dòng (A10 (v)) và một khối chèn 4 dòng (PHẢI ĐỎ Ở).
- Ghi chú dùng: `git apply --check` không dùng được cho tệp này (dòng `# lop:` nằm giữa các hunk); `patch` bỏ qua chúng, như các lượt trước.

## NHẬT KÝ ĐO (UTC, 09-10)

- 13:36 băm đầu vào; 13:37 HINT lượt 11 áp lên r11; 13:40 Phụ lục M trích và so với r11; 13:41 dựng cây (clone git nền và g1, `git archive` 19a2d96, bfb4ca3, fc852ff) trong `mktemp -d -p "$R"`.
- 13:45–14:19 A9 mảnh 1 (lõi 0,1); 14:16–14:51 A9 mảnh 3 (lõi 2,3); đối chứng âm Phụ lục M 13:50–13:52; cây giả `a9_gia.py` 14:00.
- 13:42–14:07 cửa con trên g1, bfb4ca3; cây T1b–T7, T1, N6, N8 (13:55–14:10); E698 119 (13:59).
- 14:05–14:12 CI §1.13.2 qua `gh api` (68 run, 57 danh sách job); chủ kho, #698, PR #721, master.
- 14:08–14:11 cây `P1a`, `P1a8`; Phụ lục G, ruff; 14:23–14:57 quét 101 đột biến đích `t54` (hai tiến trình, lõi 0 và 1); 14:51–15:11 Phụ lục I (lõi 2,3: bốn + bảy lượt); 14:57–15:19 63 dò đích `t54` và 3 dò KHÁC trên `P1a`.
- 15:19–15:22 sinh `HINT.patch`, dry-run, áp thật; 15:20 dọn cây (`shutil.rmtree`); `$R` từ 1,8 GB xuống 0,4 GB. Ba thư mục `dotbien_*` mồ côi của lượt suite tôi dừng giữa chừng trong `/tmp` đã dọn; các thư mục `tmp*/{a,b}` (bản sao `bash` ~1,4 MB mỗi cái, do tiền kiểm của suite để lại; ~280 cái từ lúc 13:46) không xoá được an toàn vì không tách được khỏi các phiên đo song song khác trên máy dùng chung.
- Tiến trình: mọi tiến trình con đã `wait` hoặc dừng theo PGID của chính mình; không `pkill`, không `rm -rf`.
