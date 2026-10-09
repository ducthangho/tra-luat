verdict: changes_requested
reviewed_sha: 35e7f9c8940295d0e0d50eb676fb34394e7acd2d
spec_sha256: 711b7b74e55ee14bb666b467abdc92d9aab5e4ddc5f97cbb68753241d03e4bb1
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như subagent do phiên điều phối giao (cùng họ Anthropic với phiên soạn r13). Model/effort là CẤU HÌNH được giao, không phải runtime evidence (PROTOCOL :754–760 trên `ab457c6`). Định nghĩa `~/.claude/agents/review-opus-max.md` có trên máy này, sha256 `e225b81cf2fbdd0f05a54a689cac17db8972b2f8c0684a0a30931875cd4b792c`, 1175 byte, frontmatter `model: claude-opus-5-5`, `effort: max` (khớp băm ghim ở ghi chú dưới closure); lượt này CÓ được giao qua định nghĩa ấy hay không: KHÔNG ĐO ĐƯỢC từ phía tôi. Không mạng, không đăng GitHub, không commit/push, không sửa `$R/cay-kho`; chỉ ghi dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`; TMPDIR=`$R/tmp`.

Kết luận nội dung: **0 P1 / 1 P2 / 1 P3** (theo lớp).
- **P2 `tuong-tac-677-kiem-ke-t70-chua-neu` — CÒN MỞ** (lượt 8, 9, 10, 11, 12, 13). Sáu đường của lượt 12 (E1, E2b, E3, E4, E5, E6b) ĐÃ ĐÓNG THẬT (H2, (S) r13; đo lại ở 3.11 và 3.12). Biểu hiện MỚI, CÓ TỪ TRƯỚC r13: **F13-1, họ E8** — ca gọi BẢN SAO helper trong một module NẠP LẠI từ chính tệp test (globals mới: guard chưa vá, lớp `BoQuaNen` riêng), CÙNG tiến trình. E8a (`importlib.util.spec_from_file_location`), E8c (`exec` cả tệp), E8d, E8f, E8g qua `t70` (khi thêm `mong`), `t193`, `t204`, phép quét động theo chữ r13 (`quet13.py` của chính phiên soạn: N, K, N − D, H − D, H2 − D), (S) r13 và (S) của HINT lượt 12, ở 3.11 lẫn 3.12 — mà `main()` chạy như `__main__` dưới mô phỏng `nt` ĐỎ (E8a/c/d/f; E8g: KHÔNG ĐO ĐƯỢC). Lời khai A8 *"Còn lại sau H, H2 và (S): … E5f (tiến trình con)"* và *"H2 thấy cả khi helper là BẢN SAO"* rộng hơn phép đo; (iii) không được đo là đạt bằng máy cho họ này. HINT nhóm 1: thêm vế lật `os.name` trong khung guard (khoá theo tên HOẶC bytecode) vào seam của phép quét động — đo: bắt E8a, E8c, E8d, E8f; nền, 38 biến thể cũ và quét ĐỦ nền giống hệt bộ quét r13 (0 báo nhầm); phần còn lại khai thẳng (E5f; E8e luồng `_thread` thô, đo ĐỎ dưới mô phỏng; E8g thân guard bị sửa).
- **P3 `chinh-xac-hoa-so-hieu-va-tham-chieu` — CÒN MỞ.** Sáu biểu hiện lượt 12 ĐÃ ĐÓNG; ba biểu hiện mới trong CHỮ MỚI của r13: (a) "123 mục chuỗi ở 23 lease (thêm 2 null)" — là 21 cặp + 2 cặp `null`, đơn vị là cặp; (b) "59 cặp … khai `scope_files`" — 39/59; (c) "mười một dạng … rc=11 ở …" kể 9 dạng. HINT nhóm 2.
- **`thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2 lượt 7–12) — ĐÃ VÁ THẬT.** Trọng tâm (1): không tìm ra đường nào để một lease CÒN HẠN giữ write set mà chuỗi r13 CẤP, ngoài miền tệp đã khai (đo: miền ấy trùng miền của workflow đăng): 17 ca trực tiếp mới, 33 ca của phiên soạn, 11 dạng tên lượt 12, 106 kịch bản × 3 bản. Lời khai *"đo hiệu ứng lên splitlines, không liệt kê ký tự"* đúng (mã :159 + GS, RS, CRLF, U+2028/FS ở cuối tên ⇒ 12). Danh sách cho phép hình dạng mục chỉ có thể THÊM người giữ (mục ngoài danh sách tính PHỦ), không bớt; khoá YAML lặp đọc y như cổng đăng (quan sát, không phải lỗi).
- **Không có P1:** làm đúng chữ r13 thì packet land hợp lệ trong trường hợp thường; r13 đổi đúng những gì nó khai (hàng `objective`, `review_class`, `risk`, `executor`, `environment`, `reviewer`, `spec_hash` và năm hàng closure giống BYTE r12; §1, §5, §6, A1, A3–A6, A9, A10 giống byte).

Tỷ lệ vá thật 12→13 (§12, chỉ báo): U = 3 lớp, F = 1 ⇒ **1/3 = 33%**; theo finding 9/9. Chuỗi: 7→8 0/5, 8→9 2/7, 9→10 1/4 (2/4), 10→11 2/4, 11→12 0/2, 12→13 1/3 — hai chuyển tiếp liền nhau < 50%; Q13 (lặp không trần) đã quyết nên đây là số báo cáo.

Trả lời ba trọng tâm. (1) `s5.py` r13 + `_quet_lease_toan_kho`: giữ — không CẤP nhầm ngoài miền khai (BẢNG SĂN S1–S3). (2) (S): 0 báo nhầm trên năm ca hợp lệ đúng; các dạng gợi ý (`getattr` động, `eval`, decorator, `__dict__`, `attrgetter`, f-string) đã bị cổng động hay (S) bắt hoặc thuộc E5f; riêng `importlib`/`exec` cả tệp mở họ E8 (P2). (3) Số hạng: 106 (61/36/9 × 3 bản, từng hàng), 1307 lượt (từng hàng), 38 biến thể (25 ĐỎ; 19/7/6/1/5/0), đột biến (S) 18/7/2/1, 33 ca, 21 đột biến đơn vị, baseline quét đủ — tái lập đúng; 473 ref và các số `adg2` KHÔNG ĐO ĐƯỢC (không mạng), hiện vật nhất quán trừ ba câu P3.

## KIỂM ĐẦU VÀO

```
$ sha256sum $R/SPEC.md
711b7b74e55ee14bb666b467abdc92d9aab5e4ddc5f97cbb68753241d03e4bb1  SPEC.md      # khớp PROMPT
$ git -C $R/cay-kho rev-parse HEAD
35e7f9c8940295d0e0d50eb676fb34394e7acd2d                                      # khớp reviewed_sha
$ git -C $R/cay-kho config core.abbrev
7
```
`kho.git`: `origin-master` = ab457c651eb4428705f0492163080b661c858b72 (nền r13), `master` = 423b4ba (gốc nhánh), `r13`/`claude/spec-wp678-r7` = 35e7f9c; 9 nhánh + 42 tag, KHÔNG phải 472 nhánh máy chủ. Công cụ: python 3.11.15, 3.12.3, 3.13.12; PyYAML 6.0.1; git 2.43.0; GNU patch 2.7.6; shellcheck; actionlint (`~/.local/bin`).

## NHẬT KÝ TĂNG DẦN

- 13:2xZ sha256 r7..r13 trong `cay-kho` (`git show HEAD:<tệp> | sha256sum`): đủ bảy băm khớp PROMPT; commit tạo mỗi tệp
  (`git log --diff-filter=A`): 088511f, f958e14, 2469f3e, 42292b4, e48423a, d5a57c1, 35e7f9c. `cmp SPEC.md
  ops/specs/...-r13.md` rc=0; `cmp SPEC-r12.md ...-r12.md` rc=0.
- 13:2xZ `s5.py` trích từ CHÍNH SPEC.md (rào ```python sau dòng `**\`s5.py\`**`): dòng 119–325, 207 dòng;
  `git hash-object` = c730245ceea8cc5368d5ef84f8e296cd35102694; sha256 708790485694de7d2379928fec30f09dd8491803677764c94b2c7a55841d02f6;
  0 dấu chéo ngược — KHỚP lời khai. `cmp` với `r13do/s5_tu_r13_cuoi.py`, `r13do/l2/s5/s5.py`, `r13do/live/ra1/T/s5.py`: rc=0.
  Khối chuỗi lệnh (dòng 63–99, 37 dòng) `cmp` với `r13do/khoi_cuoi.txt` và `r13do/live/khoi_r13.txt`: rc=0.
- 13:2xZ 38 ca tự kiểm của `s5.py` (nạp như module, `cham` trên `CA` + `tu_kiem_goi_git`): 3.11.15, 3.12.3, 3.13.12 ⇒
  `CA 32 sai [] goi_git 6 sai []` ở cả ba.
- 13:31:52Z–13:40:22Z 106 kịch bản chuỗi (`tat_ca13.py` của phiên soạn, chép vào `w13.*/l2`, harness KHÔNG sửa;
  `H12_R12=$R/SPEC.md`, `H12_S5=<s5.py trích từ SPEC.md>`; `goi/do/chay_106.sh`): 3.11 / 3.12 / 3.13 đều
  `kịch bản 106 | KHÔNG CẤP 61 | KXĐ 36 | CẤP 9 [S0, S15, K_ops_reviews, K_ops_lease, K_ops_leases, N3_url_cho_phep,
  R5_ngoai_ops_leases, R5_thu_muc_hoa, R5_duoi_cach]`; so TỪNG HÀNG với `r13do/l2/chuoi/tat_ca13_py3.1x.json`:
  0 lệch nhãn, 0 lệch chữ ở cả 106 hàng × 3 bản; 0 `.pyc`; thư mục kịch bản (554 MB mỗi lượt) dọn bằng shutil.
- 13:38:20Z–13:38:42Z 17 ca trực tiếp MỚI cho hướng (1) (`goi/do/f1/do_f1_rev13.py`, chép khung `do_f1a.py`, bảng ca
  của tôi; `ketqua/f1_rev13_py311.txt`). Xem BẢNG SĂN S1.
- 13:4xZ Đột biến mức ĐƠN VỊ của `s5.py` (`dot_bien_s5_r13.py` của phiên soạn, chạy trên bản chép): 21 đột biến;
  `don_vi_py3.11/3.12/3.13.json` `cmp` bằng của phiên soạn (rc=0 cả ba); 21 tệp `hai_lop_*.py` giống hệt.
- 13:40Z–14:25Z ĐO HƯỚNG (2) — họ E8 (bản sao helper trong module NẠP LẠI, cùng tiến trình): `goi/do/e8/dung_e8.py`
  dựng E8a/b/c; E8d, E8e, E8f, E8g dựng tay (cùng mẫu: chèn `t204_moi` trước `def main(` như `bt/`). Bộ chạy
  `chay_e8_day_du.py` (MỘT lệnh, 3.11 + 3.12 song song, cây tối thiểu = bản chép `r13do/l2b/nen`, trả nền + kiểm sha256
  sau mỗi biến thể): lượt 1 NỀN + 38 biến thể của phiên soạn + E8a/b/c (`ketqua/e8_day_du.txt`), lượt 2 E8d
  (`ketqua/e8d.txt`), lượt 3 NỀN + 38 + E8a–E8f với bộ quét khoá-bytecode (`ketqua/e8_lan3.txt`), lượt 4 E8g
  (`ketqua/e8g.txt`). Mọi lượt: trả nền đúng N/N, 0 `.pyc`.
- 13:4xZ (S) r13 (`s13.py` của phiên soạn) trên E8a–E8g: rc=0 cả bảy ở 3.11/3.12/3.13; (S) HINT lượt 12
  (`luot12/do/quet_s_ast.py`): rc=0 cả năm biến thể E8a–E8e ⇒ họ E8 CÓ TỪ TRƯỚC r13.
- 13:4xZ Tái lập: 33 ca trực tiếp `do_f1a.py` (0 lệch rc); 91 hàng cũ so json lượt 12 (0 lệch nhãn, chỉ N4×2 khác chữ);
  (S) 25/38 và phủ chéo 19/7/6/1/5/0 ở 3.11 và 3.12; `dot_s13.py` 18/7/2/1 ở 3 bản (đầu ra `diff` bằng của phiên soạn);
  11 dạng tên tệp của lượt 12 (`tai_hien_ten_tep_s5.sh`, cột cuối đổi sang `s5.py` r13).
- 13:50:08Z–14:19:13Z quét ĐỦ nền `ab457c6` (hai clone đầy đủ từ `kho.git`, MỘT lệnh, hai bản song song) bằng
  `quet13.py` của phiên soạn rồi `quet13_lat.py` (đề xuất, khoá theo tên guard): xem BẢNG ĐO.
- 14:25:45Z–14:41:04Z quét ĐỦ nền bằng `quet13_lat2.py` (đề xuất cuối, khoá theo tên HOẶC bytecode guard): cùng mọi tập
  như `quet13.py` ở 3.11 (784,0 s) và 3.12 (919,8 s); status 0, 0 `.pyc` (`ketqua/quet_du_nen_lat2.txt`).
- 14:26:32Z–14:50:09Z chạy lại 1307 lượt đột biến chuỗi (`dot13.py` của phiên soạn trên bản chép, `H12_R12=SPEC.md`):
  bảng in ra `diff` bằng `r13do/l2/dot13.out` (trừ dòng thời gian); `dot13.json` 1307/1307 khoá chung, 0 lệch nhãn, 0 lệch
  chữ, 0 `.pyc` (`ketqua/dot13_tai_lap.out`).
- 14:4xZ HINT.patch dựng bằng `goi/do/mk_hint13.py`; dry-run, áp thật, áp từng nhóm: xem DRY-RUN.
- 14:52:02Z–14:52:18Z E8f với bản đề xuất khoá theo TÊN (`lan6/`): không bắt (K rỗng), mô phỏng khoá-tên cũng mù ⇒ khoá theo
  tên thua phép đổi tên guard; bản khoá-bytecode (lượt 3) bắt (`ketqua/e8f_khoa_ten.txt`).
- 13:5xZ Hướng săn khác: so hàng r12↔r13; Q readback 30/30; §2 `grep` 38/19 + 19 tọa độ; code point 3/11/13; số hạng nền
  trên `kho.git`; miễn trừ (`coord`); CLI `bien_nhan_v2` trên clone đủ `ab457c6` (186 ĐẠT … tổng 239, rc=0);
  hiện vật chạy thật r13 (`r13do/live/ra1`); miền đăng của workflow (`git diff` pathspec).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 12 (Claude Sonnet 5.5 max, trên `d5a57c1`; VERDICT `eb28deae…2e3f`, HINT `e1b57491…ad23`, băm đo lại khớp): 0 P1 / 2 P2 / 1 P3, ba lớp. Nhãn theo PROTOCOL §8 (:678–680) và §8.3 (:784–800 trên `ab457c6`): lớp ĐÃ VÁ THẬT chỉ khi mọi biểu hiện trong phạm vi đã đóng (tôi tự đo), không còn biểu hiện cùng cơ chế do bản vá sinh ra, không còn phần phải đo. Cột finding dùng bốn nhãn của §8.

| lớp (lượt 12) | finding lượt 12 | nhãn finding trên r13 | nhãn LỚP lượt 13 | bằng chứng tự đo |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2) | F12-1a tệp lease bị lọc theo TÊN (nháy kiểu C, đuôi hoa) | **ĐÃ VÁ THẬT** | **ĐÃ VÁ THẬT** (đóng ở lượt 13; mở từ lượt 7) | 106 kịch bản × 3 bản: sáu hàng R1 CẤP nhầm ở r12 nay KHÔNG CẤP rc=11; 11 dạng tên của lượt 12 trên `s5.py` r13: rc=11 ở 9, rc=12 ở LF, rc=1 ở không-UTF-8, 0 rc=0 (`ketqua/ten_tep_11_r13.txt`); 33 ca `do_f1a.py` tái lập 0 lệch. Cửa mới mà chính HINT lượt 12 mở (tiêm dòng qua ký tự ngắt dòng, symlink, gitlink) đã do r13 đóng: R5 bốn hàng tiêm dòng, symlink ánh xạ, gitlink ⇒ KXĐ; tôi thử thêm GS, RS, CRLF, U+2028 và FS ở CUỐI tên ⇒ rc=12 cả năm (`ketqua/f1_rev13_py311.txt`). Phép kiểm `x.splitlines() != [x]` ĐÚNG là đo hiệu ứng lên bộ tách (đọc mã :159; `_quet_lease_toan_kho` :678 dùng cùng `str.splitlines`) |
| | F12-1b "không diễn giải được" là danh sách CẤM | **ĐÃ VÁ THẬT** | | năm hàng R4 CẤP nhầm ở r12 nay KHÔNG CẤP; bốn hàng R6 (`type` lạ, khoá lạ, thiếu `type`, dấu chấm cuối) KHÔNG CẤP; ca của tôi `!!set`, `PLANNED:`, ánh xạ vô hướng ⇒ rc=11; đột biến đơn vị 21/21 cùng bảng với phiên soạn ở 3 bản |
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | F12-2 sáu đường E1, E2b, E3, E4, E5, E6b lọt mọi vế | **ĐÃ VÁ THẬT** (cả sáu) | **CÒN MỞ** (lượt 8, 9, 10, 11, 12, 13): biểu hiện MỚI F13-1 (họ E8), CÓ TỪ TRƯỚC r13 | ma trận của tôi, 3.11 và 3.12: E1, E2b, E3, E4, E6b ⇒ H2 − D có `t204`; E5 ⇒ (S) r13 ĐỎ (`ketqua/e8_day_du.txt`). E8a, E8c, E8d, E8f, E8g ⇒ `t70`, `t193`, `t204` `1/1`, `quet13.py` của phiên soạn không bắt, (S) r13 xanh, mà `main()` dưới mô phỏng `nt` trung thực ĐỎ (E8a/c/d/f; E8g: KHÔNG ĐO ĐƯỢC, xem CHI TIẾT). (S) của HINT lượt 12 cũng xanh ở E8a–E8e ⇒ không do r13 sinh |
| `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3) | (a) băm `dbf3b905…8f67` | **ĐÃ VÁ THẬT** | **CÒN MỞ** (sáu biểu hiện cũ đóng; ba biểu hiện mới cùng nguyên nhân ở CHỮ MỚI của r13) | dòng 42 r13 ghi `…8f67`; `git show ab457c6:ops/lease_publish.py \| sha256sum` = dbf3b905…8f67 |
| | (b) lệnh `grep` D1–D9 | **ĐÃ VÁ THẬT** | | `grep -c lease_id` = 38, lệnh cũ = 19; cả 19 tọa độ D1–D9 trên blob `93cff2f` có `lease_id` |
| | (c) dict comprehension | **ĐÃ VÁ THẬT** | | §4 và A2 r13 ghi "list, set hay dict comprehension" (diff r12↔r13 đúng hai dòng ấy) |
| | (d) điều kiện fixture A7 | **ĐÃ VÁ THẬT** | | A7 r13 thêm đúng câu fixture qua `_kiem_provider_identity` |
| | (e) "mười ba code point" | **ĐÃ VÁ THẬT** | | brute-force 3 bản Python: NFC→ASCII 3 (U+037E, U+1FEF, U+212A), casefold 11, NFC(casefold) 13 — khớp chữ r13 :464–467 |
| | (f) "năm điều kiện không đổi" | **ĐÃ VÁ THẬT** | | dòng 4–5 r13 ghi điều kiện (1) đo bằng `s5.py` r13, chặt hơn |

Lớp lượt 7–11 đã đóng — có tái phát không: `grep -c -i codex SPEC.md` = 21 (bằng r12), từng dòng là lịch sử r1–r6, trích Q10/Q13, tên lease (`wp709-exec-g2-codex-…`, `plat-x5-…`) hay tên biên nhận; không dòng nào khai codex là reviewer lượt thi hành; hàng `reviewer`, năm hàng closure, `objective`, `review_class`, `risk`, `executor`, `environment` giống BYTE r12 ⇒ `q10-he-qua-mat-nhan-dien-giai`, `dong-reviewer-loi-khai-rong-hon-do`, `duong-review-b-chua-do-dau-cuoi`, `hop-dong-dong-bang-thieu-neo`, `so-do-nen-khong-khop`, `bo-quet-*`: KHÔNG tái phát.

**Tỷ lệ vá thật 12→13 (§12 :1087–1093 trên `ab457c6`, chỉ báo).** U = 3 lớp mở cuối lượt 12; F = {`thu-tu-677-bo-ngo-o-dieu-kien-cap`} ⇒ **1/3 = 33%** (< 50%). Ở mức finding: 9/9 ĐÃ VÁ THẬT (F12-1a, F12-1b, F12-2 cả sáu đường, P3 (a)–(f)). Chuỗi: 6→7 N/A, 7→8 0/5, 8→9 2/7, 9→10 1/4 (2/4), 10→11 2/4, 11→12 0/2, **12→13 1/3**. Hai chuyển tiếp liền nhau (11→12, 12→13) cùng < 50% ⇒ chạm điều kiện dừng §12 lần nữa; Q13 (*"Áp HINT, lặp không trần"*) đã quyết tại checkpoint nên đây là số báo cáo, không phải điểm dừng tự động. Luật một lớp ở ba lượt (:1098–1100): `tuong-tac-677-…` nay ở lượt 8–13 (sáu lượt). Lớp mới ở lượt 13 (ngoài U): không có — biểu hiện mới đều nối vào slug cũ theo §8.3 (cùng nguyên nhân), không đổi khoá để làm đẹp tỷ lệ.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (CÒN MỞ; lượt 8, 9, 10, 11, 12, 13) | **F13-1 — họ E8: BẢN SAO helper trong một module NẠP LẠI, cùng tiến trình** (A8 đoạn *Phép quét động*, *Giới hạn của vế H*, câu *"Còn lại sau H, H2 và (S): … E5f"*). Ca gọi helper của một module nạp lại từ chính tệp test (globals MỚI: lớp `BoQuaNen` riêng, guard chưa vá) qua mọi cổng: `t70` (khi thêm `mong`), `t193`, `t204` dưới posix, phép quét động theo chữ r13 (N, K, N − D, H − D, H2 − D; bộ quét `quet13.py` của phiên soạn), (S) r13 — ở 3.11 lẫn 3.12; mà `main()` dưới `nt` ĐỎ vì guard của bản sao ném `BoQuaNen` của CHÍNH bản sao, lớp `main()` không bắt. Lời khai "còn lại chỉ họ E5f (tiến trình con)" và "H2 thấy cả khi helper là BẢN SAO" rộng hơn phép đo; tiêu chí (iii) không kiểm được bằng máy cho họ này | HINT nhóm 1 (2 hunk): seam của phép quét động THÊM vế lật `os.name` thành `nt` trong khung của mọi hàm có tên `_ly_do_bo_qua_workflow` HOẶC có bytecode bằng guard đã nạp (`sys.setprofile` + `threading.setprofile`); K ghi lớp kèm module; sửa câu H2; thêm đoạn họ E8 (đo) và phần còn lại khai thẳng (E5f, E8e luồng thô, E8g sửa thân guard) + nghĩa vụ handoff liệt kê lời gọi `exec`/`importlib`/`runpy`/`_thread`/`subprocess` mới | E8a, E8c, E8d, E8f ⇒ K có `t204` ((q3) ĐỎ) ở cả hai bản; trên NỀN + 38 biến thể cũ: N, K, N − D, H − D, H2 − D GIỐNG HỆT bộ quét theo chữ r13 (0 khác ngoài các E8 bị bắt), năm ca hợp lệ 0 báo nhầm; quét ĐỦ nền: bản khoá-tên và bản khoá-bytecode đều giống hệt bộ quét r13 ở cả hai bản (N = sổ, N − D ∅, K {t199, t203}, H − D {t193}, H2 − D {t71, t72, t73, t98, t193, t203}; status 0, 0 `.pyc`). Còn lại (đo): E8e lọt mọi cổng kể cả bản đề xuất, mô phỏng `nt` ĐỎ; E8g lọt mọi cổng, kết cục Windows KHÔNG ĐO ĐƯỢC. Windows thật KHÔNG ĐO ĐƯỢC (mô phỏng). |
| `chinh-xac-hoa-so-hieu-va-tham-chieu` | **P3** (CÒN MỞ: sáu biểu hiện lượt 12 đóng; ba mới) | (a) :439–440 *"`effective_write_set` 123 mục chuỗi ở 23 lease (thêm 2 giá trị `null`)"*: bộ đếm `co_khoa_effective` của chính `do_dem.py` tính cả cặp `null`, nên 123 mục nằm ở 21 cặp, cộng 2 cặp `null` = 23 cặp có khoá; và đơn vị là CẶP `(blob, đường dẫn)`, không phải lease. (b) :440–441 *"59 cặp … (lease review chỉ đọc, khai `scope_files`…)"*: `thieu.txt` của phiên soạn cho 39 khai `scope_files`, 6 `scope_files_can_xet`, 6 `delta_scope_files`, 8 không trường phạm vi nào. (c) :507–509 *"Đo cả mười một dạng … rc=11 ở `é`, `ệ` …, `.Yml`; rc=12 …; rc=1 …"* chỉ kể 9 dạng; hai đối chứng (ASCII, có dấu cách) rc=11 không được kể | HINT nhóm 2 (2 hunk): sửa ba câu | (a) phép thử nhỏ chạy chính `do_dem.py`: 3 cặp có khoá (2 danh sách 3 mục + 1 `null`) ⇒ `co_khoa_effective 3`, `effective_write_set:null 1` (`ketqua/do_dem_ngu_nghia.txt`); số 473 ref thì KHÔNG ĐO ĐƯỢC (không `adg2`). (b) đếm trên `r13do/f1b/thieu.txt`. (c) `ketqua/ten_tep_11_r13.txt` |
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | (P2 ở lượt 7–12) **ĐÃ VÁ THẬT** ở lượt 13 | — | — | xem ĐỐI CHIẾU; ca mới của tôi cho hướng (1) không mở biểu hiện nào (BẢNG SĂN S1) |

## BẢNG SĂN

| # | hướng | giả thuyết | lệnh / dụng cụ | output | kết luận |
|---|---|---|---|---|---|
| S1 | (1) tên/kiểu tệp lease lạ có lối CẤP nhầm qua `s5.py` r13 + `_quet_lease_toan_kho` | ký tự ngắt dòng ngoài tám ký tự đã thử, ngắt dòng ở CUỐI tên, `ops` là symlink, mode lạ, `!!set`, `PLANNED:`, ánh xạ vô hướng, khoá lặp, trường hạn khác tên, lease là danh sách | `goi/do/f1/do_f1_rev13.py` (khung `do_f1a.py`, mỗi ca một máy chủ riêng, lease CÒN HẠN giữ `ops/lease_publish_test.py`), python 3.11 | nền / r13: GS, RS, CRLF tiêm dòng 0/12; U+2028 và FS ở cuối tên 0/12; `ops` là symlink 12/12 (chốt tổ tiên của sổ thu hồi `_kiem_to_tien_la_tree` bắt trước); mode `100664` 11/11 (git chuẩn hoá về `100644` khi đọc cây); `!!set`, `PLANNED:`, ánh xạ vô hướng 0/11; `lease_until` thay `lease_expires_at_utc`, hạn không múi, lease là danh sách 12/12; khoá `write_set` lặp, giá trị phủ đứng SAU 11/11, đứng TRƯỚC **0/0** | KHÔNG PHẢI LỖI. Khoá lặp: cổng đăng đọc CÙNG giá trị (`_doc_yaml` = `yaml.safe_load`, PyYAML lấy giá trị sau ⇒ `['ops/khac.py']`), nên chuỗi nhất quán với cổng; loader nghiêm của chính kho (`_nap_yaml_khong_trung_khoa`, chỉ cho sổ thu hồi) thì ra 12 — gợi ý làm cứng, không phải finding |
| S2 | (1) danh sách cho phép hình dạng mục có từ chối dạng `kiem()` nhận mà PROTOCOL coi là phủ | từ chối ⇒ tính PHỦ (chặt hơn), không cấp nhầm; ngược lại (diễn giải được mà không phủ trong khi §5 phủ) | đọc `phu()` + ca ở S1 + 21 đột biến đơn vị | trong bảng chữ, phép khớp = exact/prefix sau separator, case-fold; mọi dạng ngoài bảng ⇒ PHỦ | KHÔNG PHẢI LỖI (giá tính sống đã khai) |
| S3 | (1) miền tệp đã khai có trùng miền workflow đăng | `ops/Leases/`, `x.yaml ` (dấu cách cuối), `x.YAML`, `x.yaml.nhap` không được đăng | đúng lệnh `git diff --name-only --diff-filter=ACM A B -- 'ops/leases/*.yaml' 'ops/leases/*.yml'` của bước *tìm lease vừa đổi* | chỉ `ops/leases/e.yaml`, `ops/leases/sub/f.yml` | KHÔNG PHẢI LỖI: miền `s5.py` ⊇ miền đăng (còn rộng hơn: hạ đuôi hoa) |
| S4 | (2) (S) danh sách cho phép trên AST + biến thể ngoài 38 | `importlib`, `exec` cả tệp, đổi tên guard, luồng thô… | E8a–E8g, `chay_e8_day_du.py`, mô phỏng `mo_phong_nt.py` | E8a/c/d/f/g qua mọi cổng; E8b chỉ bị bắt vì bộ quét đăng ký tên module; xem CHI TIẾT | **LỖI** — P2 `tuong-tac-677-…` (F13-1) |
| S5 | (2) các dạng gợi ý khác: `getattr` chuỗi động, `eval`, decorator, `__dict__`, `operator.attrgetter`, f-string | đường gọi helper GỐC trong tiến trình hiện tại thì H/N bắt; chuỗi chứa `chay_buoc_` thì (S) bắt | ma trận 38 biến thể (N1 getattr, M1 eval, N6 decorator, M3 dict, E5e tên chẻ) + đọc luật (S) | N1/M1/M3/N6: N − D, H − D, H2 − D bắt; `attrgetter("_chay_buoc_…")` là `Constant` ⇒ (S) ĐỎ; f-string tách mảnh: trong tiến trình ⇒ H bắt (như E5e), tiến trình con ⇒ họ E5f (đã khai) | KHÔNG PHẢI LỖI ngoài F13-1 |
| S6 | (2) 0 báo nhầm của (S) r13 và bộ quét đề xuất trên ca hợp lệ | — | M7, R11, R12, L1, E5c × 2 bản | (S) r13 xanh cả năm; `quet13_lat*` không xếp `t204` vào K/N − D/H − D/H2 − D | đúng lời khai (0 báo nhầm) |
| S7 | (3) số hạng r13 | 106/61/36/9; 33 ca; 21 đột biến đơn vị; 1307 lượt; 38 biến thể/25 ĐỎ; 19/7/6/1; 18/7/2/1; baseline; 473 ref | xem BẢNG ĐO | khớp ở mọi số đo lại được, kể cả 1307 lượt; 473 ref KHÔNG ĐO ĐƯỢC | khớp (trừ P3) |
| S8 | phạm vi r12→r13 | có byte kỹ thuật đổi lén? | so hàng bảng, §1–§6, A1–A10 bằng script | giống byte: `objective`, `review_class`, `risk`, `executor`, `environment`, `reviewer`, `spec_hash`, 5 hàng closure, §1, §5, §6, A1, A3–A6, A9, A10; khác: §2 (lệnh `grep`), §4 (dict comprehension, tên tệp r13), A2 (1 dòng), A7 (fixture), A8, §3 (đoạn "Áp vào r13"), header, `depends_on`, nền nghiệm thu, `thay_the_cho`, `nguon_cap_viec` | KHÔNG PHẢI LỖI (đúng phạm vi khai) |
| S9 | assurance / closure / miễn trừ | — | `review-opus-max.md` băm; CLI `bien_nhan_v2`; ba lệnh `coord` trên `ab457c6` | e225b81c… 1175 byte; "186 ĐẠT v2 · 11/11 · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 239" rc=0; `coord` 4 dòng, khớp 0 (grep rc=1), `coord.neo` 2 dòng | KHÔNG PHẢI LỖI |
| S10 | nguyên văn Q8, Q10–Q13 | — | sha256/số byte thân `readback-*.json`; 30 dòng trích `>` | 3a8c40a6…/1187, 69cc35b1…/2151, 392069d1…/1741, 4c9d5e19…/1648, 5f1ff74e…/1662, 0 thực thể HTML; 30/30 dòng có nguyên văn (thân readback hoặc `r13do/gh/i682.json`) | KHÔNG PHẢI LỖI |
| S11 | tương tác #677 / nền | — | `merge-base --is-ancestor` trên `kho.git` | 20ec8d5, 163fd5d, 89fc4fa, 423b4ba đều là tổ tiên của ab457c6 (rc=0) | KHÔNG PHẢI LỖI |
| S12 | (2) ca tự vô hiệu guard (`mock.patch.dict(globals(), {"_ly_do_bo_qua_workflow": …})`) rồi gọi helper gốc | dưới seam, guard của ca thắng seam ⇒ helper chạy như posix ⇒ đạt; trên Windows kết cục tuỳ helper chạy được hay không | biến thể E9 (`goi/do/e8/bt_9/`), `lan5/chay_e8_day_du.py`, 3.11 + 3.12 | `t70`, `t193`, `t204` `1/1`; `quet13.py` và bản đề xuất không bắt; (S) r13 xanh; mô phỏng `nt` của tôi cũng `rc=0` (guard của ca là lambda, không khớp tên hay bytecode) (`ketqua/e9.txt`) | KHÔNG ĐO ĐƯỢC: kết cục trên Windows tuỳ helper chạy được trên Windows hay không (trái (iii) chỉ khi nó ĐỎ ở đó); không xếp hạng, nêu để phiên soạn cân nhắc |

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được (lệnh / hiện vật) | khớp? |
|---|---|---|---|
| sha256 r13; r7–r12; commit tạo | 711b7b74…; bảng PROMPT; 088511f…35e7f9c | `git show HEAD:<tệp> \| sha256sum` ×7 khớp; `git log --diff-filter=A` đúng 7 commit | KHỚP |
| `s5.py` dòng, OID, sha256, dấu chéo ngược | 207; c730245c…2694; 70879048…02f6 | 207; c730245ceea8cc5368d5ef84f8e296cd35102694; 708790485694…02f6; 0 | KHỚP |
| `s5.py` tự kiểm | 38 (32 `CA` + 6 `bao_goi_git`) | 38/38 ở 3.11.15, 3.12.3, 3.13.12 | KHỚP |
| 106 kịch bản chuỗi × 3 bản | KHÔNG CẤP 61, KXĐ 36, CẤP 9 (sáu hàng sạch/khai + ba hàng miền) | 61/36/9 ở cả ba; 0 lệch nhãn/chữ từng hàng so json phiên soạn (`ketqua/tat13_rv3.1x.txt`, `tat_ca13_pyrv3.1x.json`) | KHỚP |
| 91 hàng cũ so json lượt 12 | cùng nhãn 91 hàng × 3 bản (56/29/6); chỉ N4 ×2 khác chữ | đúng vậy ở cả ba bản | KHỚP |
| 33 ca trực tiếp `do_f1a.py` | nền rc=0 25, rc=11 3, rc=12 5; HINT rc=0 19; r13 rc=0 3, rc=11 13, rc=12 16, rc=1 1 | chạy lại 13:46:41Z–13:47:30Z: y hệt, 0 lệch rc (`ketqua/f1a_tai_lap_py311.txt`) | KHỚP |
| 21 đột biến đơn vị `s5.py` | bảng §10 :2256–2263 | `don_vi_py3.1x.json` `cmp` bằng của phiên soạn ×3; in ra đúng từng ca ĐỎ | KHỚP |
| 1307 lượt đột biến chuỗi | bảng §10 :2263–2277, 0 `.pyc` | chạy lại 14:26:32Z–14:50:09Z: bảng `diff` bằng của phiên soạn; `dot13.json` 1307/1307, 0 lệch nhãn, 0 lệch chữ, 0 `.pyc` | KHỚP |
| 11 dạng tên tệp của lượt 12 trên `s5.py` r13 | rc=11 ở 7 dạng kể tên; rc=12 LF; rc=1 không-UTF-8; 0 rc=0 | rc=11 ở **9** (thêm hai đối chứng ASCII, dấu cách); rc=12 LF; rc=1 không-UTF-8; 0 rc=0 | lời khai đúng, liệt kê thiếu (P3 c) |
| (S) r13 trên 38 biến thể | ĐỎ 25/38 | 25/38 ở 3.11 và 3.12 (ma trận của tôi) và 3.13 (`dot_s13.py`) | KHỚP |
| phủ chéo trên 38 | động+S 19, chỉ động 7, chỉ S 6, không cổng nào 1 (E5f), 5 hợp lệ 0 báo nhầm | đúng 19/7/6/1/5/0 ở 3.11 và 3.12, cùng tên từng nhóm | KHỚP |
| đột biến của (S) | 18 / 7 / 2 (E5g, E5i) / 1 (N7) | `dot_s13.py` trên bản chép: đầu ra `diff` bằng `r13do/l2b/dot_s13.txt` ở 3 bản | KHỚP |
| baseline quét đủ nền `ab457c6` | 201 = 187 + N 12 + K 2; N = sổ; N − D ∅; K {t199, t203}; H − D {t193}; H2 − D {t71, t72, t73, t98, t193, t203}; 560,1 s / 668,8 s | `quet13.py` của phiên soạn trên clone đủ của tôi: cùng mọi tập ở 3.11 và 3.12; 779,3 s / 934,7 s; status 0 dòng, 0 `.pyc` (`ketqua/quet_du_nen.txt`) | KHỚP (thời gian khác do tải máy chung) |
| lượt chạy thật r13 13:12:13Z–13:13:11Z | 46 bước rc=0; 472/472/472; OID; 75/123 dòng; 0 `CÒN_HẠN`; (iv) 56 s; cả chuỗi 58 s | đọc `r13do/live/ra1` (rc.log, buoc.json, T/*): đúng từng số | KHỚP (đọc hiện vật, không đo lại live) |
| 473 ref; 3986 đường dẫn; 589 cặp; 1407 + 123 mục; 59 cặp; 6 `CÒN_HẠN`; 37081 mục cây | — | KHÔNG ĐO ĐƯỢC (không `adg2`, không mạng; mirror có 10 ref/132 cặp). `r13do/f1b/dem.txt`, `thieu.txt` nhất quán các số; nhưng câu "123 mục ở 23 lease (thêm 2 null)" và "59 cặp … khai `scope_files`" lệch nghĩa so chính hiện vật | P3 (a), (b) |
| §2: `grep -n lease_id` | 38 dòng; lệnh cũ 19; :2106, :2283 có | 38; 19; cả 19 tọa độ D1–D9 có `lease_id` | KHỚP |
| code point | NFC 3; casefold 11; NFC(casefold) 13 | 3 (U+037E, U+1FEF, U+212A) / 11 / 13 ở 3.11.15 (Unicode 14.0.0), 3.12.3 (15.0.0), 3.13.12 (15.1.0) | KHỚP |
| số hạng nền | numstat 161 1 / 372 12 / 54 10 / 90 4; 5 merge; 211 tệp; wp709 18 commit, 17 chạm hai tệp; blob 93cff2f / 7dd06ab; `bien_nhan_v2.py` 38cda51c… | đúng từng số trên `kho.git` | KHỚP |
| CLI `bien_nhan_v2` ở `ab457c6` | "186 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 239", rc=0 | đúng dòng ấy, rc=0, 10,8 s, python3.12, clone đủ của tôi (53 ref) | KHỚP |
| miễn trừ (`coord`) | `ls-tree` 4 dòng; khớp 0; neo 2 dòng | 4; 0 (grep rc=1); 2 (PROTOCOL 1, `ops/lease_publish.py` 1) | KHỚP |
| Q8, Q10–Q13 | sha256/số byte thân; 0 thực thể HTML | 3a8c40a6…/1187; 69cc35b1…/2151; 392069d1…/1741; 4c9d5e19…/1648; 5f1ff74e…/1662; 0 | KHỚP |
| định nghĩa `review-opus-max` | e225b81c…, 1175 byte | e225b81c…, 1175 byte, `model: claude-opus-5-5`, `effort: max` | KHỚP (cấu hình, không phải runtime) |

## CHI TIẾT TỪNG LỚP

### Lớp 1 — `tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ)

**F13-1 — họ E8: BẢN SAO helper trong một module NẠP LẠI, cùng tiến trình.**

- Cơ chế (đọc mã nền `ab457c6`, `ops/lease_publish_test.py`): `BoQuaNen` khai ở :74 TRONG tệp test; guard `_ly_do_bo_qua_workflow` :613 đọc `(nen or os.name) == "nt"`; hai helper gọi guard qua globals của module của chúng (:3114, :11229). `main()` :11804 chỉ bắt `except BoQuaNen` của CHÍNH module đang chạy (`__main__` khi `python ops/lease_publish_test.py`). Seam của `t193` và của phép quét động A8 (*"vá `_ly_do_bo_qua_workflow` để `nen` mặc định là `nt`"*; `quet13.py` của phiên soạn: `mock.patch.dict(m.__dict__, SEAM)`) chỉ vá MỘT dict module. Một ca nạp lại chính tệp test thành module MỚI (`importlib.util.spec_from_file_location` + `exec_module`, hay `exec` toàn bộ mã nguồn vào một dict) có globals MỚI: guard chưa vá, lớp `BoQuaNen` riêng. Dưới seam, guard của bản sao đọc `os.name` thật (posix) nên helper bản sao chạy thật và ca ĐẠT; trên Windows, guard bản sao ném `BoQuaNen` của bản sao, `main()` không bắt lớp ấy ⇒ `except Exception` ⇒ ĐỎ.
- Biến thể (đều chèn `t204_moi` trước `def main(`, như bộ `bt/` của phiên soạn; nguyên văn ở `goi/do/e8/bt/`, `bt_g/`):
  E8a `importlib.util.spec_from_file_location("ban_sao_204", Path(__file__).resolve())` + `exec_module`, gọi `m2._chay_buoc_dang_that(m2._yaml_that("wp-ok-1"))`, thêm `t204` vào `mong`;
  E8b `importlib.import_module("lease_publish_test")` (cùng thân);
  E8c `exec(compile(<một dòng trống> + mã nguồn tệp, __file__, "exec"), ns)` rồi `types.SimpleNamespace(**ns)._chay_buoc_dang_that`, thêm `t204` vào `mong`;
  E8d như E8c, lấy helper bằng `ns["_chay_" + "buoc_dang_that"]`, KHÔNG sửa `mong`;
  E8e như E8a nhưng gọi trong luồng `_thread.start_new_thread`, đưa ngoại lệ về ca;
  E8f như E8c, mã nguồn đổi tên guard thành `_kiem_nen_x`;
  E8g như E8f, thêm một câu lệnh vào thân guard (bytecode khác).
- Đo (MỘT lệnh mỗi lượt, 3.11.15 và 3.12.3 song song, cây tối thiểu = bản chép `r13do/l2b/nen`; mỗi biến thể: `quet13.py` của phiên soạn `--chi t204`, suite `--chi-ca=t70_`/`t193_`/`t204_`, (S) r13 `s13.py`, mô phỏng `nt`; trả nền và kiểm sha256; 0 `.pyc`). Hai bản Python cùng kết quả ở mọi hàng:

| biến thể | `t70` `t193` `t204` (posix) | t204 ∈ D | `quet13.py` (chữ r13): N, K, N−D, H−D, H2−D | (S) r13 | đề xuất khoá-bytecode: K | `main()` dưới mô phỏng `nt` |
|---|---|---|---|---|---|---|
| M7 (đối chứng, helper gốc, có sổ) | 1/1 ×3 | có | N {t204} (đúng sổ) | xanh | — | BỎ QUA (rc=0) |
| E8a | 1/1 ×3 | có | không xếp `t204` vào đâu | xanh | `t204:BoQuaNen@ban_sao_204` | **ĐỎ** (rc=1) |
| E8b | 1/1 ×3 | có | N {t204} (vì bộ quét đăng ký `sys.modules["lease_publish_test"]`) | xanh | — (N) | **ĐỎ** |
| E8c | 1/1 ×3 | có | không | xanh | `t204:BoQuaNen@ban_sao_204` | **ĐỎ** |
| E8d | 1/1 ×3 | không | không | xanh | `t204:BoQuaNen@ban_sao_204` | **ĐỎ** |
| E8e | 1/1 ×3 | không | không | xanh | **không** | **ĐỎ** (mô phỏng có bọc `_thread.start_new_thread`) |
| E8f | 1/1 ×3 | có | không | xanh | `t204:BoQuaNen@ban_sao_204` | **ĐỎ** |
| E8g | 1/1 ×3 | có | không | xanh | **không** | KHÔNG ĐO ĐƯỢC (mô phỏng khoá cùng tiêu chí nên cũng mù) |

  Tái lập: `cd $R/goi/do/e8/lan3 && TMPDIR=$R/tmp python3 -I chay_e8_day_du.py <thư mục cây> $R/r13do/l2b <bt...>` (cây: `cp -a $R/r13do/l2b/nen <thư mục cây>/cay3.1x`, `bin3.1x/python` trỏ đúng bản); output `ketqua/e8_day_du.txt`, `e8_lan3.txt`, `e8d.txt`, `e8g.txt`.
- Mô phỏng `nt` (`goi/do/e8/mo_phong_nt*.py`): chạy CHÍNH tệp test như `__main__` (`runpy.run_path`, `sys.path[0]` = thư mục script, đúng đường `python ops/lease_publish_test.py --chi-ca=t204_`), lật `os.name` thành `nt` CHỈ trong khung guard (tên hoặc bytecode bằng guard gốc lấy bằng `compile`, không thực thi) để `pathlib` không bị đụng. Đó là MÔ PHỎNG: Windows thật KHÔNG ĐO ĐƯỢC ở đây. Nó tách được đối chứng: M7 ⇒ `BỎ QUA t204_moi … chỉ chạy Ubuntu`, E8a ⇒ `ĐỎ t204_moi: BoQuaNen: (PosixPath(…ops-publish-lease.yml…` — đúng hai nhánh của `main()`.
- Vì sao mọi vế mù: E8a, E8c, E8f, E8g có tên helper như `Attribute.attr` ở cấp đỉnh ⇒ thuộc D (`t70` đòi `mong`, thoả) ⇒ N − D, H − D, H2 − D mù theo CẤU TRÚC; dưới seam ca đạt ⇒ (q1) N vẫn bằng sổ, (q3) K không thêm; H, H2 so code object và lớp của module đã nạp; (S) cho phép `Attribute.attr` trong thân hàm. Họ E8 không thuộc E5f (không tiến trình con, tên helper có nguyên văn), và có từ trước r13 ((S) của HINT lượt 12 cũng xanh ở E8a–E8e).
- Lời khai bị bác: A8 :1204–1206 *"H2 thấy cả … khi helper là BẢN SAO (`exec`, `code.replace`, bản sao dựng ở cấp module) … H2 không thấy ca mà guard không chạy (lỗi trước guard) hay chạy trong tiến trình con"* (bản sao globals MỚI: guard CÓ chạy, trong tiến trình hiện tại, H2 vẫn không thấy) và :1277–1281 *"Còn lại sau H, H2 và (S): … E5f … tiến trình con nằm ngoài mọi hook"* (còn cả họ E8). Nghĩa vụ (iii) vì vậy không được đo là đạt bằng máy cho họ này, trong khi A8 khai *"vế (i), (ii) và toàn bộ (iii) đo thêm như sau"*.

**Phương án (HINT nhóm 1, 2 hunk).** (i) Thêm vào seam của phép quét động một vế đo HIỆU ỨNG: lật `os.name` thành `nt` đúng trong khung của mọi hàm có tên `_ly_do_bo_qua_workflow` HOẶC bytecode bằng guard đã nạp (`sys.setprofile` + `threading.setprofile`, trả giá trị lúc vào khung khi ra), giữ nguyên seam dict cũ; K ghi lớp kèm module, để `BoQuaNen` của bản sao rơi vào K ⇒ (q3) ĐỎ. (ii) Sửa câu H2. (iii) Thêm đoạn "Họ E8" với số đo và phần còn lại khai thẳng; handoff liệt kê lời gọi mới tới `exec`, `eval`, `compile`, `importlib`, `runpy`, `__import__`, `types.FunctionType`, `_thread`, `subprocess` để đọc diff (không phải cổng tự động).

**Phép kiểm của phương án.** Bộ quét đề xuất dựng từ `quet13.py` của phiên soạn bằng đúng phần thêm ấy (`goi/do/e8/quet13_lat.py` khoá theo tên; `quet13_lat2.py` theo tên HOẶC bytecode, bộ đệm theo code object giữ tham chiếu mạnh): (1) bắt E8a, E8c, E8d (cả hai bản khoá) và E8f (chỉ bản khoá-bytecode) qua K; (2) trên NỀN + 38 biến thể cũ (`--chi t204`) N, K, N − D, H − D, H2 − D GIỐNG HỆT `quet13.py` ở cả hai bản (so bằng máy: khác đúng ở các E8 bị bắt), năm ca hợp lệ 0 báo nhầm; (3) quét ĐỦ nền (clone đầy đủ `ab457c6`, MỘT lệnh, hai bản song song): bản khoá-tên cho cùng N (= sổ, đúng cặp), N − D ∅, K {t199, t203}, H − D {t193}, H2 − D {t71, t72, t73, t98, t193, t203} như `quet13.py` (720,5 s / 809,8 s; status 0, 0 `.pyc`); bản khoá-bytecode cũng giống hệt (784,0 s / 919,8 s; status 0, 0 `.pyc`). **Giới hạn của phương án:** E8e (luồng `_thread` thô, ngoài profile) và E8g (thân guard bị sửa) lọt cả bản đề xuất; E5f vẫn khai. Vế lật là THU HẸP, không đóng họ; một vế mạnh hơn (`sys.monitoring` toàn tiến trình) chỉ có từ 3.12, mà A8 đòi cả 3.11.

### Lớp 2 — `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3, CÒN MỞ — sáu biểu hiện cũ đóng, ba mới)

(a) :439–440 *"`effective_write_set` 123 mục chuỗi ở 23 lease (thêm 2 giá trị `null`)"*. Chính script đếm của phiên soạn (`r13do/f1b/do_dem.py`) tăng `co_khoa_effective` cho MỌI cặp có khoá, kể cả khi giá trị `null`, rồi đếm riêng `effective_write_set:null`. Phép thử nhỏ chạy đúng script ấy trên một kho 3 tệp lease (hai danh sách tổng 3 mục, một `null`): `{'co_khoa_effective': 3, 'effective_write_set:chuoi': 3, 'effective_write_set:null': 1, …}` (`ketqua/do_dem_ngu_nghia.txt`). Vậy 123 mục nằm ở 21 cặp, cộng 2 cặp `null`, tổng 23 cặp có khoá; và đơn vị là cặp `(blob, đường dẫn)`, không phải lease (cùng câu ghi "589 cặp").
(b) :440–441 *"59 cặp không có khoá nào trong hai khoá (lease review chỉ đọc, khai `scope_files`; cả 59 `HẾT_HẠN`)"*. Hiện vật của chính phiên soạn (`r13do/f1b/thieu.txt`, bảng `khoa_gan_nghia`): 39 cặp khai `scope_files`, 6 `scope_files_can_xet`, 6 `delta_scope_files`, 8 không trường phạm vi nào (`('prompt_path',)` 4, `('prompt_path', 'spec_path')` 4); vai trò "review chỉ đọc" không có trong hiện vật ấy. Kết luận "không giữ gì" đứng vì 59/59 `HẾT_HẠN`.
(c) :507–509 *"Đo cả mười một dạng … rc=11 ở `é`, `ệ` (R1), nháy kép, dấu chéo ngược, TAB, `.YAML`, `.Yml`; rc=12 ở tên có LF trần; rc=1 … không phải UTF-8"*: kể 9 dạng; `tai_hien_ten_tep_s5.sh` của lượt 12 (chép, cột cuối đổi sang `s5.py` r13) cho rc=11 ở 9 dạng gồm hai đối chứng ASCII và có dấu cách (`ketqua/ten_tep_11_r13.txt`).
**Phương án:** HINT nhóm 2 (2 hunk), chỉ chữ/số; không đổi hành vi.

### Lớp đã đóng — `thu-tu-677-bo-ngo-o-dieu-kien-cap`

Đóng ở lượt 13 (mở từ lượt 7). Bằng chứng ở ĐỐI CHIẾU và BẢNG SĂN S1–S3. Điều tôi đã thử thêm mà không phải lỗi được ghi ở S1 để lượt sau khỏi lặp; riêng khoá YAML lặp là quan sát (nhất quán với cổng đăng), không phải biểu hiện.

## DRY-RUN HINT.patch

Tệp `$R/goi/HINT.patch`: 12620 byte, sha256 `c4f73b988552f0047fda022b0edfbb3531c29a6a61cee9d149e2af23d61141ce`, 2 nhóm mở bằng `# lop: <slug>` ngay trước `--- `, 4 hunk (2 + 2), một tệp đích `ops/specs/lease-id-ep-kieu-yaml-r13.md` (repo-relative, không `a/`/`b/`). Dựng bằng `goi/do/mk_hint13.py` (thay chuỗi có `assert` đếm đúng 1 lần trên SPEC.md r13; diff từng nhóm tính so BẢN GỐC; số liệu từ `goi/do/hint/so.json`). Lệnh (đúng PROMPT, trên bản sao `mktemp -d -p "$R"`, không đụng `cay-kho`); output nguyên văn ở `goi/do/ketqua/kiem_hint.txt`:

```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
patch -p0 --fuzz=0 --verbose < "$R/goi/HINT.patch"
```

```
bản sao: …/tmp.U0lr5lCHsQ/cay HEAD 35e7f9c8940295d0e0d50eb676fb34394e7acd2d status 0 dòng
HINT.patch: 12620 byte, sha256 c4f73b988552f0047fda022b0edfbb3531c29a6a61cee9d149e2af23d61141ce, nhóm 2, hunk 4
== dry-run: checking file …-r13.md · Hunk #1 succeeded at 1195. · Hunk #2 succeeded at 1286.
            checking file …-r13.md · Hunk #1 succeeded at 436.  · Hunk #2 succeeded at 505.   done   dry-run rc=0
== áp thật: 4/4 succeeded, áp rc=0
sha256 sau áp:  38eeafbf1a6c5d0a14ffe5f65577dc89491373f0ebff78f838b3ae2eaf6b8758 2556 dòng
sha256 SPEC_all: 38eeafbf1a6c5d0a14ffe5f65577dc89491373f0ebff78f838b3ae2eaf6b8758
git status:  M ops/specs/lease-id-ep-kieu-yaml-r13.md ; .orig/.rej: 0 ; dấu chéo ngược: trước 1 sau 1
nhóm tuong-tac-677-kiem-ke-t70-chua-neu: áp riêng rc=0; sha256 e02b41c4…8bebe KHỚP SPEC_tuong-tac-677-kiem-ke-t70-chua-neu.md
nhóm chinh-xac-hoa-so-hieu-va-tham-chieu: áp riêng rc=0; sha256 0490b533…d457 KHỚP SPEC_chinh-xac-hoa-so-hieu-va-tham-chieu.md
```

Đọc kết quả: dry-run rc=0, 4 dòng `succeeded`, 0 `FAILED`, 0 fuzz, 0 offset; áp thật rc=0; sha256 sau áp BẰNG `goi/do/hint/SPEC_all.md` (dựng độc lập với `patch`); đúng một tệp đổi; 0 `.orig`/`.rej`; số dấu chéo ngược của tệp không tăng (1 → 1); từng nhóm áp riêng trên bản gốc khớp bản kỳ vọng của nhóm ấy. Bản sau áp giữ nguyên khối chuỗi lệnh (so từng dòng: giống hệt) và khối `s5.py` (trích lại: OID vẫn `c730245ceea8cc5368d5ef84f8e296cd35102694`), nên điều kiện cấp và dòng `grep 38/38` không đổi. HINT chỉ sửa chữ đặc tả; vế lật `os.name` là dụng cụ scratch của executor như (q1)–(q5), không vào write set.

## LƯU Ý CHO PHIÊN ĐIỀU PHỐI (không phải finding)

1. **Danh tính lượt này.** Tôi là Claude Opus 5.5 (`claude-opus-5-5`), effort max, subagent do phiên điều phối giao; định nghĩa `review-opus-max.md` có trên máy với đúng băm ghim (e225b81c…, 1175 byte), nhưng lượt này có được dựng từ định nghĩa ấy hay không thì KHÔNG ĐO ĐƯỢC từ phía tôi. Điều kiện cấp (3) và vế review của `required_checks` đòi lượt `review-opus-max` mức `review_deferred` sạch; lượt này KHÔNG sạch (`changes_requested`), nên dù danh tính được xác nhận, (3) vẫn chưa thoả.
2. **§12 và ADR-0048.** 12→13 = 1/3 theo lớp; cùng 11→12 = 0/2 là hai chuyển tiếp liền nhau < 50%. Q13 (lặp không trần) đã quyết; tôi chỉ báo. ADR-0048 (`docs/adr/0048-tran-vong-review-len-muoi.md` ở `ab457c6`) đặt trần mười vòng review HỢP LỆ (có biên nhận) cho một PR packet, vượt trần phải khai khối `nang_tran` (`ai_nang` là chủ kho); đây là lượt 13 của chuỗi review đặc tả `wp678`. Áp ADR ấy cho chuỗi review đặc tả hay không, và Q13 có thay được khối `nang_tran` hay không, là việc của điều phối/chủ kho, không phải của reviewer (lượt 12 đã nêu).
3. **Hình dạng lặp.** Lớp P2 còn mở vì cùng một hình dạng đã thấy ở lượt 11, 12: dụng cụ đo (seam một dict, so code object/lớp theo danh tính) hẹp hơn thứ nó tuyên bố đo (kết cục `main()` dưới `nt`). Bản vá đề xuất đo HIỆU ỨNG (guard thấy `nt`) nhưng vẫn khoá guard theo tên/bytecode, nên chỉ THU HẸP; đóng dứt điểm cần Windows thật (lượt `windows-latest` của `ci.yml` trên ref thi hành TRƯỚC land — `workflow_dispatch`, xem CLAUDE.md mục *"Gate PR và gate master KHÔNG phải một thứ"*), và đó là lựa chọn của chủ kho, không phải chữ đặc tả tôi đề xuất.
4. **Việc phiên soạn r14 cần làm nếu nhận HINT:** cập nhật bảng *Thay đổi so với r13*, hàng A8 ở đầu tệp, §9 (bộ đếm sau lượt 13), §10; chạy lại phép quét động với dụng cụ của chính phiên soạn có vế lật (tôi chỉ đưa số của dụng cụ tôi dựng từ `quet13.py`); quyết có giữ câu handoff liệt kê lời gọi động hay không.

## GIỚI HẠN VÀ TOÀN VẸN

- **Không mạng.** `adg2` (472 nhánh máy chủ, 473 ref), lease live, REST: KHÔNG ĐO ĐƯỢC; chỉ đọc hiện vật của phiên soạn (`r13do/live/ra1`, `r13do/f1b`, `r13do/gh`). `kho.git` có 9 nhánh + 42 tag; clone đủ của tôi 53 ref.
- **Windows thật KHÔNG ĐO ĐƯỢC.** Kết cục "ĐỎ dưới `nt`" của E8 là của mô phỏng `mo_phong_nt*.py` (lật `os.name` trong khung guard, chạy tệp như `__main__`); mô phỏng tách đúng đối chứng (M7 ⇒ BỎ QUA) nhưng không thay một lượt `windows-latest`.
- **Bộ thử do phiên soạn dựng, tôi dùng lại** (`harness.py`, `h12.py`, `tat_ca13.py`, `dot13.py`, `quet13.py`, `s13.py`, `do_f1a.py`, `dot_s13.py`) từ BẢN CHÉP trong thư mục của tôi, không sửa mã của chúng; kịch bản/biến thể mới (17 ca S1, E8a–E8g, E9) và bộ quét đề xuất là của tôi, lưu ở `goi/do/`. Nếu harness lệch thì cả hai lệch cùng chiều; tôi kiểm bằng tái lập đúng số của phiên soạn trước khi tin hàng mới, và đo trực tiếp ngoài harness ở S1.
- **Trần song song.** Lượt E9 (14:29:59Z–14:30:30Z, hai quét `--chi t204`) chạy chồng lên hai lượt quét đủ ⇒ trong ~31 giây có 4 lượt quét động cùng lúc, vượt trần 2 của chỉ dẫn; các lượt khác giữ ≤ 2. Không lượt nào cho kết quả lạ vì chồng tải (E9 xanh như dự đoán; quét đủ cho cùng tập với lượt trước).
- **Đĩa.** Thư mục của tôi ≤ 0,6 GB lúc cao nhất (thư mục kịch bản 554 MB của một lượt 106 kịch bản, dọn ngay bằng `shutil`; hai clone đủ 365 MB ở lượt quét đủ, dọn khi xong). `luot9/` (1,5 GB) là đầu vào có sẵn.
- **Toàn vẹn đầu vào.** `PROMPT.md`, `SPEC.md`, `SPEC-r12.md`, `r12-r13.diff` giữ băm; `r13do/`, `luot9/`–`luot12/`, `kho.git/`: 0 tệp mới hơn `PROMPT.md`. `cay-kho`: HEAD 35e7f9c…, `status --porcelain --ignored` 0 dòng; chỉ `.git/index` (và mtime thư mục `.git`) được làm mới bởi lệnh `git status` đầu tiên, nội dung cây không đổi.
- **Ràng buộc đã giữ.** Không đăng GitHub, không commit/push, không in biến môi trường hay bí mật; mọi `patch` trên bản sao `mktemp -d -p "$R"`; chỉ giết tiến trình của chính tôi (không cần giết lượt nào).
