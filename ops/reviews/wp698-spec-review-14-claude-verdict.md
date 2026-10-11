verdict: approve
reviewed_sha: d17ec09088acf674a05638345f7b3ec28ff03c6d
spec_sha256: ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21
model/effort tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), effort max — KHÔNG phải codex. Reviewer độc lập thay cho lượt codex, làm đúng `PROMPT.md` r14 (lượt 14, HẸP) với ba khác biệt do phiên điều phối nêu: không sửa `cay-kho/` (chỉ ghi dưới `goi/` và các thư mục `mktemp -d -p "$R"`); không dùng mạng, không đăng GitHub, không commit/push. Lượt chạy liền một mạch (không phải lượt tiếp nối). Máy đo: Linux 4 lõi; Python 3.11.15 (Unicode 14.0.0) · 3.12.3 (15.0.0) · 3.13.12 (15.1.0), mỗi venv có PyYAML 6.0.3 và jsonschema 4.26.0; ruff 0.15.15. Phép so khoá cách tính r14 do reviewer viết lại từ chữ r14 (`goi/dung-cu/so_nghiem.py`), rồi đối chiếu với `so_kq.py` của lượt 13. Không có bản `sub/*.json` của lượt 13 trong gói: các cây dựng lại từ mô tả chữ bằng `goi/dung-cu/mk_sub.py` + `dung_cay.py` của lượt 13, và năm cây có blob để đối chiếu đều trùng byte (BẢNG ĐO dòng 8).
số lớp: 0 P1 · 0 P2 · 0 P3 (0 lớp)

## BẢNG LỚP

Không có lớp mở. Bảng rỗng có chủ đích:

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| — | — | — | — | — |

Ba câu hỏi của PROMPT, trả lời bằng số (chi tiết ở CHI TIẾT TỪNG LỚP):

1. **Hai lớp lượt 13: cả hai ĐÃ ĐÓNG, bản vá không sinh lỗi mới đo được.** `W1c` (blob `8beb1250…`, trùng r14 §0 (3)) vẫn 56/56 ở 3.11 · 3.12 · 3.13, r12 (iv)(v) xanh, ruff một `F841 ci` như g1, giao rỗng với sáu hàm cấm sửa, 13/13 đột biến đích `t53` GIẾT đúng (đột biến đo ở 3.12) — và ĐỎ đúng MỘT đường `("byte","luoi")` (danh sách → chuỗi) dưới chữ r14, XANH dưới hai cách đọc của r13. `Gb` ĐỎ 11 lỗi, `Gc` ĐỎ 17 (cả hai suite 56/56; `Gb` 67/67 đột biến đích `t52`). `Wpad` XANH ở mọi cách đọc (đúng như r14 khai), `VE` ĐỎ 27 đường (đúng như r14 khai "đỏ theo chữ").
2. **Cách đọc nghiêm KHÔNG chặn oan `VB`, `VD`, `Nap` và KHÔNG đổi kết quả g1.** `VB` · `VD` · `VBD` · `Nap` XANH ở 3.11 · 3.12 · 3.13 (suite 56/56 ở 3.12 cho `VB` · `VD` · `Nap`); g1 chạy lại dưới 4 `PYTHONHASHSEED`, đường có dấu cách và chữ có dấu, môi trường CI, locale `C`, `__pycache__` có sẵn — 30 cặp (nền, biến thể) × hai chiều: phép so r14 XANH cả 30; chữ ký (đường → loại, độ dài) chỉ khác ở `("m5b", 0)` (E698) ở 3 cặp có `__pycache__`, đúng đường chữ r14 đã miễn.
3. **Diff r13 → r14 KHÔNG nới tiêu chí nào khác.** `difflib` r13+HINT so r14: 23 khối, toàn sổ sách; 29/30 dòng `+` của HINT có mặt nguyên văn, dòng còn lại chỉ đổi con trỏ `(§0)` → `(§0-r13)` như r14 đã khai; §2 §3 §4 §7 §9 và Phụ lục A–N giống từng byte; §5 và §6 chỉ khác r13 đúng ở các hunk của HINT.

## ĐỐI CHIẾU LƯỢT 13

| lớp lượt 13 | trạng thái r14 | phép đo |
|---|---|---|
| `a10-v-chua-chot-cach-tinh-khi-g2-thieu-duong-hay-doi-kieu` (P3) | **ĐÃ ĐÓNG.** Chữ "(r14) Cách tính, chốt" (A10 (v)) cho kết luận DUY NHẤT trên mọi cây đã đo: `W1c` ĐỎ (1 đường) · `VE` ĐỎ (27) · `W1b` ĐỎ (1) · `VR` ĐỎ (503) · `Wpad` XANH · `Nap` XANH, cùng kết quả ở ba phiên bản; phép so viết độc lập từ chữ r14 trùng số lỗi "chat" của `so_kq.py` (lượt 13) ở 17 cây × 3 phiên bản = 51/51 cặp; 21/21 ca biết trước đáp án của chính phép đo đạt. Không hồi quy | `bang_nghiem.py`, `bang_gon.py`, `kiem_phep_do.py`; `goi/log/bang_nghiem.md`, `bang_gon.md`, `kiem_phep_do.txt`, `chi_tiet_loi.txt` |
| `a10-v-cua-gom-khong-cay-do-va-phu-khai-cha-tu-do` (P3) | **ĐÃ ĐÓNG.** Số đo thay cho câu "không cùng cơ chế" khớp: cha đỏ 71/72 (`t52`), 32/32 (`t53`), 508/508 (`t54`), im lặng duy nhất `ghi_gay`; `Ga` · `Gb` · `Gc` · `Gd` suite 56/56 và ĐỎ ở phép so khoá (3 · 11 · 17 · 3 lỗi), `GbCon` 55/56; `Gb` 67/67 đột biến đích `t52`; phép so chỉ đọc cửa `main` XANH ở `B1` · `Ga` · `Gb` · `Gc` · `Gd`, ĐỎ ở `P1a` (395). Chữ M8 "Cấm" thu về "HIỆN TRONG `KQ`" đúng với mã (khối F28 của `t54` không sinh khoá `KQ` nào). Không hồi quy | `cha_phan_ung.py` (3.12), `chay_suite.sh`, `chay_dot_bien.py`; `goi/so-lieu/cha_phan_ung_g1.json`, `goi/log/suite/*`, `goi/log/dotbien/*` |
| Bản vá có sinh lớp MỚI không? | **KHÔNG đo được lớp mới** (0). Đã thử: g1 so g1 qua 30 biến thể × 2 chiều; `VB` · `VD` · `VBD` · `Nap` × 3 phiên bản; con trỏ `§0` trần (108 chỗ) đều thuộc chữ của revision cũ trỏ chính nó hoặc thuộc r14; các số r14 tự đo lại trùng (409/410 đường, 1 · 0 · 11 · 17 · 27 · 1 · 395 lỗi); bảng markdown không lệch cột | BẢNG ĐO dòng 17–23 |

Tỷ lệ vá thật lượt 13 → 14 theo §12: 2/2 = 100,00 % (U = hai slug trên, cả hai ĐÃ ĐÓNG; lớp mới 0, lớp tái mở 0).

## BẢNG ĐO

Ký hiệu: `R` = thư mục làm việc; `T` = `mktemp -d -p "$R"` giữ các cây (đã xoá sau khi đo); `X` = `…/x698`; lệnh chạy từ `R`. Mọi cây = g1 (`git --git-dir=kho.git archive 19a2d96`) cộng đúng thay đổi nêu, dựng bằng `cp -al` rồi ghi tệp mới + `os.replace` (`goi/dung-cu/dung_cay.py`, đặc tả thay thế ở `goi/so-lieu/sub/<cây>.json` sinh bởi `mk_sub.py`). Mọi lượt chạy `python -B` với `PYTHONDONTWRITEBYTECODE=1`. Ba trạng thái: có · không · KHÔNG ĐO ĐƯỢC.

| # | khẳng định | đặc tả khai | đo được (lệnh) | khớp? |
|---|---|---|---|---|
| 1 | băm đầu vào | `SPEC.md` `ed027f41…1a21`; r13 `e01eb24c…e0ac`; lượt 13 `8dfbaa57…0079`, `914d6f97…6b10`; HEAD `d17ec09` | `sha256sum SPEC.md SPEC-r13.md r13-r14.diff luot13/VERDICT.md luot13/HINT.patch`: `ed027f41…`, `e01eb24c…`, `b5827378…` (diff 325 dòng), `8dfbaa57…`, `914d6f97…`; `git -C cay-kho rev-parse HEAD` = `d17ec09088acf674a05638345f7b3ec28ff03c6d`; `wc -l`: 5374 · 5247 | có |
| 2 | r1–r13 giữ nguyên byte; r14 trong kho | "sha256 của mười ba tệp ấy … trùng nhau"; chuỗi dòng dõi 13 băm | `sha256sum cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r{1..14}.md`: 13 băm r1–r13 khớp đầu và đuôi chuỗi dòng dõi ở header (đuôi r3 ghi `dfe1b`, đúng `…28dfe1b`); `cmp` r14 trong kho với `SPEC.md` rc=0 và r13 với `SPEC-r13.md` rc=0; `git --git-dir=kho.git diff --name-status a2734e5 d17ec09` = `A ops/specs/ci-g5-cong-cu-va-tiep-r14.md` (một tệp, không sửa r1–r13); cha của `d17ec09` là `a2734e5` | có |
| 3 | bản sao HINT đổi đích | `3f92e0dd…7fac`, "đúng hai dòng" | `sed -e '2s#r13\.md#r14.md#' -e '3s#r13\.md#r14.md#' luot13/HINT.patch` rồi `sha256sum` = `3f92e0dda2c48626ab84dfc88205879fd43df56f5394aa6e4aa3886472d57fac`; `diff` với bản gốc: đúng dòng 2 và 3 | có |
| 4 | HINT lượt 13 áp nguyên văn | rc=0, 5/5 hunk, 0 fuzz, 0 offset, 5273 dòng, `0e9a49e9…db8a` | `patch -p0 --fuzz=0 --dry-run --verbose` rồi `patch -p0 --fuzz=0 --verbose` trên bản sao r13 đặt ở `ops/specs/ci-g5-cong-cu-va-tiep-r13.md`: rc=0 cả hai; `Hunk #1 succeeded at 167` · `#2 at 2631` · `#3 at 3020` · `#4 at 3053` · `#5 at 3547`; 0 dòng `fuzz`, 0 `offset`, 0 `.orig`/`.rej`; `wc -l` 5273; sha256 `0e9a49e9bfab4b610903a0f2e7bd67752e2096ce43c1eae696ff34296024db8a` | có |
| 5 | r14 chỉ lệch r13+HINT ở sổ sách; 29/30 dòng `+` nguyên văn | 23 khối; một chỗ trỏ `§0` | `python3 -B goi/dung-cu/so_hunk_r13h_r14.py <r13+HINT> SPEC.md luot13/HINT.patch` (`goi/log/so_hunk.out`): 23 khối; 30 dòng `+`, 29 có mặt nguyên văn, 1 vắng = dòng "kiểu ở đó; hai cách đọc … (§0) nhưng KHÁC nhau …" (r14 viết `(§0-r13)`); 0 TAB, 0 dấu chéo ngược | có |
| 6 | tiêu chí không đổi ngoài HINT | §5 và §6 chỉ năm hunk; Phụ lục A–N không đổi | `python3 -B goi/dung-cu/diff_theo_muc.py SPEC-r13.md <r13+HINT> SPEC.md` (`goi/log/diff_theo_muc.txt`): §2 §3 §4 §7 §9 và Phụ lục A–N GIỐNG; §5 +2/−1 và §6 +19/−0 do HINT (r13+HINT → r14: GIỐNG ở cả hai mục); §1 +1/−1 (con trỏ); §8 +3/−1 (dòng r14 của S5); §10 +2/−1 (HINT) cộng +9/−2 (r14); §11 +10/−6; header +13/−12 | có |
| 7 | Phụ lục giữ nguyên | vùng A–L `e99226fd…3d2b` 1145 dòng; M `2fe67a92…`; N `3ba04375…` | `python3 -B goi/dung-cu/so_phu_luc.py SPEC-r13.md SPEC.md`: ba vùng giống từng byte; vùng A–L (bỏ dòng trống cuối) `e99226fdd6470ed5e507d3bbac89b6cb90d3a85da6a1a8fea70cc1e420d53d2b`, 1145 dòng; khối mã Phụ lục M · G · I · N khớp sha256 ở tiêu đề | có |
| 8 | cây dựng lại trùng blob | `W1c` `8beb1250…`, `Gb` `201d58fd…`, `Gc` `6504b030…`; `numstat` 3 2 · 2 2 · 2 2 | `python3 -B goi/dung-cu/dung_cay.py "$T" <cây> goi/so-lieu/sub/<cây>.json` (`goi/log/dung_cay.out`): `W1c` `8beb125072fb331b…`, `Gb` `201d58fdef363228…`, `Gc` `6504b03089531b48…`, numstat `3 2` · `2 2` · `2 2`; thêm `B1` `76fc907ca333df06…` và `P1a` `5953da4f58944ed1…` trùng lượt 12/13. (`W1c` và `Gb` chỉ khớp sau khi thử vị trí dòng thêm và bộ ba giá trị còn lại — `(True, "1", "so_thuc")` — trên blob, nên khớp blob là bằng chứng trùng byte, không phải trùng hình dạng.) `Wpad` `05e4b8c5…`, `Ga` `04df7f97…`, `Gd` `25673486…`, `GbCon` `b38d6f29…`, `VE` `f7edcb4e…`, `Nap` `fb0eef4d…`, `VB` `b9d07c60…`, `VD` `b6859098…` không có blob để đối chiếu. `goi/log/dung_cay.out` ghi cả lượt dựng đầu của `W1c`, `Wpad`, `Gb`, `GbCon` (vị trí dòng thêm và bộ ba giá trị khác, blob lệch) — đã xoá bằng `shutil.rmtree` và dựng lại | có |
| 9 | g1 | blob `9c628700…`; 32 · 508 · 72 khoá; 212 · 60 · 162 · 122 · 456 và 121 `E698` (3.12) | `git hash-object` = `9c628700ce23e042992d8f8e4c6a6263b1d8912f`; `bang_nghiem.py`/`goi/so-lieu/kq/g1_312_*`: 32 · 508 · 72 khoá; `luoi` 212, `luoi_git` 60, `m3698-` 162, `noi698-` 122, `ghi698[0]` 456, `E698` 121, `m1` `[673234, 122268, [], 0]`; số đường list/dict 410 (409 không kể `("m5b",0)`) · 1512 · 210 ở cả ba phiên bản. Khác theo phiên bản (chỉ số tuyệt đối, không dùng chéo phiên bản): `ghi698[0]` 452 · 456 · 457, `E698` 119 · 121 · 124, `m1` `[666094, 121008]` · `[673234, 122268]` · `[673404, 122298]` | có |
| 10 | phép so khoá r14: 7 số lỗi của §0 (3) | `W1c` 1 · `Wpad` 0 · `Gb` 11 · `Gc` 17 · `VE` 27 · `B1` 1 · `P1a` 395 | `python3 -B goi/dung-cu/bang_nghiem.py goi/so-lieu/kq g1 <cây,…>` (`goi/log/bang_nghiem.md`): 1 · 0 · 11 · 17 · 27 · 1 · 395, đúng cả ba phiên bản; thêm `Ga` 3 · `Gd` 3 · `GbCon` 11 · `W1b` 1 · `VR` 503; cột "khớp so_kq.chat" = có ở 51/51 cặp (17 cây × 3 phiên bản) | có |
| 11 | `W1c` ĐỎ đúng một đường; r13 XANH | `("byte","luoi")` danh sách 17 → chuỗi 768 | `python3 -B goi/dung-cu/chi_tiet_loi.py goi/so-lieu/kq g1 W1c,…` (`goi/log/chi_tiet_loi.txt`): `('doi_loai', ('byte','luoi'), 'list', 'str')`, 1 lỗi; `kq["byte"]["luoi"]` g1 là list 17, `W1c` là str 768; hai cách đọc r13 ("chỉ-list", `len()`) 0 lỗi; `kq["m1"]` `[673234, 122268, [], 0]` bằng g1 | có |
| 12 | bảng cây (bảng dưới) | — | `python3 -B goi/dung-cu/bang_gon.py "$R" "$T" g1,B1,W1c,…` (`goi/log/bang_gon.md`) | xem dưới |
| 13 | suite `manh` từng cây | 56/56 | `bash goi/dung-cu/chay_suite.sh "$T/<cây>" "$X/venv3.12/bin/python" <nhãn> "$R"` (`CONG_CU_TEST_BAN_KINH=manh`, `PYTHONDONTWRITEBYTECODE=1`, `-B`; `goi/log/tong_hop_suite.md`): 3.12 — g1 · `B1` · `W1c` · `Wpad` · `Nap` · `VB` · `VD` · `VE` · `P1a` · `Ga` · `Gb` · `Gc` · `Gd` đều rc=0, 56/56, `CỔNG TRÊN CÂY THẬT: ĐẠT`, 0 dòng `ĐỎ` (252–344 s ở 3.12; 243–354 s qua mọi lượt; 1–4 tiến trình song song); `GbCon` 55/56 (`t52` ĐỎ). 3.11 và 3.13 — g1 · `W1c` · `VE` · `Wpad` đều 56/56; 3.13 — `Gb` · `Ga` 56/56 | có |
| 14 | đột biến đích không mất răng | `W1c` 13/13 (`t53`); `Gb` 67/67 (`t52`); `B1` 90/90 (`t53`) | `chay_dot_bien.py` (gọi `_do_mot` + `_ket_luan_ban_ghi` của tệp test của cây; `TMPDIR` dưới `goi/`): `W1c` 13 tên (`f9_*`, `f32_*`, `f34_source_text_bytes`, `f36_*`), `Gb` toàn bộ 67 tên `t52`, `B1` toàn bộ 90 tên `t53`; `python3 -B goi/dung-cu/tong_hop_dotbien.py`: cả ba `loi=0` và `chet == [ca đích]`, bán kính 1/56 ở **13/13 · 67/67 · 90/90**; tập tên bằng đúng toàn bộ tên của ca đích trong `DOT_BIEN` (470 mục: `t52` 67, `t53` 90, `t54` 101) | có |
| 15 | cha phản ứng khi con bỏ MỖI lần một khoá (g1, 3.12) | `t52` đỏ 71/72, `t53` 32/32, `t54` 508/508; ngoại lệ `ghi_gay` | `"$X/venv3.12/bin/python" -B goi/dung-cu/cha_phan_ung.py "$T/g1" "$R/goi/so-lieu/kq" g1_312 gom che-do main "$R/goi/so-lieu/cha_phan_ung_g1.json"`: chuẩn `qua` cả ba; gom — im lặng 1/72 (`ghi_gay`), đỏ 71 (65 `giet_that` + 6 `tin_dung_gia`); che-do — im lặng 0/32, đỏ 32 (27 + 5); main — im lặng 0/508, đỏ 508 (503 + 5) | có |
| 16 | ruff `--select F` và sáu hàm cấm sửa | một `F841 ci` như g1; giao rỗng | `"$X/venv3.12/bin/python" -B -m ruff check --select F --no-cache --output-format concise "$T/<cây>/ops/cong_cu_test.py"`: g1 và 14 cây (`B1` `W1c` `Wpad` `Nap` `VB` `VD` `VBD` `VE` `P1a` `Ga` `Gb` `GbCon` `Gc` `Gd`) mỗi cây đúng một `F841` (`ci`); `python3 -B goi/dung-cu/giao_6ham_so_g1.py "$T/g1/ops/cong_cu_test.py" <14 tệp>`: `cham: []` cả 14, rc=0 (đây là biến thể A4-d lấy g1 làm nền, không phải Phụ lục G) | có |
| 17 | `VB` · `VD` · `VBD` · `Nap` không bị chặn oan | — (Q2) | `bang_nghiem.py`: XANH ở r12 (iv)(v), r14 chặt, hai cách đọc r13, cả 3.11 · 3.12 · 3.13; suite 56/56 (`VB` 2 thêm/0 xoá, `VD` 7/1, `Nap` 1/1; `VBD` 9/1 không chạy suite); ruff và giao 6 hàm như dòng 16 | có |
| 18 | g1 chạy lại: phép so r14 hai chiều | XANH (tự khai: g1 so g1 seed 12345) | `python3 -B goi/dung-cu/chay_bien_the_g1.py "$R" "$T" "$X"` rồi `python3 -B goi/dung-cu/bang_bien_the.py goi/so-lieu/kq goi/so-lieu/kq_bt` (`goi/log/bang_bien_the.md`): 10 nhãn × 3 phiên bản = 30 cặp (`lai`; `PYTHONHASHSEED` `0` `1` `99999` `12345`; `alt` = cây ở `duong khác nhau/ünï cô dê/g1_alt`; `ci` = `CONG_CU_TEST_BAN_KINH=manh` `CONG_CU_TEST_TIEN_TRINH=2` `CI` `GITHUB_ACTIONS`; `loc` = `LC_ALL=C` `LANG=C` `PYTHONIOENCODING=ascii` `TZ`; `pyc0`/`pyc` = cây có `ops/__pycache__`): r14 nền→biến thể và biến thể→nền **XANH cả 30**; chữ ký khác 0 đường ở 27/30, 1 đường `("m5b",0)` ở 3/30 (`pyc` 3.12: 121 → 119; `pyc0` 3.12: 121 → 119; `pyc` 3.13: 124 → 123). r12 (v) (`E698` chứa) ĐỎ ở đúng 3 cặp `pyc` ấy — tình huống r12 đã khai và đã cấm bằng "không `__pycache__`" | có |
| 19 | tái lập giữa hai lần chạy | — | chạy lại 8 cây (`W1c` `Wpad` `Gb` `Gc` `VE` `Nap` `VB` `VD`) ở 3.12 với `PYTHONHASHSEED=12345` (`goi/so-lieu/kq_lai`): số lỗi so g1 và hai chiều giữa hai lần chạy — GIỐNG ở cả 8 | có |
| 20 | phép đo tự kiểm | — | `python3 -B goi/dung-cu/kiem_phep_do.py goi/so-lieu/kq` (`goi/log/kiem_phep_do.txt`): 21 biến đổi tổng hợp trên `KQ` g1 biết trước đáp án (thêm khoá, thêm phần tử ở cuối, đổi giá trị lá, đổi thứ tự khoá, tuple → list, `m5b[0]` ngắn đi ⇒ XANH; bớt phần tử, danh sách → từ điển/`null`/chuỗi, bỏ khoá, đổi tên, chèn ở đầu ⇒ ĐỎ): `DAT` 21/21, `sai: 0`. `P1a` 395 = 131 khoá × 3 đường + 1 + 1, tính tay trùng | có |
| 21 | con trỏ `§0` trần | r14: chỉ chữ r14 dùng `§0` cho mục r14; chỗ r13 trỏ `§0` đã đổi thành `§0-r13` | liệt kê mọi `§0` không hậu tố trong `SPEC.md` bằng `re` `§0(?![-\w])`: 108 chỗ. Chỗ r14 dùng cho mục r14 — dòng 8 (`thay_the_cho`), 22 (hàng "review của r13"), 25 (`nguon_cap_viec`), 30 (reviewer), 84 và 96 (GIỚI HẠN LỜI KHAI), 930 (§1.1), 3295 (S5), 3644 (§10 mục r14), 3715 (§11 Q14), 3732–3733 và 3756 (§11.1), 3795 (bảng (B) Q14) — đọc từng chỗ: đều đúng mục. Còn lại là chữ của revision cũ trỏ chính §0 của nó (quy ước từ §0-r11, vd dòng 1265, 1609, 1641, 1855, 2018–2032, 2094, 2903, 3598, 3861–3865, 3965–3969: r3/r4/r5/r6) hoặc chữ mở đầu §0-r13/§0-r12… nói về chính việc đổi tên. Không chỗ nào còn trỏ `§0` mang nghĩa r13 | có |
| 22 | bảng markdown | — | đếm ký tự gạch đứng ngoài khối code ở 100 dòng đầu: mọi hàng bảng header đủ 3; bảng §0 (4) đủ 6 | có |
| 23 | số lượng `DOT_BIEN` | 470 mục; `t52` 67, `t53` 90, `t54` 101 | `dem_dot_bien.py "$T/g1"` (`goi/so-lieu/dot_bien_ten_theo_ca.json`): 470; `t52_` 67 · `t53_` 90 · `t54_` 101; khối F28 của `t54` có 4 mục `DOT_BIEN` riêng (`f28_can_cau_hinh`, `f28_gate_di_tat`, `f28_du_nuot_ma`, `f28_nen_ma`) và không ghi khoá nào vào `KQ` | có |
| 24 | răng của từng mệnh đề của chữ r14 | mỗi mệnh đề có cây cần đến nó | `python3 -B goi/dung-cu/rang_tung_menh_de.py goi/so-lieu/kq g1 W1c,W1b,VE,VR,B1,Ga,Gb,Gc,Gd,P1a,Wpad,Nap,VB,VD,VBD` (`goi/log/rang_tung_menh_de.md`): cột "bỏ loại": `W1c` `W1b` `VE` `VR` XANH, các cây còn lại không đổi; cột "bỏ độ dài": `B1` XANH; cột "bỏ thiếu-đường" và "bỏ khoá đỉnh": không cây mã nào đổi kết luận (số lỗi giảm nhưng vẫn ĐỎ); ca tổng hợp đổi tên `byte.luoi` ⇒ "bỏ thiếu-đường" XANH, ca tổng hợp đổi tên `gom.N` ⇒ "bỏ khoá đỉnh" XANH; `Wpad` `Nap` `VB` `VD` `VBD` XANH ở mọi cột | có |

Bảng cây (nguồn `goi/log/bang_gon.md`, ba phiên bản Python như nhau ở mọi hàng; cột "+/−" là `git diff --no-index --numstat` so g1; "r14 chặt" là số lỗi tổng ba cửa kèm che-do/main/gom; "r13" là cách đọc chỉ-danh-sách / `len()`):

| cây | blob | +/− | suite 3.12 | r12 (iv)(v) | r14 chặt | r13 chỉ-list / len() |
|---|---|---|---|---|---|---|
| g1 | `9c628700` | — | 56/56 | XANH | XANH (0/0/0) | XANH / XANH |
| `B1` | `76fc907c` | 1/1 | 56/56 | XANH | ĐỎ 1 (1/0/0) | ĐỎ 1 / ĐỎ 1 |
| `W1c` | `8beb1250` | 3/2 | 56/56 | XANH | **ĐỎ 1** (1/0/0) | **XANH / XANH** |
| `Wpad` | `05e4b8c5` | 3/2 | 56/56 | XANH | XANH (0/0/0) | XANH / XANH |
| `Nap` | `fb0eef4d` | 1/1 | 56/56 | XANH | XANH (0/0/0) | XANH / XANH |
| `VB` | `b9d07c60` | 2/0 | 56/56 | XANH | XANH (0/0/0) | XANH / XANH |
| `VD` | `b6859098` | 7/1 | 56/56 | XANH | XANH (0/0/0) | XANH / XANH |
| `VBD` | `f0891c5e` | 9/1 | — | XANH | XANH (0/0/0) | XANH / XANH |
| `VE` | `f7edcb4e` | 1/1 | 56/56 | XANH | ĐỎ 27 (27/0/0) | XANH / XANH |
| `VR` | `7afd02bc` | 1/1 | — | XANH | ĐỎ 503 (0/503/0) | XANH / XANH |
| `W1b` | `34e531b8` | 7/6 | — | XANH | ĐỎ 1 (1/0/0) | XANH / ĐỎ 1 |
| `P1a` | `5953da4f` | 1/1 | 56/56 | XANH | ĐỎ 395 (0/395/0) | ĐỎ 2 / ĐỎ 2 |
| `Ga` | `04df7f97` | 0/5 | 56/56 | XANH | ĐỎ 3 (0/0/3) | ĐỎ 2 / ĐỎ 2 |
| `Gb` | `201d58fd` | 2/2 | 56/56 | XANH | ĐỎ 11 (0/0/11) | ĐỎ 2 / ĐỎ 2 |
| `GbCon` | `b38d6f29` | 1/1 | 55/56 | XANH | ĐỎ 11 (0/0/11) | ĐỎ 2 / ĐỎ 2 |
| `Gc` | `6504b030` | 2/2 | 56/56 | XANH | ĐỎ 17 (0/0/17) | ĐỎ 1 / ĐỎ 1 |
| `Gd` | `25673486` | 2/2 | 56/56 | XANH | ĐỎ 3 (0/0/3) | ĐỎ 2 / ĐỎ 2 |

Mô tả cây (thay đổi so g1): `B1` biên `(63, 64, 65, 4095, 4096, 4097, 8193)` → `(64, 4096)` ở `_luoi_byte`; `W1c` = `B1` + một dòng `kq["byte"]["luoi"] = "".join(kq["byte"]["luoi"])` ngay trước dòng `sha = lambda …` ở `_in_tu_kiem_che_do` + cha so với `"".join(sha(b) for b in _luoi_byte())`; `Wpad` = `B1` + `kq["byte"]["luoi"] += [""] * 5` ở con + cha so với `[…] + [""] * 5`; `Nap` thêm `8194` vào cuối biên của `_luoi_byte`; `VB` thay `Path.read_bytes` bằng hàm trả `b"698"` trong lúc quét `head` (con); `VD` nhớ đệm `bam({…})` trong `phong` của `_in_tu_kiem_main`; `VE` đặt khối `so` lên đầu giá trị trả về của `_luoi_che_do()`; `VR` thay `list(log)` bằng sha256 của nó ở 503 kịch bản `main` (chỉ đổi con — dùng cho `KQ`, không dùng suite); `W1b` = `B1` + dời `byte.luoi` sang `byte2.luoi`; `P1a` `range(2, 17) … range(n)` → `(2, 16) … (0, n - 1)` ở `_luoi_noi_main`; `Ga` bỏ khối `ghi_gay` ở con; `Gb` sáu giá trị `gt` → `(True, "1", "so_thuc")` ở con và `range(6)` → `range(3)` ở `mong` của `t52`; `GbCon` chỉ phần con của `Gb`; `Gc` `range(2, 17)` → `range(2, 16)` ở `phan_hoach` của con và ở `lech` của `t52`; `Gd` bỏ biên `(17, None)` ở con và hàng `bien_17_None` ở `mong`.

## CHI TIẾT TỪNG LỚP

Không có lớp nào đứng được trên phép đo, nên không có mục lớp mới. Dưới đây là cách hai lớp của lượt 13 được kiểm đóng, rồi hai câu còn lại của PROMPT.

### Lớp lượt 13 #1 — `a10-v-chua-chot-cach-tinh-khi-g2-thieu-duong-hay-doi-kieu`: ĐÃ ĐÓNG

Điều lượt 13 đòi (hunk 3 và 5): chốt cách tính; PHẢI ĐỎ Ở `W1c`, đỏ theo chữ `VE`, không bắt (đã khai) `Wpad`; thay "KHÔNG ĐO" ở §10 bằng kết quả; đổi hình dạng `KQ` ⇒ DỪNG theo S11. r14 áp đúng các hunk ấy (BẢNG ĐO dòng 4–6).

Đóng thật, theo bốn phép đo độc lập nhau:

- **Chữ r14 đủ để viết phép so ra kết luận giống nhau.** Hai bản phép so viết riêng từ cùng chữ — của reviewer lượt 13 (`so_kq.py`, cột "chat") và của lượt này (`so_nghiem.py`, viết sau khi đã đọc `so_kq.py` nên độc lập chỉ ở mức mã) — cho CÙNG số lỗi ở 51/51 cặp (17 cây × 3 phiên bản). Bản thứ ba, của phiên soạn r14 (§0 (3)), khai 1 · 0 · 11 · 17 · 27 · 1 · 395 lỗi ở `W1c` `Wpad` `Gb` `Gc` `VE` `B1` `P1a` (3.12): trùng số của hai bản kia; script ấy không có trong gói nên chạy lại nó: KHÔNG ĐO ĐƯỢC. Lần đầu tiên "g2 thiếu đường hay đổi loại" có một câu trả lời.
- **Mỗi mệnh đề của chữ r14 có một phép thử cần đến nó** (phản chứng bơm vào bản họ: gỡ TỪNG mệnh đề khỏi phép so, xem cây nào qua — `goi/dung-cu/rang_tung_menh_de.py`, `goi/log/rang_tung_menh_de.md`, BẢNG ĐO dòng 24): gỡ "CÙNG loại" ⇒ `W1c`, `W1b`, `VE`, `VR` qua (XANH); gỡ "độ dài không nhỏ hơn" ⇒ `B1` qua (12 < 17 chỉ bị độ dài bắt); gỡ "thiếu đường ⇒ ĐỎ" ⇒ không cây mã nào đổi kết luận (các cây bỏ khoá còn bị độ dài và tập khoá bắt), chỉ ca tổng hợp "đổi tên `byte.luoi` thành `byte.luoi2`" qua (mệnh đề này thừa với độ dài và tập khoá đỉnh ở mọi cây bỏ khoá đã đo); gỡ "tập khoá đỉnh chứa" ⇒ không cây mã nào đổi kết luận, chỉ ca tổng hợp "đổi tên khoá đỉnh có giá trị lá `gom.N` thành `gom.N2`" qua (độ dài `KQ` không đổi, đường `N` là số nên không phải đường list/dict). "Theo chỉ số": `VE` là hoán vị thuần các phần tử danh sách `luoi` (cùng đa tập loại và độ dài), nên mọi phép so không theo vị trí cho XANH ở đó — chỉ phép so theo chỉ số làm nó ĐỎ, ở 27 đường `("luoi", i, 1)` với `i` = 135…161 (tính tay: khối `so` 169 phần tử dời lên đầu, 135 phần tử `manh` đầu tiên của nó chiếm chỉ số 0–134, nên 27 chỉ số 135–161 vốn là `["manh", [k, n, "x"]]` của g1 nay mang phần tử không phải `manh` ⇒ danh sách → chuỗi/`null`). Đo trùng: 27 đường.
- **`W1c` đúng là cây "sai nhưng xanh" mà chỉ chữ r14 bắt**: suite 56/56 ở 3.11 · 3.12 · 3.13, r12 (iv)(v) xanh, ruff một `F841 ci` như g1, giao rỗng với sáu hàm cấm sửa, 13/13 đột biến đích `t53` chạm bảng byte GIẾT đúng `t53` (bán kính 1/56, 38 s mỗi đột biến), phép so khoá cách đọc r13 XANH — và r14 ĐỎ ở đúng `("byte","luoi")` (`list` → `str`). `Wpad` 56/56 ở 3.11 · 3.12 · 3.13, XANH ở mọi cách đọc, đúng chữ "không bắt (đã khai)". `VE` 56/56 ở 3.11 · 3.12 · 3.13, XANH ở cách r13, ĐỎ ở r14.
- **Phép đo tự kiểm**: 21 ca biết trước đáp án (BẢNG ĐO dòng 20) đạt 21/21; `P1a` 395 tính tay trùng.

Không sinh lỗi mới: không cây nào trong 17 cây đổi kết luận giữa ba phiên bản; g1 vẫn XANH (dòng 18). Hai cách đọc r13 vẫn cho XANH ở `W1c`/`VE` — chính vì thế r14 phải chốt, và chữ r14 loại chúng tường minh ("không bỏ qua với lý do …, và không lấy `len()` của một chuỗi").

### Lớp lượt 13 #2 — `a10-v-cua-gom-khong-cay-do-va-phu-khai-cha-tu-do`: ĐÃ ĐÓNG

Điều lượt 13 đòi (hunk 1, 2, 4): thay câu "cha tự đỏ … không cùng cơ chế" bằng kết quả đo; thu M8 "Cấm" về "mọi ô còn lại HIỆN TRONG `KQ`"; thêm `B1`, `Ga`, `Gb` làm PHẢI ĐỎ Ở cho hai cửa còn lại.

- **Số đo thay câu cũ khớp từng con số** (dòng 15): cha đỏ 71/72 · 32/32 · 508/508, im lặng duy nhất `ghi_gay` (`kq.get("ghi_gay", [False])` ở `t52`, mã thật dòng 6871 của g1). Khi sửa cả hai phía: `Gb` · `Gc` · `Gd` suite 56/56 (3.12; `Gb` còn 56/56 ở 3.13), `Ga` 56/56 (3.12, 3.13), `GbCon` 55/56 — đúng bốn xanh một đỏ mà r14 khai. Cả bốn cây xanh ĐỎ ở phép so khoá (3 · 11 · 17 · 3). `Gb` 67/67 đột biến đích `t52` GIẾT đúng, bán kính 1/56 (46,5 s trung bình).
- **Danh sách PHẢI ĐỎ Ở nay phủ cả ba cửa**: `P1a` (main, 395) · `B1` (che-do, 56/56 + 90/90 đột biến đích `t53`, 12 < 17) · `Ga`/`Gb` (gom). Một phép so chỉ đọc cửa `main` ĐỎ ở `P1a` nhưng XANH ở `B1` · `Ga` · `Gb` · `Gc` · `Gd` (cột "che-do/main/gom" ở bảng cây: main = 0 ở cả năm) — đúng câu "(đo)" của hunk 4.
- **Chữ M8 "Cấm" đúng với mã**: khối F28 của `t54` (3 chế độ × 3 mã thoát, chạy trong tiến trình) không ghi khoá nào vào `KQ`; công thức đếm điểm mã của `t53` cũng ở cha. Hai khối ấy không được phép so khoá phủ, và r14 nói thẳng điều đó (§10: "chốt nào bắt việc thu hẹp chúng: KHÔNG ĐO"). Khối F28 có 4 mục `DOT_BIEN` riêng, nên không phải vùng không răng — nhưng đó là phép đo của lượt này, không phải điều r14 khai; tôi không dựng cây thu hẹp nó (ngoài phạm vi HẸP) và không coi đó là hồi quy.

### Câu hỏi 2 — cách đọc nghiêm có chặn oan tối ưu hợp lệ M8 hay đổi g1 không: KHÔNG

- `VB` (quét `head` đọc `TEP_TEST` trong bộ nhớ) · `VD` (nhớ đệm `bam({…})`) · `VBD` · `Nap` (thêm ô cuối `_luoi_byte`): XANH ở r12 (iv)(v), r14 chặt và cả hai cách đọc r13, ở 3.11 · 3.12 · 3.13; suite 56/56 (`VB` · `VD` · `Nap`, 3.12). Các cây này **sai khác g1 ở chỗ nào cũng không đổi hình dạng `KQ`**, nên không phụ thuộc vào cách đọc.
- g1 chạy lại 30 biến thể × 3 phiên bản (BẢNG ĐO dòng 18): r14 XANH hai chiều ở cả 30; chữ ký đổi duy nhất ở `("m5b",0)` khi cây đã có `__pycache__`, đường mà chữ r14 miễn. Điều nên nhớ cho executor (đã có từ r12, r14 không làm khác): với `__pycache__` có sẵn, r12 (v) về `E698` ĐỎ — vì thế (v) đòi cây `git archive` không `__pycache__`.
- Điều r14 chủ ý chặn (theo luật cứng): đổi hình dạng `KQ` kể cả khi nội dung kiểm không yếu đi — `VR` (băm `log` ở 503 kịch bản) ĐỎ 503, `VE` ĐỎ 27. Đo thêm (không lên lớp): `VR` chỉ đổi con, không cắt được CPU cửa `main` — `chay_cua.py` 10 lượt xen kẽ ở 3.12, CPU cửa `main` trung vị **3,16 s** (`VR`) so **3,03 s** (g1), min 2,80 so 2,89, dải chồng nhau; JSON `KQ` 763 KB so 2 697 KB (`goi/so-lieu/cpu_vr`). Tức luật cứng của r14 không chặn mất một khoản tiết kiệm CPU nào đo được ở `VR`.

### Câu hỏi 3 — diff r13 → r14 có nới tiêu chí nào khác không: KHÔNG

Bảng theo mục ở BẢNG ĐO dòng 6. Chỉ có ba loại thay đổi: (a) đúng năm hunk của HINT lượt 13 (A10 (v): hai đoạn "(r14)", M8 "Cấm": một mệnh đề thu hẹp phạm vi *lời khai* của phép so, không đụng danh sách các việc bị cấm; §0-r13 (4) "Phủ": thay câu bằng số đo; §10: thay "KHÔNG ĐO"); (b) sổ sách — header, danh sách revision của `land_obligations`, GIỚI HẠN LỜI KHAI, S5 một dòng, §10 một mục r14, §11 Q14, §11.1, bảng (B) Q10/Q14; (c) mục §0 mới (r14) và §0 cũ đổi tên §0-r13 kèm đoạn mở đầu. Không điều kiện DỪNG (S1–S11), tiêu chí A1–A10, mục tiêu M1–M8 (trừ mệnh đề đã nêu), `ci_budget`, `write_set`, `ngoai_pham_vi` hay Phụ lục nào đổi chữ. Bản gốc chữ HINT ngoài một chỗ trỏ `§0`: giữ nguyên.

## DRY-RUN HINT.patch

`goi/HINT.patch`: **tệp RỖNG** (0 byte; sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, băm của chuỗi rỗng) — không còn lớp mở nên không có hunk nào. Không có dòng `---`/`+++` vì một HINT chỉ có đầu tệp mà không có hunk bị `patch` coi là rác (đo: `patch: **** Only garbage was found in the patch input.`, rc=2).

Dry-run trên bản sao của `SPEC.md` đặt ở `ops/specs/ci-g5-cong-cu-va-tiep-r14.md` trong `mktemp -d -p "$R"`:

```
patch -p0 --fuzz=0 --dry-run --verbose < goi/HINT.patch
```
- **rc=0**; thông báo `Hmm...  I can't seem to find a patch in there anywhere.` (0 hunk, 0 dòng `fuzz`, 0 dòng `offset`); tệp đích không đổi (`cmp` rc=0; sha256 vẫn `ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21`); 0 `.orig`/`.rej`. Nhật ký: `goi/log/dry_run_hint.out`.
- Đối chiếu: HINT lượt 13 áp lên r13 đã đo ở BẢNG ĐO dòng 4 (5/5 hunk, 0 fuzz).

## GHI NHẬN KHÔNG THÀNH LỚP

- **M8 "Giữ răng" (dòng 2731) còn chép cách nói r13** — "tập khoá `KQ` … chứa tập của g1 với độ dài mọi danh sách và từ điển lồng không nhỏ hơn (A10 (v))" — không nhắc "cùng đường, cùng loại". Không lên lớp: câu tự trỏ (A10 (v)), là điều kiện CẦN chứ không mâu thuẫn với A10 (v), và A10 (v) là tiêu chí nghiệm thu duy nhất; không cây nào đo được bị đổi kết luận vì dòng này. Nếu muốn dọn, một nửa dòng là đủ ("… cùng đường, cùng loại, độ dài không nhỏ hơn (A10 (v), cách tính r14)"). Có từ r13; r14 không làm khác.
- **`Wpad` và đổi tên khoá lồng có giá trị là số/chuỗi** vẫn lọt — cùng giới hạn đã khai ("(v) đếm số, không so nội dung từng ô"). Đổi tên khoá cấp đỉnh hay khoá lồng có giá trị là danh sách/từ điển thì phép so bắt (`byte.luoi` → `byte.luoi2` ĐỎ ở `kiem_phep_do.py`).
- **Ràng buộc ngầm "giữ 56 ca"** của khoá `m3698-` (lượt 13 ghi nhận): không đổi, r14 không đụng.
- **Đích 0,85 của M8**: `VBD` đo 0,875 ở lượt 13 (Phụ lục I, lượt này không chạy lại); r14 khai thẳng ở §10 rằng đích chưa chứng minh đạt được mà không phạm điều cấm, và S11 là đường ra. Không phải finding.
- **Số vòng**: nếu lượt này được chấp nhận thì đây là vòng thứ tư của mục việc r11 (r11, r12, r13, r14); ý chủ kho về số vòng: KHÔNG ĐO ĐƯỢC (không dùng mạng). Lời nhắc cho phiên điều phối, không phải finding.

## KHÔNG ĐO ĐƯỢC

1. GitHub: #698 (28 comment, mới nhất `6079843708` theo r14), PR #721, lease, comment chủ kho — không dùng mạng ở lượt này; các mệnh đề §0 (1) và hàng "review của r13" về bản chiếu chưa có trên #698: KHÔNG ĐO ĐƯỢC ở đây.
2. Giây thật trên runner `ubuntu-latest`, tải runner, Windows (Q8) — như đặc tả.
3. 419 dò, A5 trọn (470), 54 canh, Phụ lục I trên `W1c` · `Gb` · `Gc` · `Wpad` · `VE` · `Nap` · `VB` · `VD`: không chạy (như §10 r14); Phụ lục I `VBD` 0,875 là số lượt 13.
4. Exact head g2: chưa có; mọi kết luận về g2 là suy từ cây dựng trên g1.
5. Ô chỉ có ở cha (khối F28 của `t54`, công thức điểm mã của `t53`): chốt nào bắt việc thu hẹp chúng ngoài 4 mục `DOT_BIEN` của F28: KHÔNG ĐO ĐƯỢC (không dựng cây thu hẹp) — đúng như §10 r14 khai.
6. Suite `manh` trên 3.11/3.13 cho `B1` · `Ga`(3.11) · `Gb`(3.11) · `Gc` · `Gd` · `Nap` · `VB` · `VD`: KHÔNG ĐO ĐƯỢC (CI ghim 3.12; chỉ đo g1, `W1c`, `VE`, `Wpad` ở cả hai phiên bản và `Gb`, `Ga` ở 3.13).
7. Tính hợp lệ của `VB`, `VD` theo M8 "Được": phán đoán của reviewer (đo được chỉ là chúng không đổi `KQ` và qua suite).
8. Bản `sub/*.json` gốc của lượt 13 cho `Wpad` · `Ga` · `Gd` · `VD` · `VR` · `VB` · `VE` · `Nap` · `W1b`: gói không mang; blob của năm cây có số để so (`B1` · `P1a` · `W1c` · `Gb` · `Gc`) trùng, còn lại là dựng lại từ mô tả (số `numstat` trùng ở `Wpad` 3/2 · `Ga` 0/5 · `Gd` 2/2 · `VE` 1/1 · `Nap` 1/1 · `VB` 2/0 · `W1b` 7/6; `VD` 7/1 so 6/1 và `VR` 1/1 so 3/1 khác ở số dòng — hai cây ấy chỉ dùng để đo `KQ`/suite).

## NHẬT KÝ ĐO (UTC, 09-10)

- Giờ xấp xỉ. 18:25 mở gói; 18:28 kiểm băm, đọc diff r13 → r14, đọc VERDICT/HINT lượt 13 và bộ dụng cụ; 18:30 áp HINT lên r13 (rc=0, 5/5); 18:32 dựng g1 + 16 cây; 18:33–18:37 KQ (144 lượt cây × phiên bản × cửa + 9 lượt g1, rc=0 cả); 18:38 phép so r14; 18:41–19:02 suite 3.12 (9 + 3 cây); 18:44–18:52 g1 chạy lại 30 biến thể; 18:49 `cha_phan_ung`; 18:50–18:58 đột biến `W1c`; 19:15 thử 3.11/3.13; 19:32 đột biến `Gb` xong; 19:54 đột biến `B1` xong; 20:02 suite 3.11/3.13 xong; sau đó đo CPU `VR`, kiểm tự kiểm, dựng `HINT.patch` rỗng và dry-run.
- Sự cố nhỏ: bộ xếp hàng `hang_viec.py` lần đầu tự khớp `pgrep -f` với chính nó và đứng chờ; tôi dừng đúng tiến trình đó bằng `kill <PID>` (không `pkill`), sửa, chạy lại. Mất ~12 phút khe rỗng, không ảnh hưởng số đo.
- Dọn: sau khi đo xong, ba thư mục `mktemp -d -p "$R"` (cây g1 và 16 cây biến thể; thư mục áp HINT; thư mục dry-run) và nội dung `goi/so-lieu/tmp_db`, `goi/so-lieu/tmp_suite` đã xoá bằng `shutil.rmtree` (cây dựng bằng `cp -al` nên con số dung lượng giải phóng đếm trùng hard link); `R` còn ~623 MB. Dựng lại cây: `goi/dung-cu/mk_sub.py` + `dung_cay.py` (lệnh ở BẢNG ĐO dòng 8); toàn bộ KQ ba cửa × ba phiên bản của 17 cây ở `goi/so-lieu/kq`, của g1 biến thể ở `goi/so-lieu/kq_bt`, nhật ký suite/đột biến ở `goi/log/suite`, `goi/log/dotbien`.
- Tiến trình: mọi tiến trình con đã `wait` hoặc kết thúc; không `pkill`, không `rm -rf` (dọn bằng `shutil.rmtree` chỉ trong thư mục tạm dưới `R`); tối đa 4 tiến trình đo song song; không ghi vào venv (kiểm: không tệp nào trong `x698/venv*` mới hơn 18:25); `R` giữ dưới 1,5 GB.
