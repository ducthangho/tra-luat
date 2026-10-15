verdict: changes_requested
reviewed_sha: c54b502bff2aaf3e9a40f8b0b37a657fa09174c1
spec_sha256: f69bb398441168830443d4e095be18247fc4029c930fce8793cfb6574a652c0a
model/effort tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), effort "max" theo chỉ thị điều phối; chạy bằng SUBAGENT trong phiên điều phối. KHÔNG phải codex. Effort thực đo từ bên trong: KHÔNG ĐO ĐƯỢC.
nhãn assurance của lượt này: `review_deferred` — `ops/bien_nhan_v2.py` dòng 703 (`che_do` chứa "subagent") + dòng 720 (từ chối mọi mức trong ASSURANCE_CAN_DOC_LAP khi tự khai chạy trong phiên điều phối) + dòng 736–739 (cùng họ Claude với executor ⇒ từ chối `cross_approved`). Đặc tả khai đúng điều này (header `assurance đạt được`).
tổng kết: 0 P1 · 4 P2 · 12 P3 — 16 lớp / 56 biểu hiện (đếm lớp và đếm biểu hiện riêng)
ngưỡng áp: đặc tả khai 0 P1 · 0 P2 · 0 P3 ⇒ còn 16 lớp mở thì KHÔNG approve (`changes_requested`).

## TIỀN KIỂM VÀ GIỚI HẠN KHAI THẲNG

Tiền kiểm (PROMPT "Việc đầu tiên"), đã chạy, KHỚP, không dừng:
  $ sha256sum PROMPT.md SPEC.md              -> 6ad7185c99259e49950140bb44642b4a8cd1752dce004b9eb0cb5511bf3ab443 · f69bb398441168830443d4e095be18247fc4029c930fce8793cfb6574a652c0a
  $ git -C cay-kho rev-parse HEAD            -> c54b502bff2aaf3e9a40f8b0b37a657fa09174c1
  $ cmp SPEC.md cay-kho/ops/specs/ci-g5-cong-cu-va-tiep-r2.md -> SAME ; core.abbrev = 7 ; git status rỗng
Bản đầy đủ lệnh + output: `evidence/static_checks.txt`.

Giới hạn (khai trước để không bị đọc thành trần):
  · KHÔNG mạng: KHÔNG ĐO ĐƯỢC ruleset LIVE `20856202`, số ref 459, lease #671 (hạn `2026-10-01T03:35:00Z` đã qua lúc review) và `1235a32`/`bd6ad5d` (`git cat-file` báo không có trong mirror), thời lượng job `12,7–18,2 phút` (cần `readback-jobs-36696528580.json`, không có trong sandbox lượt này), CI thật, Windows.
  · ruff: chỉ có 0.15.8; bản `ci.yml` ghim 0.15.15 KHÔNG ĐO ĐƯỢC (cùng kết luận ở hai bản: 1 lỗi `F841`). `jsonschema` không cài ⇒ ca `t2` luôn `bo_qua` ở mọi phép đo của tôi (đặc tả đo có `jsonschema` ở 3.12.3 nên `t2` chạy).
  · Python: mọi phép đo đột biến chạy trên 3.12.3 (bản CI ghim). 3.11.15 chỉ đo phần tĩnh (|D698|, S1/S2, vét cạn, Phụ lục B). Cột 3.11 của các bảng đặc tả KHÔNG đo lại.
  · Bậc hai (A1/A2/A3/A8 "gỡ riêng một phần miền"): ứng viên tham chiếu `IMP-R2-GO` KHÔNG có trong sandbox và đặc tả không đính công cụ gỡ nhóm. Tôi tái hiện trên ứng viên CỦA TÔI cho nhóm miền `D698`, nhóm `ra` (A2) và họ D (A3) (BẢNG SĂN hàng 13, lớp `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`); nhóm `exc` (A8: ba ô ngoại lệ) KHÔNG đo. Con số "canh SỐNG lại" của tôi so với bảng §1.8.7 của r2 chỉ có nghĩa dưới định nghĩa nhóm tôi nêu ở đó, không phải kiểm lại IMP-R2-GO.
  · A5 trọn (8 mảnh + `--gop`, 459 đột biến) KHÔNG chạy; chỉ chạy 43 canh mới + 47 đột biến cũ nhắm `t53`/`t54` (mẫu mỗi ba).
  · Đĩa dùng chung với phiên khác, dao động từ 36 MB tới 22 GB trống: lượt nền Phụ lục C đầu bị tôi DỪNG ở 144/221 (SIGTERM, chỉ tiến trình do tôi sinh; 0 zombie) để khỏi đầy đĩa; các lượt sau chạy qua `run_g.sh` (tạm dừng bằng SIGSTOP khi trống < 120/60/50 MB) và **bỏ qua ca `t38`** (nó rò 1,4 MB/lượt; ca không liên quan tới mọi dò) bằng đúng cơ chế `do_o_nen.json` có sẵn trong Phụ lục A/C; một số lượt đích `t53`/`t54` còn bỏ `t52` (rò thêm 40 MB tạm; `t52` chỉ đo gom/bộ ghi/registry, không đọc bộ đọc cấu hình). Một dòng bất thường do hết đĩa (`x46_tab_head`: `t52` chết `tin_dung_gia`) đã được CHẠY LẠI; kết quả cuối là `GIET`. `evidence/baseline_C.jsonl` và `candidate_C.jsonl` là hợp nhất cuối.
  · Ứng viên tham chiếu của tôi (`IMP-ME`, +150/−4 dòng, một tệp, dựng CHỈ từ chữ của §5 M1–M5 + 43 canh) nằm trong sandbox dưới `$R/tmp.*/cand` (và các cây biến thể `tv_*`, liệt kê ở mục SANDBOX). Nó KHÔNG thuộc `goi/`, KHÔNG được giao (Q14). Lệnh xoá `rm -rf` bị hệ thống quyền từ chối nên tôi không xoá được; điều phối viên muốn giữ đúng chữ Q14 thì tự xoá `$R/tmp.bTzYbIG8z9` trước khi chuyển sandbox cho ai khác.
  · Hai tệp thử nhỏ (`/tmp/__hint_test.patch` 22 KB và `/tmp/__x` rỗng) bị tôi ghi nhầm ra ngoài vùng cho phép; đã `rm -f` ngay và kiểm lại là không còn (mục SANDBOX). Không ghi gì khác ngoài `$R/goi/` và `mktemp -d -p $R`.
  · Danh sách dò của tôi do tôi liệt kê từ mã nên có thể thiếu; lượt sau tìm ra đường sống nào ngoài danh sách vẫn là finding.

## ĐỐI CHIẾU LƯỢT TRƯỚC (protocol §8/§8.3) — làm TRƯỚC mọi hướng săn mới

Nguồn lượt trước: `luot1/VERDICT.md` sha256 `c825a405a9897a21a356c5c721af1ce703f348d3972dd6c07b5a6b922f2f2133` (Sonnet 5.5 subagent, 0 P1 · 5 P2 · 3 P3 = 8 lớp / 52 biểu hiện, `reviewed_sha dcc2cbc`). Cách đo: tôi dựng ỨNG VIÊN `IMP-ME` chỉ từ chữ của §5/§6 r2 (M1–M5, 43 canh), rồi chạy chính Phụ lục A/C/D/E của r2 trên nền `fc852ff` và trên ứng viên (Python 3.12.3). Từ vựng: ĐÃ ĐÓNG = ĐÃ VÁ THẬT · CÒN MỞ = CHƯA VÁ · TÁI PHÁT = lớp cũ có biểu hiện cùng cơ chế sau bản vá (VÁ HỜ) · VÁ SINH LỖI MỚI.

Kết quả tổng của phép đo ứng viên (số liệu trong `evidence/candidate_C.jsonl`, phân hạng bằng ĐÚNG Phụ lục D của r2):

| tập (Phụ lục D) | dò | nền: SỐNG / GIẾT / KHÁC | ứng viên đúng chữ r2: GIẾT / SỐNG / KHÁC | đặc tả khai |
|---|---|---|---|---|
| T-B (A1) | 155 | 149 / 6 / 0 | 153 / 2 / 0 | nền 149 SỐNG; ứng viên 2 SỐNG (đúng hai dò tương đương) — KHỚP |
| T-C (A2) | 41 | 40 / 0 / 1 | 40 / 0 / 1 (`s_ra_realpath` KHÁC bán kính 2, như nền) | KHỚP |
| T-D (A3) | 12 | 11 / 1 / 0 | 12 / 0 / 0 | KHỚP |
| T-E (A8) | 7 | 5 / 2 / 0 | 7 / 0 / 0 | KHỚP |
| ngoài lớp (`g_`,`t_`) | 6 | 6 / 0 / 0 | 0 / 6 / 0 | KHỚP (SỐNG 6/6 = nợ khai) |
| tổng | 221 | 211 / 9 / 1 | 212 / 8 / 1 | KHỚP |

`so_neo` = 1 ở cả 221 dòng, 0 `LOI_DUNG`, 0 `tin_dung_gia`. Ứng viên qua A4-a (`CONG_CU_TEST_BAN_KINH=manh`: `55/55 đạt; tổng=56, bỏ qua=1` vì thiếu `jsonschema`, `đột biến=459`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0, 204 s; nền: `đột biến=416`, rc=0, 181 s), A4-b (ruff 0.15.8: nền 1 `F841` ở :2606 → ứng viên 1 `F841` ở :2659, đa tập (mã, thông điệp) bằng nhau), A4-c (`ci_dang_ky_test`: `1025/1025`, `TỔNG: ĐẠT`, đầu ra nền và ứng viên GIỐNG HỆT), A4-e (Phụ lục E: ứng viên `sau_moc: []`), A1-(iv) (ký tự nguồn: Cf 0, U+FF01…U+FF5E 0, NFKC khác chính nó = {U+2026}, bằng nền).

| slug lượt 1 (hạng) | trạng thái lượt 2 | bằng chứng tự đo | lớp lượt 2 nối |
|---|---|---|---|
| `tran-cu-adr-0043-da-bi-thay` (P2) | **ĐÃ ĐÓNG** phần P2, **VÁ SINH LỖI MỚI** (2 P3) | `tran_cu: 10` + `tran_cu_nguon` trỏ ADR-0048 (Accepted 2026-09-12; ADR-0048 dòng 117 "Chỗ ở duy nhất của con số trục VÒNG là tệp này"); S6 chép hai quy tắc dừng (protocol dòng 1047, 1054–1055 khớp). Nhưng r2 khai con số "chỉ được chép đúng một chỗ" mà đo được HAI chỗ (dòng 31 và dòng 42); và S6 "chép đúng" bỏ ba mệnh đề của §12 | `tran-vong-so-10-hai-cho` (P3) · `s6-chep-thieu-quy-tac-dung` (P3) |
| `ra-thieu-hang-chuan-hoa-lop-b` (P2) | **TÁI PHÁT** (VÁ HỜ) | `ra` tầng `_doc_che_do`: ĐÃ ĐÓNG (T-C 40/40 GIẾT, nền 40 SỐNG; 12 ô cấu trúc M2 + quét M1). Nhưng CÙNG giá trị `ra`, CÙNG phép, ở hai tầng hạ nguồn (`main`, bộ ghi): 12/12 dò SỐNG | `ra-ha-nguon-main-bo-ghi-chua-co-o` (P2) |
| `luc-luong-chi-quet-truc-khong-quet-tich` (P2) | **ĐÃ ĐÓNG** (phần tích biên); phần "hằng giữa × tọa độ khác" r2 CỐ Ý để ngỏ (§7) | T-D 12/12 GIẾT trên ứng viên (nền 11 SỐNG); lưới 162 kịch bản mới đúng (57 + 56 + 1 + 48); lời khai đã đổi thành "trục trọn + tích biên", đúng phép đo. Lỗ F50 gốc đóng cho mọi hằng: `or len(bo_qua) == 2` và `== 7` nền SỐNG → ứng viên GIẾT; hai biến thể "hằng giữa × tọa độ khác" SỐNG 2/2 (BẢNG SĂN hàng 14) — đã được §7 nêu kèm chi phí (tích đầy đủ ≈ 22–37 s mỗi lượt `t54`) | `s11-1-thieu-cach-doc-q4-q9-q13` (P3, chỉ nhắc cách đọc Q4) |
| `a1-khong-do-vi-tri-thanh-vien` (P2) | **ĐÃ ĐÓNG** cho `bk`/`mh`/`ra`; `head` **TÁI PHÁT** (VÁ HỜ) | 153/155 T-B GIẾT, 2 còn lại chứng minh tương đương bằng vét cạn (§tái hiện bên dưới); 47 dò anh em của lượt 1: nền 43 SỐNG → ứng viên 0 SỐNG. Nhưng `head` chỉ có ba neo + R698/N698: dò nhiều dòng (LF) 4/4 SỐNG, dò "thành viên ngoài R698 × vị trí ngoài neo" 3/3 SỐNG | `head-nhieu-dong-chi-tach-lf-chua-co-o` (P2) · `head-moi-vi-tri-moi-thanh-vien-qua-loi` (P3) · `a1-tap-dong-thieu-do-theo-nhom-unicode` (P3) |
| `khai-khong-do-duoc-nhung-do-duoc` (P2) | Zs: **ĐÃ ĐÓNG**; kiểu ngoại lệ: **TÁI PHÁT** (VÁ HỜ) | Zs: `zs` 4/4 + R-zs 2/2 GIẾT. Ngoại lệ: 3 ô M5 giết 7/7 dò `z_exc_*`, nhưng mở rộng tập bắt sang 12 kiểu khác SỐNG 12/12 | `m5-ngoai-le-chi-ba-kieu` (P2) |
| `muc-tieu-m1-m4-cau-chu-thieu-chinh-xac` (P3) | **ĐÃ ĐÓNG** 5/5 | (a) M2 mỗi phép một ô (12 ô); (b) `setpriv --reuid=54321`: có HOME → `/root/x`, bỏ HOME → `~/x`, HOME rỗng → `/x`, root bỏ HOME → `/root/x` (khớp §1.8.5) và M1/M2 ghim HOME; (c) `chr()` + đo ký tự nguồn (số trên); (d) A7 có mặt; (e) `head`×TAB nêu đúng "tương đương vì strip()" | — |
| `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3) | **VÁ HỜ** (đóng 3/6 trọn: (b)(e)(f); 3/6 hẹp: (a)(c)(d)) | (a) A5 nay kiểm TÊN ✓ nhưng chỉ tên, không nội dung canh; (b) so ruff theo (mã, thông điệp) ✓ đo; (c) Phụ lục E chạy được ✓ (`{"tong":9,…"sau_moc":[]}` khớp) nhưng A4-d vẫn bằng mắt — đúng hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"; (d) tách ĐẠT KHI / PHẢI ĐỎ Ở ✓ nhưng "A1-ii" nay trùng số hiệu; (e) 3.12 ✓; (f) :2318 là nhánh `giet_that`, :2292 là `def _chay_1_ca` ✓ đo | `a5-canh-khong-kiem-bang-do` · `a4-d-khong-co-phep-do-may` · `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (đều P3) |
| `nghia-vu-land-thieu-dinh-nghia-tac-nghiep` (P3) | **VÁ HỜ** (đóng 3/4 trọn) | (a) định nghĩa "đỏ vì hết trần" + neo `trich-log.txt` dòng 1962/2438/2440/2590 ✓ khớp từng dòng; (b) r2 chốt (d) `thu-hoi` "vẫn bắt buộc" nhưng job chưa kích hoạt và không có điểm dừng; (c) phạm vi sổ CI ✓; (d) `land_obligations` 7/8 có nơi ghi/chủ thể ✓ | `thu-hoi-do-khong-co-diem-dung` (P3) |

Hai điểm trọng tâm PROMPT §0:
  · "miền `D698`×vị trí có giết được mọi dò anh em": CÓ — 153/155 T-B + 40/41 T-C GIẾT trên ứng viên đúng chữ; hai dò `m_nfkc_no_bk` và `m_nfkc_khac_bmp_mh` ĐÚNG là tương đương (vét cạn `vet_can.py`: `No`×`bk` = 0 điểm mã, `khác-BMP`×`mh` = 0, cả 3.11.15 lẫn 3.12.3; hai dò SỐNG vì không thể chết). Răng của tiêu chí xem HƯỚNG 2.
  · "trần 300 dòng khả thi": CÓ — `git diff --numstat` của ứng viên = **+150/−4** (một tệp), nếu ngắt mọi dòng ở 120 ký tự ≈ 201; tệp nền đã có 186 dòng > 120 ký tự (max 432) và kho không có cấu hình E501, nên "ngắt ở 120" không phải luật kho. Ước 265–280 của §11.1 điểm 8 là BẢO THỦ so với phép đo độc lập (không phải lỗi; đã ghi trong BẢNG ĐO).

## BẢNG LỚP

Mỗi finding có đúng một slug lớp nguyên nhân; đếm lớp và đếm biểu hiện riêng (protocol §8.3). `reviewed_sha` mọi lớp: `c54b502bff2aaf3e9a40f8b0b37a657fa09174c1`. Cột "nối" chỉ lớp lượt 1 / họ kế thừa §9 của r2 mà lớp này tiếp tục — để điều phối đếm đúng lượt xuất hiện cho checkpoint S6(2).

| slug lớp | hạng | biểu hiện (đếm) | nối lớp lượt 1 / họ §9 | phương án (chỉ mô tả; Q14) | phép kiểm đóng lớp / giới hạn |
|---|---|---|---|---|---|
| `m5-ngoai-le-chi-ba-kieu` | P2 | 12: mở rộng tập bắt của `_van_tay` sang `TypeError` `AttributeError` `KeyError` `LookupError` `AssertionError` `ImportError` `EOFError` `UnicodeEncodeError` `NotImplementedError` `IndexError` `ZeroDivisionError` `MemoryError` — SỐNG 12/12 (đích `t53`, không ca nào chết) trên ứng viên làm đúng chữ M5 (ba ô `ValueError`/`UnicodeDecodeError`/`RuntimeError`) | `khai-khong-do-duoc-nhung-do-duoc` (P2, lượt 1) · `doc-che-do-van-tay` | dẫn xuất ô từ thuộc tính: mọi lớp con cụ thể của `Exception` trong `builtins` không thuộc họ `OSError` (dựng bằng `__new__` khi hàm tạo đòi đối số; 45 lớp trên 3.12.3), kỳ vọng `NEM:<tên lớp>`, giữ ba ô thu hẹp; A8 thêm "mở rộng bằng MỘT kiểu bất kỳ của miền ⇒ GIẾT `t53_…`" | biến thể đo (+14 dòng): 12 dò này + 7 dò `z_exc_*` ⇒ **19/19 GIẾT** đúng `t53_…`, `t53` nền vẫn `qua`. Giới hạn: chỉ kiểu có mặt trong `builtins`; ngoại lệ của thư viện thứ ba ngoài miền |
| `ra-ha-nguon-main-bo-ghi-chua-co-o` | P2 | 12: `ra` đi từ `_doc_che_do` sang `main` (`k, n, ra = tham_so`) rồi bộ ghi (`tep = Path(ra)`); `normpath` `expanduser` NFKC bỏ-Cf bỏ-TAB bỏ-Zs ở `main` (đích `t54`) 6/6 SỐNG và ở bộ ghi (đích `t52`) 6/6 SỐNG | `ra-thieu-hang-chuan-hoa-lop-b` (P2, lượt 1) · `doc-che-do-van-tay` · `main-luc-luong-gia-tri` (F42/F44 đã đòi `ra` nguyên văn ở `main`, nhưng chỉ với strip/lower) | thêm vào `_luoi_noi_main` các đường ra có cấu trúc của M2 (mỗi phép một đường, HOME ghim) và vào kịch bản bộ ghi `ghi_duong` một đường tương tự; đưa các dò vào tập đóng (T-C) + canh | 12 dò `x_main_ra_*`/`x_wr_ra_*` phải GIẾT đúng `t54_…`/`t52_…`. Giới hạn: tôi KHÔNG dựng bản vá cho lớp này (chỉ đo SỐNG); hạ nguồn thứ ba (`--gop <thư mục>`) chưa đo |
| `head-nhieu-dong-chi-tach-lf-chua-co-o` | P2 | 4 SỐNG: `strip().split(LF)[-1]`, `…[0]`, `rsplit(LF,1)[-1]`, `split(CR LF)[-1]` (đích `t53`); +4 dò `splitlines()` chỉ chết nhờ đúng 2 ô tình cờ (U+000B ở head 64) | `a1-khong-do-vi-tri-thanh-vien` (P2, lượt 1) · `doc-che-do-van-tay` | ô nhiễu = chuỗi không-hex ngắn + MỖI ký tự tách dòng Unicode (LF CR CRLF VT FF FS GS RS NEL LS PS) + mã băm hợp lệ, cả hai thứ tự, kỳ vọng `None` từ `_mong_git` (+44 ô) | biến thể đo (+5 dòng): 4 dò LF + 4 dò `splitlines` **8/8 GIẾT**, `t53` nền `qua`. Giới hạn: nhiễu một ký tự `x`; chưa thử nhiễu nhiều ký tự |
| `t53-thoi-gian-khong-co-tieu-chi-do` | P2 | 1: không tiêu chí nào đo thời gian `t53`/`t54`; bản thi công đúng chữ M1 nhưng gọi `_van_tay()` thật cho 122.148 ô `head` chạy cửa con 63,0–65,5 s thay vì 4,2–4,7 s (cùng kết quả `[673234, 122148, [], 0]`) | `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3, lượt 1) | thêm tiêu chí A4-g: `t53` ≤ nền + 8 s, `t54` ≤ nền + 4 s, đo cùng lệnh; ghi mẫu trỏ `TEP_TEST` sang tệp tạm trong phạm vi phép quét `head` | đo lại: `python3.12 ops/cong_cu_test.py --tu-kiem-che-do` trên bản trỏ `TEP_TEST` vs bản không trỏ. Giới hạn: thời lượng trên runner CI KHÔNG ĐO ĐƯỢC (chỉ ngoại suy từ hệ số 2,0–2,8 của chính r2) |
| `a1-tap-dong-thieu-do-theo-nhom-unicode` | P3 | 4: nhóm Mc, Me, Pf, Pi không có dò riêng; bản dùng DANH SÁCH nhóm (Cc Cf Zs Zl Zp + NFKC khác chính nó) thay vì luật `D698` bị 4/4 dò xoá-nhóm bỏ lọt (SỐNG), trong khi toàn bộ T-B + T-C (196 dò) cho hạng GIỐNG HỆT ứng viên (nên A1/A2 không phân biệt được hai bản) | `a1-khong-do-vi-tri-thanh-vien` (P2, lượt 1) | thêm một dò xoá-cả-nhóm cho MỖI nhóm Unicode chung (≈30, dẫn xuất từ `unicodedata`) trên `bk`; ứng viên đúng chữ giết 18/18 nhóm đã thử | 18 dò `x_cat_*` trên ứng viên 18/18 GIẾT; trên bản danh sách 14 GIẾT + 4 SỐNG |
| `phu-luc-c-dem-209-lech-221` | P3 | 1: tiêu đề Phụ lục C "(209 dò)" trong khi tập có 221 | — | sửa số, giải thích 209 + 12 | `python3 do_dot_bien_r2.py … liet_ke ¦ wc -w` = 221 |
| `s1-8-8-nhan-tag-sai` | P3 | 1: "120 Cf (TAG)" — số 120 đúng, nhãn sai: 97 TAG + 23 Cf khác | — | ghi 97 + 23 và dải điểm mã | đếm bằng `unicodedata` trên 3.11.15 |
| `tran-vong-so-10-hai-cho` | P3 | 1: §0 hàng 1 khai "Con số chỉ được chép đúng một chỗ (`tran_cu`)"; đo được hai: dòng 31 `tran_cu: 10` và dòng 42 (trích tiền lệ "ADR-0048 = 10") | `tran-cu-adr-0043-da-bi-thay` (P2, lượt 1) | diễn đạt lại câu trích bằng lời, bỏ chữ số thứ hai | script đếm số 10 đứng riêng (ranh giới từ) gần vòng/trần/ADR-0048 ⇒ 2 dòng |
| `s6-chep-thieu-quy-tac-dung` | P3 | 4: S6 "chép đúng" §12 nhưng thiếu (i) nhiều finding cùng lớp chỉ tính một lần (ii) U rỗng ⇒ `N/A`, không ghép hai tỷ lệ thấp qua `N/A` (iii) lớp mới/lớp tái mở/phần chưa đo báo riêng, không vào tử số (iv) mốc "báo chủ kho TRƯỚC khi soạn revision" không kiểm được: câu kế chỉ viện comment Q10, mà Q10 đến SAU khi r2 đã soạn | `tran-cu-adr-0043-da-bi-thay` (P2, lượt 1) | chép đủ ba mệnh đề, hoặc thay bản chép bằng con trỏ tới §12 (CLAUDE.md: "CON TRỎ, không phải bản sao"); nói rõ Q10 chỉ ghi nhận, không thay việc báo trước | so S6 với `docs/PROTOCOL_DA_PHIEN.md` dòng 1043–1056 |
| `head-moi-vi-tri-moi-thanh-vien-qua-loi` | P3 | 3: `objective` khai "mọi vị trí và mọi thành viên"; riêng `head` chỉ ba neo + R698/N698: xoá U+2063 ở đúng chỉ số 17, xoá Cf-khác chỉ ở giữa, xoá `Sm` chỉ ở giữa — SỐNG 3/3 | `a1-khong-do-vi-tri-thanh-vien` (P2, lượt 1) | thu hẹp lời khai (nêu rõ tổ hợp không đo) hoặc thêm ô | 3 dò `x_head_*` SỐNG; 3 dò đối chứng cùng họ (lead-only, trail-only, NFKC chữ hex fullwidth) GIẾT |
| `a5-canh-khong-kiem-bang-do` | P3 | 1: A5 chỉ so TÊN 43 mục; không đòi bộ (mỏ neo, phép thay) của mục bằng từng byte bộ cùng tên dò trong Phụ lục A/C | `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3, lượt 1) | thêm (vi): so bộ (tìm, thay) sau khi nạp mô-đun và hai phụ lục | một mục canh cùng tên nhưng phép thay yếu hơn vẫn ra 459 `ok` (suy ra từ chữ A5; KHÔNG dựng phản chứng chạy được) |
| `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` | P3 | 3: (a) "Bậc hai (A1-ii)" trùng số hiệu với mục (ii) của ĐẠT KHI (b) nhóm `cf` `tab` `cc` `zs` `dau` `nfkc` "handoff ghi rõ định nghĩa" ⇒ tự khai; đo trên ứng viên độc lập, kết quả PHỤ THUỘC định nghĩa: 5/7 nhóm miền `D698` khớp bảng §1.8.7, 2/7 lệch chỉ vì định nghĩa (`nfkc` +2 canh Zs, `cc` +5 canh TAB) (c) đặc tả không đính công cụ gỡ nhóm, mà §11.1 điểm 8 nói hằng gỡ nhóm bị bớt khỏi bản giao | `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3, lượt 1) | đổi số hiệu; CHỐT định nghĩa nhóm trong đặc tả (phân hoạch hay giao; `cc` có gồm TAB không; `nfkc` có gồm Zs không); nói rõ đo trên bản riêng; coi bảng đo thiếu là lý do đỏ | bậc hai TÁI HIỆN được trên ứng viên của tôi (13 cây liên kết cứng, mỗi cây chỉ khác một hàm lọc ≈ +9–11 dòng), xem BẢNG SĂN hàng 13. Giới hạn: không đo nhóm `ra` `exc` (A2, A8) |
| `doc-bang-205-vs-211` | P3 | 3: "Đọc bảng" nêu nền 205, IMP-MIN 184, IMP-GEN 138 dò sống, bảng ngay trên ghi tổng 211/190/144 (khác 6 dò hàng Z) | — | ghi "ngoài hai hàng Z" ở cả ba chỗ | 211 − 6 = 205; 190 − 6 = 184; 144 − 6 = 138 |
| `s11-1-thieu-cach-doc-q4-q9-q13` | P3 | 3: §11.1 khai "Ngoài tám điểm trên, không còn câu hỏi mở nào" nhưng còn ba cách đọc của r2 chưa liệt kê: Q4 "quét trọn miền" → trục + tích biên (cách đọc này có hậu quả đo được: hai biến thể F50 "hằng giữa × tọa độ khác" SỐNG 2/2); Q9 "các context bắt buộc" → thêm (b) và (d) (`thu-hoi` chưa là required check); Q13 "không chặn r1" → "không chặn packet" | — | liệt kê ba điểm (9)–(11) vào §11.1 | so `readback-5914438647.json` với §11 |
| `a4-d-khong-co-phep-do-may` | P3 | 1: A4-d "không chạm thân sáu hàm" chỉ đo bằng mắt (khác A4-e có Phụ lục E) | `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3, lượt 1) | giao khoảng dòng hunk `git diff -U0` với khoảng dòng `ast` của sáu hàm trên nền | script ≈10 dòng; ứng viên của tôi: giao rỗng (đo bằng tay) |
| `thu-hoi-do-khong-co-diem-dung` | P3 | 2: (d) `thu-hoi` "vẫn bắt buộc" nhưng `SO_THU_HOI_KICH_HOAT = False`, workflow tự ghi "chưa là required check"; S7 chỉ có điểm dừng cho `gate-registry` đỏ; lượt PR #696 từng có `thu-hoi` `CHAN [12]` (`trich-log.txt` dòng 765–767) | `nghia-vu-land-thieu-dinh-nghia-tac-nghiep` (P3, lượt 1) | thêm điểm dừng "`thu-hoi` đỏ ⇒ DỪNG, hỏi chủ kho" và nêu vì sao nó vẫn là điều kiện | `grep -n SO_THU_HOI_KICH_HOAT ops/lease_publish.py` ⇒ dòng 1093 `False` |

## BẢNG SĂN

Mỗi hàng là MỘT HƯỚNG theo mẫu PROMPT (giả thuyết → lệnh → output → kết luận) viết gọn trong một ô; cột kết luận dùng đúng ba nhãn LỖI · KHÔNG PHẢI LỖI · KHÔNG ĐO ĐƯỢC. Hướng nào dẫn tới lớp P2/P3 có khối đầy đủ ("HƯỚNG 2b / 8a / 8b / 8c / 9") trong CHI TIẾT TỪNG LỚP. 14 hướng: 7 gợi ý của PROMPT (hàng 1–7) cộng 7 hướng tự thêm (hàng 8–14).

| # | hướng | giả thuyết → lệnh → output (rút gọn) | kết luận |
|---|---|---|---|
| 1 | Tái hiện Phụ lục A/B/C/D/E | chạy lại cả năm tập lệnh nhúng trên bản sao nền `fc852ff`, Python 3.12.3. Băm năm khối mã khớp 5/5; Phụ lục B đầu ra `42ca657c…741d` trùng từng byte (cả 3.11.15 lẫn 3.12.3); Phụ lục E `{"tong":9,"truoc_anh":[2256,2262],"trong_cua_so":7,"sau_moc":[]}`; Phụ lục A: **24 SỐNG + 6 đối chứng bị giết** (5 `giet_that` 1/56 + `c49_ra_abspath` bán kính 2); Phụ lục C: 221 dò, nền SỐNG 211 (149/40/11/5/6), 10 đối chứng; `so_neo`=1 ở 251/251 | KHÔNG PHẢI LỖI |
| 2 | Răng của A* (bản SAI-nhưng-thoả-chữ) | dựng ứng viên `IMP-ME` đúng chữ r2 (+150/−4) rồi 6 biến thể làm sai MỘT chỗ: `V-BMP` (D698 chỉ mặt phẳng cơ bản), `V-INS` (chỉ chèn, không thay), `V-NORA` (bỏ `ra` khỏi phép quét), `V-LIST` (danh sách nhóm thay cho luật), `V-EXC`/`V-HEAD` (bản ĐÚNG hơn, để chứng minh phương án). `V-BMP`: 6/6 dò ngoài-BMP SỐNG (`m_cf_tag_*`, `m_nfkc_ngoai_bmp_*`) còn 2 đối chứng GIẾT; `V-INS`: `m_nfkc_fwonly_bk` SỐNG; `V-NORA`: `m_cf_tag_ra`, `q_cf_mid_ra`, `s_ra_cf` SỐNG; `V-LIST`: toàn bộ T-B + T-C (196 dò): hạng GIỐNG HỆT ứng viên (193 GIẾT · 2 SỐNG tương đương · 1 KHÁC đối chứng) — bản danh sách nhóm vẫn qua tập đóng; 18 dò nhóm mới: 14 GIẾT + 4 SỐNG (Mc, Me, Pf, Pi) | **A1/A2 CÓ RĂNG** với ba kiểu sai đầu; răng yếu đúng chỗ nhóm không có dò riêng (lớp `a1-tap-dong-thieu-do-theo-nhom-unicode`); M5/M2 "thoả chữ" nhưng lọt (lớp `m5-…`, `ra-ha-nguon-…`) |
| 3 | Tín dụng giả | đọc `_chay_1_ca` (:2292–2331): `giet_that` CHỈ khi `TinHieuChotCa` mang đúng tên ca (`bang()`); `LoiDungCa`/ngoại lệ trần/chốt ca khác ⇒ `tin_dung_gia`. Trên ứng viên: 221 dò ⇒ 0 `tin_dung_gia`, 0 `LOI_DUNG`; dòng KHÁC duy nhất là `s_ra_realpath` (bán kính 2, đối chứng, đúng như nền). Chốt tín hiệu của 43 canh: mỗi canh `giet_that` đúng ca đích và thông điệp của `TinHieuChotCa` nằm đúng chốt định chết (26 bởi phép quét D698×vị trí, 8 bởi lưới `_doc_che_do`, 9 bởi lưới `main` nối; `evidence/canh_msg.txt`). A5-lite (`do_reg.py` = `_do_ban_kinh` + `_ket_luan_ban_kinh`, bán kính 1/56): 90/90 `giet_that` đúng ca đích (43 canh + 47 đột biến cũ nhắm `t53`/`t54`), 0 KHÁC, 0 SỐNG, 0 LOI_DUNG. Quan sát có sẵn từ lượt 1: `_in_tu_kiem_che_do` nuốt mọi ngoại lệ của `_van_tay` thành `NEM:<kiểu>` ⇒ một dò chỉ chết vì NameError trong `_van_tay` sẽ ra `giet_that`; đặc tả chặn bằng A1(i) "dò phải SỐNG trên nền" và 221 dò đều viết an toàn | KHÔNG PHẢI LỖI (bẫy có sẵn, chưa phát nổ) |
| 4 | Trung thành quyết định chủ kho | so 11/11 nhãn "chọn/không chọn" với `readback-5914438647.json`: có trong comment VÀ trong §11; sha256 thân comment `4a2dba07…684d0`, 0 dấu chéo ngược. Q1/Q2/Q3/Q5/Q6/Q7/Q8/Q10/Q11/Q12/Q14 khớp chữ. Ba cách đọc rộng/chặt hơn chữ: Q4 "miền"→"trục + tích biên", Q9 thêm (b)+(d), Q13 "r1"→"packet" — r2 chỉ liệt kê tám điểm | LỖI P3: `s11-1-thieu-cach-doc-q4-q9-q13`; KHÔNG có điểm nào TRÁI chữ chủ kho (không P1) |
| 5 | Closure + hợp đồng | `required_checks` so `ci.yml`@`fc852ff`: job `gate` `gate-ops` `gate-packet-loop` `gate-cong-cu` (matrix 0–7, `timeout-minutes: 30`) `gate-cong-cu-gop` `gate-registry` đúng tên; `thu-hoi` đúng `pull_request_target` 5 kiểu; `trich-log.txt` dòng 1962/2438/2440/2590 khớp; write set 1 tệp; `origin-master`=`20ec8d5`: `ops/cong_cu_test.py` blob `9edea6b1…` KHÔNG đổi, `git diff --name-only fc852ff 20ec8d5` đúng 2 tệp; ruleset LIVE/lease/ref KHÔNG ĐO ĐƯỢC | `thu-hoi` bắt buộc mà chưa kích hoạt: P3 `thu-hoi-do-khong-co-diem-dung`; còn lại KHÔNG PHẢI LỖI |
| 6 | Số liệu (số hạng, không chỉ quan hệ) | xem BẢNG ĐO: 57 hàng đo lại, 4 lệch, 3 KHÔNG ĐO ĐƯỢC | LỖI P3 ×4: `phu-luc-c-dem-209-lech-221`, `s1-8-8-nhan-tag-sai`, `doc-bang-205-vs-211`, `tran-vong-so-10-hai-cho` (hàng 11) |
| 7 | Mức assurance | `bien_nhan_v2._thieu` dòng 703/720/736: subagent ⇒ từ chối mọi mức độc lập; cùng họ ⇒ từ chối `cross_approved`. Protocol §8: `sensitive` cần `cross_approved` hoặc `human_audited`; hết quota ⇒ pause | KHÔNG PHẢI LỖI |
| 8 | Đường sống cùng lớp mà §2 bỏ sót | liệt kê THEO TẦNG DÒNG CHẢY của giá trị thay vì theo tên bộ đọc: (a) kiểu ngoại lệ `_van_tay` (b) `ra` sau `_doc_che_do` (c) cấu trúc nhiều dòng của stdout `head` (d) nhóm Unicode không có dò riêng (e) tổ hợp thành viên×vị trí của `head`. Với (a)(b)(c)(e): 40 dò mới (`evidence/extra_probes.py`) trên ứng viên: **31 SỐNG** (12 + 12 + 4 + 3) + 9 GIẾT (3 đối chứng cùng họ, 2 dò `split()` chết nhờ ô nền, 4 dò `splitlines()` chết nhờ đúng hai ô tình cờ); với (d): 18 dò `x_cat_*`, ứng viên 18/18 GIẾT, bản danh sách nhóm 14 GIẾT + 4 SỐNG | LỖI: 3 lớp P2 + 2 lớp P3 |
| 9 | Thời gian CI (Q7 "CI một lần") | đo cửa con `--tu-kiem-che-do` của ứng viên, máy rảnh (loadavg 0,4–0,9; `evidence/timing.txt`): 4,5 / 4,2 / 4,7 s (ba lần); bản không trỏ `TEP_TEST` sang tệp nhỏ: 65,5 / 63,0 s (hai lần; cùng `[673234, 122148, [], 0]`); vi đo `_van_tay()` thật: 0,498 ms/ô ⇒ 122.148 ô ≈ 60,8 s | LỖI P2 `t53-thoi-gian-khong-co-tieu-chi-do` |
| 10 | Ứng viên tự dựng + trần 300 dòng | `IMP-ME` +150/−4; ≈201 nếu ngắt 120; tệp nền có 186/8393 dòng > 120 ký tự; 416 bộ sáu trường cũ y nguyên, mỏ neo của 416 đột biến cũ không đổi số lần xuất hiện hay ngữ cảnh, 43 mỏ neo mới đúng 1 lần | KHÔNG PHẢI LỖI (ước 265–280 của đặc tả bảo thủ) |
| 11 | Trần vòng ADR-0048 "đúng một chỗ" | script đếm số 10 đứng riêng gần vòng/trần/ADR-0048 trong SPEC.md: dòng 31 (`tran_cu: 10`) + dòng 42 (trích tiền lệ) = 2; ADR-0048 dòng 117: "Mọi tài liệu khác TRỎ, không chép" | LỖI P3 `tran-vong-so-10-hai-cho` |
| 12 | Tiêu chí A5 và A4-d | đọc A4–A5: A5 chỉ so TÊN 43 mục (tôi KHÔNG dựng phản chứng chạy được); A4-d "không chạm thân sáu hàm" chỉ bằng mắt, trong khi A4-e có Phụ lục E | LỖI P3 `a5-canh-khong-kiem-bang-do`, `a4-d-khong-co-phep-do-may` |
| 13 | Bậc hai (A1-b2, A2, A3) tái hiện trên ứng viên độc lập | dựng cây liên kết cứng từ ứng viên, mỗi cây chỉ khác MỘT hàm: `cf` `nfkc` `tab` `zs` `cc` `dau` `ngoai` (lọc nhóm khỏi `D698` và `R698`; `ngoai` bỏ `N698` và dùng `len(_N698)` trong công thức đếm), `ra` (bỏ 12 ô cấu trúc M2), `bq` `tich` `hong` `hong_tich` `tk` `tk_tich` (bớt một phần `_luoi_luc_luong`); chạy 32 canh T-B/T-C (hoặc 9 canh D, 10 canh T-C cho `ra`) bằng `do_reg.py` và so tập SỐNG lại với bảng §1.8.7. Họ miền: SỐNG lại đo/bảng — `cf` 11/11; `nfkc` 6/4 (+2: s_bk_drop_zs, s_mh_drop_zs); `tab` 5/5; `zs` 2/2; `cc` 6/1 (+5: q_tab_lead_mh, s_ra_tab, x46_tab_bk, x46_tab_head, x46_tab_mh); `dau` 1/1; `ngoai` 1/1; `ra` 1/1. Họ D: SỐNG lại đo/bảng — `bq` 3/3; `tich` 4/4; `hong` 0/0; `hong_tich` 5/5; `tk` 0/0; `tk_tich` 5/5. Nhóm `exc` (A8) KHÔNG đo | KHÔNG PHẢI LỖI về khả thi (bậc hai tái hiện được, mỗi biến thể ≈ +9–11 dòng); LỖI P3 về định nghĩa nhóm (nằm trong lớp `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`) |
| 14 | F50 ngoài T-D | thêm 6 biến thể vị từ lực lượng ở nhánh mảnh NGOÀI T-D (`x_f50_*`, đích `t54`): lỗ F50 gốc `or len(bo_qua) == 2` và `== 7`, ngưỡng `len(hong) >= 2` và `len(tien_kiem_bo_qua) >= 2`, và hai biến thể "hằng giữa × tọa độ khác" (`… and len(bo_qua) != 3`). Nền (`fc852ff`): 4 SỐNG + 2 GIẾT. Ứng viên: 4 GIẾT (cả `== 2` và `== 7`) + 2 SỐNG (hai biến thể hằng giữa) | KHÔNG PHẢI LỖI với lỗ F50 gốc (đóng cho mọi hằng `k`); hai biến thể SỐNG là hệ quả của "tích biên", đã nằm trong lớp `s11-1-thieu-cach-doc-q4-q9-q13` |

Tám điểm tự quyết của §11.1 đối chiếu CHỮ chủ kho (`readback-5914438647.json`; chủ kho chọn "Chấp nhận, trừ Q5: lặp tới 0/0/0" — không chọn "Chấp nhận, trừ Q14: cho HINT"):

| §11.1 | chữ chủ kho liên quan | r2 làm gì | vượt chữ chủ kho? |
|---|---|---|---|
| 1. mở rộng mục tiêu (`ra` thành bộ đọc thứ tư, mọi vị trí/thành viên, Zs/Cc/Mn, M5 kiểu ngoại lệ) | Q1 "Không, chỉ F49+F50"; Q3 "giữ các phần mở rộng (TAB, `>=2`, `len(CA)-1`, `hong`, `tien_kiem`)" — danh sách đóng trong ngoặc | `ra`: có trong Issue (F49-P3). Vị trí/thành viên/Zs/Cc/Mn: nới của F49 cùng bản chất. M5: kiểu ngoại lệ của F46, KHÔNG có trong danh sách Q3; r2 viện "cùng lý lẽ" với TAB | vượt CHỮ Q3 (danh sách đóng) ở M5 và ở các họ ký tự mới; KHÔNG trái Q1; đã khai và chờ Q10 ⇒ không P1 |
| 2. đổi cách làm lớp B sang miền dẫn xuất | không có chữ; protocol §12 đòi xem lại cách làm khi lớp quá ba lượt | đổi ở tiêu chí | không |
| 3. M3 thêm tích biên | Q4 "quét trọn miền `0…len(CA)`" | giữ trục, THÊM 48 kịch bản | không (thêm, không bớt); cách đọc "miền"→"trục" xem `s11-1-…` |
| 4. 43 canh (tổng 459) | Q12 "≤ 3 tệp và ≤ 300 dòng thêm"; Q7 "CI một lần" | +43 hàng; ứng viên của tôi +150 dòng | không trái chữ; rủi ro thời gian CI xem `t53-thoi-gian-…` |
| 5. hai bộ đọc ngoài lớp B → nợ `gom-dau-manh-chuan-hoa-wp698`; gộp `t_cf`/`t_tab` vào nợ Q2 | Q2 "fullwidth trong `_so_tien_trinh_ban_kinh` ghi thành nợ" | thêm nợ mới + nới nghĩa nợ Q2 sang Cf/TAB | không (nợ là hướng an toàn) nhưng nới nghĩa nợ đã chấp nhận ⇒ cần Q10 |
| 6. Q9 không miễn (d) | Q9 "coi các context bắt buộc xanh là đủ" | đòi thêm (b) tám mảnh và (d) `thu-hoi` | CHẶT HƠN chữ (không nới): `thu-hoi` chưa là required check ⇒ lớp `thu-hoi-do-khong-co-diem-dung` |
| 7. chủ thể `land_obligations` 8 = người chủ kho chỉ định | Q13 "đưa hồ sơ lượt 22 vào một nhánh `ops/**`; không chặn r1" | thêm chủ thể; "không chặn land" | trung tính; "r1"→"packet" xem `s11-1-…` |
| 8. ước kích thước 265–280 | Q12 ≤ 300 | ước bảo thủ | không (đo: +150) |

Kết luận hướng 4: KHÔNG có điểm nào TRÁI quyết định chủ kho (không P1); điểm 1 vượt chữ Q3 và điểm 6 chặt hơn Q9 — cả hai đã khai, chờ Q10.

## BẢNG ĐO

57 hàng; lệch 4 (đã vào BẢNG LỚP: `s1-8-8-nhan-tag-sai`, `phu-luc-c-dem-209-lech-221`, `tran-vong-so-10-hai-cho`, `doc-bang-205-vs-211`); KHÔNG ĐO ĐƯỢC 3. Mọi hàng đo lại được từ `evidence/static_checks.txt` hoặc từ các `evidence/*.jsonl`.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| sha256 SPEC.md (đối tượng review) | `f69bb398…2c0a` (PROMPT, header §0) | `sha256sum SPEC.md` = `f69bb398441168830443d4e095be18247fc4029c930fce8793cfb6574a652c0a` | có |
| HEAD `cay-kho` | `c54b502…` | `git rev-parse HEAD` = `c54b502bff2aaf3e9a40f8b0b37a657fa09174c1`; `SPEC.md` == `ops/specs/ci-g5-cong-cu-va-tiep-r2.md` (cmp SAME) | có |
| năm khối mã Phụ lục A–E khớp băm khai | `3d53b90d…` `6707002f…` `c6a4db8b…` `c1bdf8d2…` `b0772b01…` | tách khối python + một xuống dòng, `sha256` ⇒ 5/5 KHỚP (`static_checks.txt` §2) | có |
| blob `ops/cong_cu_test.py` ở `423b4ba`/`fc852ff`/`20ec8d5` | `9edea6b1…` (trùng nền) | `git rev-parse <rev>:ops/cong_cu_test.py` = `9edea6b1629b46f27758b2073e74210dc73495b7` cả ba | có |
| `git diff --quiet fc852ff 20ec8d5 -- ops/cong_cu_test.py` | rc=0 (nền không dời) | rc=0; `origin-master` = `20ec8d5d0e86cb7dc01f202c7596407a957e5961` KHÔNG đổi tệp write set | có |
| `git diff --name-only fc852ff 20ec8d5` | đúng 2 tệp (`pr684-wp677-land-evidence.yaml`, `lease_publish_test.py`) | đúng 2 tệp đó | có |
| `git rev-list --count fc852ff..20ec8d5` | 22 | 22 | có |
| `--full-history` hai merge `7c106a5`/`8e630c0` (Q11) | cha nhánh blob `a2010821…` → `9edea6b1…`, không đổi so cha master | `7c106a5f`: cha `e8c2388e`=`a20108212906`, cha `fc852fff`=`9edea6b1629b`; `8e630c0a`: cha `4dc226bc`=`a20108212906`, cha `423b4ba1`=`9edea6b1629b` | có |
| `20ec8d5` commit lúc `2026-10-01T00:55:21Z` | như trái | `2026-10-01T07:55:21+07:00` = 00:55:21Z | có |
| 66 tệp khác nhau `423b4ba`↔`fc852ff` | 66 (23/3/39/1) | 66; `ops/land` 23 · `ops/leases` 3 · `ops/reviews` 39 · `ops/specs` 1 | có |
| 56 ca · 416 đột biến · `t2` bỏ qua | 56 · 416 · `t2` (thiếu jsonschema) | 56 · 416 · `{'t2_canary_thieu_shellcheck_phai_SUY_GIAM': 'bo_qua'}` | có |
| gate nền A4-a (`CONG_CU_TEST_BAN_KINH=manh`) | `56/56 đạt…`, 416, rc=0, 175 s (có jsonschema) | `55/55 đạt; tổng=56, bỏ qua=1`, `đột biến=416`, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0, 181 s (không jsonschema) | có (khác ở t2 vì môi trường) |
| `t52`/`t53`/`t54` nền, Python 3.12.3 | 4,38 / 0,47 / 1,89 s | máy rảnh, 3 lần, in-process: `t52` 4,33–6,97 s (nhiễu) · `t53` 0,40–0,49 s · `t54` 1,85–2,05 s (`evidence/case_clock.txt`) | cùng bậc |
| `t53`/`t54` ứng viên so nền | +4,06 s / +0,55 s (IMP-R2G) | ứng viên của tôi (máy rảnh, 3 lần): `t53` 4,37–4,66 s (≈ +4,1 s) · `t54` 2,54–2,84 s (≈ +0,75 s) | cùng bậc |
| lưới `_luoi_che_do` / `_luoi_git` | 200 / 57 | 200 / 57 | có |
| số kịch bản cửa `--tu-kiem-main` | 219 | 224 khoá `KQ` − 5 khoá phi kịch bản (`mong_du` `mong_manh` `ten_ca` `so` `so1`) = 219 | có |
| dòng khớp `os.environ`/`env.get`/`getenv`; hai chỗ đọc thật | 61; `_doc_che_do` :7468 và `_so_tien_trinh_ban_kinh` :7092 | 61; :7468 và :7092 | có |
| chỗ ghi `DOT_BIEN` (Phụ lục E) | 9 = 2 / 7 / 0 | `{'tong':9,'truoc_anh':[2256,2262],'trong_cua_so':7,'sau_moc':[]}` | có |
| số dòng: `_TEN_NANG_LUC` :7456 · `_TRUOC_NANG_LUC` :7422 · `_doc_che_do` :7461–7487 · `_van_tay` :7495–7505 · `_luoi_che_do` :8040 · `_mong_che_do` :8052 · `_luoi_git` :8069 · `_mong_git` :8080 · `_in_tu_kiem_che_do` :8093 · nhánh mảnh :8227–8248 · `t54` :6884 · `_in_tu_kiem_main` :7905 · :2256/:2262 · :7094 · :2318 · :2292 | như trái | `grep -n`/`sed -n` khớp từng dòng (:2292 là `def _chay_1_ca`, :2318 là `return "giet_that"`) | có |
| ký tự nguồn nền: Cf / U+FF01…FF5E / NFKC khác chính nó | 0 / 0 / {U+2026} | 0 / 0 / ['0x2026'] | có |
| kích thước D698, 3.11.15 (Unicode 14.0.0) | 19.588 (BMP 10.982, ngoài 8.606, Cf 163, NFKC≠ 4.866) | 19588 / 10982 / 8606 / 163 / 4866 | có |
| kích thước D698, 3.12.3 (Unicode 15.0.0) | 19.798 (10.984 / 8.814 / 170 / 4.928) | 19798 / 10984 / 8814 / 170 / 4928 | có |
| S1, S2 trên 3.11.15 | 666.094 ; 120.888 | 666094 ; 120888 | có |
| S1, S2 trên 3.12.3 | 673.234 ; 122.148 | 673234 ; 122148 | có |
| `Lo` có NFKC khác chính nó (3.11.15) | 2.159 | 2159 (đầu tiên U+00AA) | có |
| U+0378 là `Cn` ở Unicode 14.0.0 và 15.0.0 | `Cn` | `Cn` ở 3.11.15, 3.12.3 và 3.13.12 | có |
| trong 8.606 điểm mã ngoài BMP của D698: Cf / Mn / Ll / Lu / So | 120 Cf (TAG), 886 Mn, 782 Ll, 704 Lu, 3.874 So | 120 / 886 / 782 / 704 / 3874 — nhưng trong 120 Cf chỉ 97 là TAG (U+E0001, U+E0020…E007F), 23 Cf khác | **KHÔNG** (nhãn) |
| vét cạn hai dò tương đương | `No`×`bk` = 0; `khác-BMP`×`mh` = 0; các cặp còn lại 4–137 | `No`×`bk`=0, `khác-BMP`×`mh`=0 (3.11.15 và 3.12.3); các cặp còn lại 4–137 (4 … 137) | có |
| kích thước tập đóng (Phụ lục C) | 221 (header, §2, §6) / "209 dò" (tiêu đề Phụ lục C) | `liet_ke` ⇒ 221 | **KHÔNG** (tiêu đề Phụ lục C) |
| chia tập T-B/T-C/T-D/T-E/ngoài | 155 / 41 / 12 / 7 / 6 | 155 / 41 / 12 / 7 / 6 (bằng hàm `tap` của Phụ lục D) | có |
| 53 dò của reviewer lượt 1 + 168 dò mới | 53 + 168 | 47 (R47) + 4 (R-exc) + 2 (R-zs) = 53; 221 − 53 = 168 | có |
| 43 canh = 16 + 27; A1 9+13, A2 2+8, A3 5+4, A8 2 | như trái | tính lại từ bảng §5: 9+2+5 = 16 ; 3+3+2+3+1+3+1+1+1+3+2+4 = 27 ; 22 + 10 + 9 + 2 = 43; cả 43 tên có trong Phụ lục A/C | có |
| Phụ lục C trên NỀN (Python 3.12.3) | SỐNG T-B 149, T-C 40, T-D 11, T-E 5, ngoài 6; 10 đối chứng | 149 / 40 / 11 / 5 / 6; đối chứng 6+1+1+2 = 10 (T-C `s_ra_realpath` KHÁC bán kính 2) | có |
| Phụ lục C trên ỨNG VIÊN đúng chữ r2 (3.12.3) | chỉ 2 dò tương đương SỐNG; `s_ra_realpath` KHÁC | T-B 153 GIẾT + 2 SỐNG; T-C 40 GIẾT + 1 KHÁC; T-D 12/12; T-E 7/7; `so_neo`=1 ×221; 0 `tin_dung_gia` | có |
| Phụ lục A trên nền | 24 SỐNG + 6 đối chứng bị giết | 24 SỐNG + 6 (5 `giet_that` 1/56 + `c49_ra_abspath` bán kính 2) | có |
| Phụ lục A trên ứng viên: 16 canh r1 | GIẾT đúng ca đích | 16/16 GIẾT; 8 dò F48 vẫn SỐNG (ngoài phạm vi, nợ `registry-nang-luc-ngoai-cua-so`) | có |
| Phụ lục B đầu ra | sha256 `42ca657c…741d` | `42ca657c282ec38b87170a3b1b98be32b1affd68169bde375540e5d7da1d741d` trên 3.11.15 và 3.12.3 | có |
| `ci_dang_ky_test.py` (không `--chay`) | 1025/1025, TỔNG: ĐẠT, delta 0 | 1025/1025 `TỔNG: ĐẠT` rc=0 ở nền và ứng viên, đầu ra GIỐNG HỆT (`diff` rỗng) | có |
| ruff F nền | 1 lỗi F841 ở :2606 (0.15.8 và 0.15.15) | 1 lỗi `F841` ở :2606 (0.15.8); ứng viên 1 lỗi ở :2659, cùng (mã, thông điệp); 0.15.15 KHÔNG ĐO ĐƯỢC | có (phiên bản khác) |
| ước kích thước bản giao | IMP-R2G +191/−5; ước 265–280 (biên mỏng 20–35 dòng) | ứng viên của tôi +150/−4; ngắt mọi dòng ở 120 ký tự ≈ 201; tệp nền 186/8393 dòng > 120 | khác — đặc tả bảo thủ, KHÔNG phải lỗi |
| thân comment `5914438647` | sha256 `4a2dba07…684d0`, 0 dấu chéo ngược | cùng sha256, `count(chr(92))` = 0 | có |
| 11 nhãn chủ kho chọn/không chọn | nguyên văn | 11/11 có trong comment VÀ trong §11 | có |
| `grep -c nang_tran` ở `ops/lease_publish.py` và `.claude/dev/packet_loop.py` | 0 và 0 | 0 và 0 | có |
| ADR-0048: Accepted 2026-09-12, thay đúng con số trục VÒNG của ADR-0043 | như trái | ADR-0048 dòng 3–8, 117 | có |
| con số trần vòng "chỉ được chép đúng một chỗ" | 1 (`tran_cu`) | 2 (dòng 31 `tran_cu: 10`, dòng 42 trích tiền lệ) | **KHÔNG** |
| protocol §12 dòng 1047, 1054–1055 | như trái | khớp; nhưng S6 bỏ 3 mệnh đề của dòng 1043–1052 | có (nhưng S6 thiếu, lớp `s6-…`) |
| `TIEN_TO_CHUNG` :730 khớp `ops/cong_cu_test.py` | :730 | :730 `("ops/cai_", "ops/cong_cu")` | có |
| `SO_THU_HOI_KICH_HOAT` | (không khai) | `False` (`ops/lease_publish.py:1093`); workflow ghi "chưa là required check" | đo thêm |
| `setpriv --reuid=54321` / HOME | có HOME ⇒ `/root/x`; bỏ ⇒ `~/x`; rỗng ⇒ `/x`; root bỏ ⇒ `/root/x` | cùng 4 giá trị | có |
| `UnicodeDecodeError` từ `subprocess.run(text=True)` (byte 0xFF) | `ValueError` đúng, `OSError`/`SubprocessError` sai | `UnicodeDecodeError True False` | có |
| `gate-cong-cu` `timeout-minutes` | 30 | 30 (`ci.yml` dòng 451); ghim `python-version: "3.12"` và `ruff==0.15.15` | có |
| `trich-log.txt` dòng 1962 / 2438 / 2440 / 2590 / 765–767 | như đặc tả | khớp từng dòng | có |
| ruleset `20856202`, 459 ref, lease #671, commit `1235a32`/`bd6ad5d`, thời lượng job 12,7–18,2 phút | như đặc tả | không mạng; commit không có trong mirror; `readback-jobs-…` không có | KHÔNG ĐO ĐƯỢC |
| IMP-MIN / IMP-GEN còn SỐNG: A1 T-B 133 / 101 · A2 T-C 38 / 24 · A3 T-D 8 / 8 | như trái (PHẢI ĐỎ Ở) | hai ứng viên không có trong sandbox; chỉ đo nền (149 / 40 / 11 SỐNG) và ứng viên của tôi; răng của A1/A2 đo thay bằng ba biến thể sai của tôi (V-BMP, V-INS, V-NORA) | KHÔNG ĐO ĐƯỢC |
| A5 trọn trên IMP-R2G: 8 mảnh `k/8` 57–58 đột biến, 497–521 s mỗi mảnh, `GOM MẢNH 8/8`, 459 dòng `ok` | như trái | không chạy A5 trọn; chạy A5-lite: 43/43 canh + 47 đột biến cũ nhắm `t53`/`t54` đều `giet_that` đúng ca đích, bán kính 1/56 (90/459) | KHÔNG ĐO ĐƯỢC (đo một phần 90/459) |
| bậc hai (gỡ riêng một nhóm): canh SỐNG lại, bảng §1.8.7 của r2 | IMP-R2-GO: cf 11 · nfkc 4 · tab 5 · zs 2 · cc 1 · dau 1 · ngoai 1 · ra 1 (giới hạn trong 32 canh T-B/T-C); D: bq 3 · tich 4 · hong 0 · hong,tich 1 · tk 0 · tk,tich 1 | ứng viên CỦA TÔI (không phải IMP-R2-GO), nhóm = mọi điểm mã có thuộc tính; SỐNG lại đo/bảng — họ miền: `cf` 11/11; `nfkc` 6/4 (+2: s_bk_drop_zs, s_mh_drop_zs); `tab` 5/5; `zs` 2/2; `cc` 6/1 (+5: q_tab_lead_mh, s_ra_tab, x46_tab_bk, x46_tab_head, x46_tab_mh); `dau` 1/1; `ngoai` 1/1; `ra` 1/1; họ D: `bq` 3/3; `tich` 4/4; `hong` 0/0; `hong_tich` 5/5; `tk` 0/0; `tk_tich` 5/5 | khớp 12/14 nhóm; các nhóm lệch chỉ vì định nghĩa nhóm (xem lớp `bac-hai-…`) |
| "Đọc bảng": số dò sống của nền / IMP-MIN / IMP-GEN | 205 / 184 / 138 | bảng ngay trên: 211 / 190 / 144 (chênh đúng 6 = hai hàng Z; chỉ bullet IMP-R2F ghi "ngoài hai hàng Z") | **KHÔNG** (cơ sở đếm khác nhau) |

A5-lite trên ứng viên (`evidence/a5_lite.jsonl`): 43/43 canh mới — 43 GIẾT đúng ca đích, 0 KHÁC, 0 SỐNG, 0 LOI_DUNG; 47 đột biến cũ nhắm `t53`/`t54` (mẫu mỗi ba trong 139) — 47 GIẾT đúng ca đích, 0 KHÁC, 0 SỐNG, 0 LOI_DUNG. Tiêu chí "GIẾT đúng ca đích, bán kính 1/56" của A5 đo bằng chính `_do_ban_kinh` + `_ket_luan_ban_kinh`; A5 trọn (8 mảnh + `--gop`) KHÔNG chạy.

## CHI TIẾT TỪNG LỚP

### Lớp `m5-ngoai-le-chi-ba-kieu` (P2)
HƯỚNG 8a: tập ngoại lệ `_van_tay` bắt có thật sự được đo "từ hai phía" (M5) không
  giả thuyết : M5 chọn tay ba kiểu ngoài tập bắt (`ValueError`, `UnicodeDecodeError`, `RuntimeError`) và khai "hợp đồng tập bắt CHÍNH XÁC là (OSError, SubprocessError) được đo từ hai phía". Một đột biến mở rộng tập bắt sang kiểu KHÁC ba kiểu ấy (và tổ tiên của chúng) không có ô nào ném nó ⇒ lọt.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3.12 evidence/extra_probes.py <cây ứng viên> <ra.jsonl> x_exc_typeerror x_exc_attributeerror x_exc_keyerror x_exc_lookuperror x_exc_assertionerror x_exc_importerror x_exc_eoferror x_exc_unicodeencodeerror x_exc_notimplemented x_exc_indexerror x_exc_zerodiv x_exc_memoryerror`
               (mỏ neo `EXC` = hai dòng `except (OSError, subprocess.SubprocessError):` + `head = ""`, đúng mỏ neo của Phụ lục C; phép thay `except (OSError, subprocess.SubprocessError, <Kiểu>):`; `so_neo`=1 cả 12)
  output     : 12 dòng `SONG` — `khong_qua = {'t2_c': 'bo_qua'}` (không ca nào chết), đích `t53_…` vẫn `qua`. Đối chứng cùng lượt: 7 dò `z_exc_*` của Phụ lục C GIẾT 7/7.
  kết luận   : LỖI. Đây là "danh sách CẤM không bao giờ đủ" (CLAUDE.md; chính §9 của r2 viện nó cho M1) áp lên tập ngoại lệ, và là "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba": lượt 1 chỉ `Exception`/`+ValueError`; r2 thêm `BaseException`/`+UnicodeError`/`+RuntimeError` và ba ô; mọi kiểu còn lại vẫn lọt.
  phương án  : (lời) dẫn xuất miền ô từ thuộc tính thay vì chọn tay: mọi lớp con CỤ THỂ của `Exception` trong `builtins` không thuộc họ `OSError`, dựng bằng `E.__new__(E)` (bỏ lớp đòi đối số như `ExceptionGroup`), kỳ vọng `NEM:<tên lớp>` dựng độc lập; giữ ba ô thu hẹp sẵn có. A8 thêm điều kiện "mở rộng tập bắt bằng MỘT kiểu bất kỳ của miền ⇒ GIẾT `t53_…`".
  phép kiểm  : biến thể đo `tv_exc` (+14 dòng so ứng viên; 45 lớp trên 3.12.3; `t53` nền `qua`; `_luoi_git` 57 → 102 ô): 12 dò `x_exc_*` + 7 dò `z_exc_*` ⇒ **19/19 GIẾT** đúng `t53_…` (`evidence/variants.jsonl`, trường `bien_the` = `v_exc`). Giới hạn: miền = `builtins` của 3.12.3.

### Lớp `ra-ha-nguon-main-bo-ghi-chua-co-o` (P2)
HƯỚNG 8b: giá trị `ra` còn chảy qua tầng nào sau `_doc_che_do`?
  giả thuyết : F49-P3 nêu `ra` "ở tầng `_doc_che_do`"; nhưng `ra` đi tiếp vào `main` (`k, n, ra = tham_so`, hai lời gọi `_ket_thuc_manh`) rồi vào bộ ghi (`tep = Path(ra)`). Lượt 19/20 (F42/F44, `f42_ra_strip`/`f42_ra_lower`/`f44_nen_ra_*`) đã đòi `ra` đi NGUYÊN qua `main`, nhưng chỉ chặn strip/lower; các phép của F49-P3 và của lớp B không có ô ở hai tầng ấy.
  lệnh       : `evidence/extra_probes.py <cây ứng viên> <ra.jsonl> x_main_ra_normpath x_main_ra_expanduser x_main_ra_nfkc x_main_ra_cf x_main_ra_tab x_main_ra_zs x_wr_ra_normpath x_wr_ra_expanduser x_wr_ra_nfkc x_wr_ra_cf x_wr_ra_tab x_wr_ra_zs`
               (main: mỏ neo `        k, n, ra = tham_so` — chính mỏ neo của `f42_*`, đích `t54`; bộ ghi: mỏ neo `    tep = Path(ra)` — chính mỏ neo của `f35_writer_path_trim`, đích `t52`)
  output     : 12/12 `SONG` (`khong_qua = {'t2_c': 'bo_qua'}`). Đột biến KHÔNG tương đương: `normpath('a/./b//c')` = `a/b/c`, `expanduser('~/x')` = `/root/x` — chỉ là lưới `_luoi_noi_main` (`x`, ` space `, `Mixed.TXT`, `dir/Sub Dir/Mảnh.TXT`, hai dấu cách, `d con/manh 3.txt`) và `ghi_duong` (`a/b c/manh-0.txt␠`) không có đường nào đổi dưới các phép này.
  kết luận   : LỖI (TÁI PHÁT lớp `ra-thieu-hang-chuan-hoa-lop-b`: bản vá đóng đúng tầng được chỉ, bỏ sót hai tầng cùng giá trị cùng phép).
  phương án  : (lời) thêm vào `_luoi_noi_main` các đường ra có cấu trúc của M2 (mỗi phép một đường; HOME ghim); thêm một đường tương tự vào kịch bản bộ ghi; đưa 12 dò vào tập đóng (T-C, A2) và canh tương ứng (+12 hàng ≈ +12 dòng; vẫn dưới trần 300).
  phép kiểm  : 12 dò phải GIẾT đúng `t54_…`/`t52_…`, bán kính 1/56. Giới hạn: tôi chưa dựng bản vá cho lớp này (chỉ đo SỐNG); hạ nguồn thứ ba (`--gop <thư mục>`) chưa đo.

### Lớp `head-nhieu-dong-chi-tach-lf-chua-co-o` (P2)
HƯỚNG 8c: ô MỘT ký tự có dựng được mọi đầu vào mà đột biến của `head` nhận khác nền không?
  giả thuyết : `_van_tay` làm `p.stdout.strip()`: ký tự tách ở hai đầu bị `strip()` che. Đột biến "lấy dòng cuối/đầu của stdout" (thành ngữ hay gặp khi git in thêm cảnh báo) chỉ khác nền khi stdout có ≥ 1 ký tự nhiễu + ký tự tách + mã băm; mọi ô của §5 M1 chỉ sửa MỘT ký tự.
  lệnh       : `evidence/extra_probes.py <cây> <ra.jsonl> x_head_nl_last x_head_nl_first x_head_rsplit_nl x_head_crlf_last x_head_lastline x_head_lastline_raw x_head_firstline x_head_lastnonblank x_head_split_last x_head_split_first` (mỏ neo `HEAD`, đích `t53`)
  output     : nền: 8/10 SỐNG (chỉ `split()` theo khoảng trắng chết, nhờ ô nền `hop + " " + hop`). Ứng viên: **4/4 dò tách theo LF SỐNG** (`x_head_nl_last`, `x_head_nl_first`, `x_head_rsplit_nl`, `x_head_crlf_last`); 4 dò `splitlines()` GIẾT — nhưng mỗi dò chết bởi ĐÚNG 2 ô, cả hai dùng U+000B (một đại diện Cc của R698) ở `head` 64 ký tự: chỉ số 23/24 (`lastline`, `lastline_raw`, `lastnonblank`: đuôi còn đúng 40) hoặc 40 (`firstline`: đầu còn đúng 40) — nghĩa là 64 = 40 + 24 và có VT trong R698. Bỏ một trong hai thì cả bốn SỐNG. Minh hoạ hành vi: stdout `"warning: x" + LF + <40 hex>` nền ⇒ `None`, `nl_last` ⇒ mã băm.
  kết luận   : LỖI. Miền "một ký tự × vị trí" không thể dựng đầu vào nhiều thẻ; hai trong năm giá trị tách dòng của Unicode (LF, CR) thậm chí không có ô nào.
  phương án  : (lời) ô nhiễu = chuỗi không-hex ngắn + MỖI ký tự tách dòng Unicode (LF, CR, CRLF, VT, FF, FS, GS, RS, NEL, LS, PS) + mã băm hợp lệ, cả hai thứ tự, kỳ vọng `None` từ `_mong_git`; công thức cha cộng 2 × 2 × 11 = 44 ô.
  phép kiểm  : biến thể đo `tv_head` (+5 dòng so ứng viên; `t53` nền `qua`): 4 dò LF + 4 dò `splitlines` ⇒ **8/8 GIẾT** `t53_…` (`evidence/variants.jsonl`, trường `bien_the` = `v_head`).

### Lớp `t53-thoi-gian-khong-co-tieu-chi-do` (P2)
HƯỚNG 9: làm đúng từng chữ M1 có vượt trần 30 phút của `gate-cong-cu` mà không tiêu chí nào đỏ không?
  giả thuyết : M1 đòi 120.888 (3.11) / 122.148 (3.12) ô `head` qua `_van_tay()` với `subprocess` giả. `_van_tay` băm lại toàn bộ `TEP_TEST` (600.770 byte) ở MỖI lời gọi. Đặc tả không nói điều này, không khai tiêu chí thời gian trong A1–A8, mà Q7 chỉ cho MỘT lượt CI.
  lệnh       : `python3.12 ops/cong_cu_test.py --tu-kiem-che-do` (cửa con của `t53`) trên hai bản của ứng viên, máy rảnh (loadavg 0,4–0,9, 4 lõi): (1) trỏ `g["TEP_TEST"]` sang tệp 1 byte trong phạm vi phép quét `head` (mẫu có sẵn ở khối `kq["byte"]`); (2) bỏ đúng hai dòng ấy. Vi đo: `_van_tay()` với `subprocess` giả × 3000 lần.
  output     : (1) rc=0, **4,5 / 4,2 / 4,7 s** (ba lần), `quet=[673234, 122148, [], 0]` · (2) rc=0, **65,5 / 63,0 s** (hai lần), cùng `quet` · vi đo 0,498 ms/ô × 122.148 = 60,8 s (`evidence/timing.txt`; lần đo đầu của tôi, dưới tải 3,47: 4,0 s và 58,8 s — cùng bậc). Ngoại suy theo CHÍNH hệ số của r2 (runner 59–84 s so container 29,8 s ⇒ ×2,0–2,8; mảnh 57–58 đột biến, 4 tiến trình): thêm (64,3 − 4,5) × (2,0…2,8) × 58/4 ≈ **29–40 phút** vào mảnh vốn 12,7–18,2 phút ⇒ vượt trần 30 phút (ƯỚC, không đo trên runner).
  kết luận   : LỖI (P2): bản thi công "đúng chữ" mà ngây thơ qua A1–A8 (kết quả đúng, chỉ chậm) và chỉ lộ ở lượt CI duy nhất ⇒ S10 DỪNG, hỏi chủ kho. §7 có số ước cho ứng viên tham chiếu nhưng không có chốt.
  phương án  : (lời) thêm A4-g: `t53` ≤ nền + 8 s, `t54` ≤ nền + 4 s, đo trong cùng lệnh với nền (đặc tả khai +4,06 s và +0,55 s); nêu mẫu trỏ `TEP_TEST` sang tệp tạm trong phạm vi phép quét.
  phép kiểm  : A4-g đỏ trên bản (2), xanh trên bản (1) trên cùng máy. Giới hạn: ngưỡng +8/+4 s là đề nghị của tôi (đệm 2× so khai); thời lượng trên runner thật KHÔNG ĐO ĐƯỢC.

### Lớp `a1-tap-dong-thieu-do-theo-nhom-unicode` (P3)
HƯỚNG 2b: tiêu chí A1 có phân biệt "luật CHO PHÉP `D698`" với "danh sách nhóm" không?
  giả thuyết : §9 của r2 viện "đảo danh sách CẤM thành luật CHO PHÉP" cho M1. Tập đóng chỉ có dò riêng cho Cc, Cf, Zs, Mn, Lo, Co, Cn, dấu (`m_bodau_*`) và các tập con NFKC (`m_nfkc_*`); các nhóm Mc, Me, Pf, Pi (không phần tử nào có ánh xạ NFKC) không có dò xoá-cả-nhóm, nên một phép quét dùng DANH SÁCH nhóm (Cc, Cf, Zs, Zl, Zp + NFKC khác chính nó) có thể qua A1.
  lệnh       : 18 dò `x_cat_<nhóm>_bk` = xoá mọi ký tự nhóm đó khỏi `bk` (Sm Sc Sk So Pc Pd Ps Pe Pi Pf Po Mc Me Nl Lm Lt Zl Zp), chạy trên ứng viên (D698 đúng luật) và trên biến thể `tv_list` (D698 = danh sách nhóm trên).
  output     : ứng viên **18/18 GIẾT**. `tv_list`: 14 GIẾT + **4 SỐNG** (`x_cat_mc_bk`, `x_cat_me_bk`, `x_cat_pf_bk`, `x_cat_pi_bk`). Trên `tv_list` chạy toàn bộ T-B + T-C của Phụ lục C (196 dò): **hạng GIỐNG HỆT ứng viên trên cả 196 dò** (193 GIẾT · 2 SỐNG là hai dò tương đương mà đặc tả đã khai · 1 KHÁC là đối chứng `s_ra_realpath`; ba dò không GIẾT: `m_nfkc_khac_bmp_mh`, `m_nfkc_no_bk`, `s_ra_realpath`) — tức bản danh sách nhóm qua trọn A1 (ii)/A2 (ii) của tập đóng.
  kết luận   : LỖI P3: tiêu chí A1/A2 như viết KHÔNG phân biệt được luật `D698` với danh sách nhóm ở bốn nhóm Mc, Me, Pf, Pi (đo trực tiếp bằng toàn bộ T-B + T-C). Mỉa mai đúng chỗ §9: lời "đảo danh sách CẤM thành luật CHO PHÉP" chỉ được tiêu chí đo tới các nhóm có dò riêng. Mức P3 vì bốn nhóm ấy không có điểm mã nào mà bộ đọc hiện tại xử lý riêng (không mutant nào của mã hiện có rơi vào đó) — rủi ro là mã TƯƠNG LAI.
  phương án  : (lời) thêm một dò xoá-cả-nhóm cho MỖI nhóm Unicode chung (≈30, dẫn xuất từ `unicodedata` thay vì chọn tay) trên `bk`.
  phép kiểm  : 18/18 dò mới GIẾT trên ứng viên đúng luật; ≥ 1 SỐNG trên bản danh sách.

### Lớp `phu-luc-c-dem-209-lech-221` (P3)
  biểu hiện  : dòng 1271 "Tập dò đóng của r2 (209 dò)" trong khi tập có 221 (đoạn đầu header, §2, §6 đều ghi 221; 209 là số của lô đo đầu).
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 do_dot_bien_r2.py <gốc> /dev/null liet_ke | wc -w` ⇒ `221`.
  phương án  : sửa số và giải thích 209 + 12 (HINT.patch nhóm đầu).

### Lớp `s1-8-8-nhan-tag-sai` (P3)
  biểu hiện  : §1.8.8 "có 120 Cf (TAG)".
  lệnh       : đếm `unicodedata.category == "Cf"` ở U+10000…U+10FFFF trên 3.11.15 ⇒ 120, trong đó U+E0001 và U+E0020…U+E007F = 97; còn lại 23: U+110BD, U+110CD, U+13430…U+13438, U+1BCA0…U+1BCA3, U+1D173…U+1D17A.
  phương án  : ghi "97 TAG + 23 Cf khác".

### Lớp `tran-vong-so-10-hai-cho` (P3)
  biểu hiện  : §0 hàng 1 "Con số chỉ được chép đúng một chỗ (`tran_cu`)"; ADR-0048 dòng 117 "Mọi tài liệu khác TRỎ, không chép". Đo: dòng 31 (`tran_cu: 10`) và dòng 42 (trích nguyên văn tiền lệ `…ADR-0048 = 10 cho spec dong bang…`).
  lệnh       : đếm số 10 đứng riêng trong ngữ cảnh vòng/trần/ADR-0048/`tran_cu` ⇒ 2 dòng (`evidence/static_checks.txt` §7).
  phương án  : diễn đạt lại câu trích bằng lời (không chép chữ số thứ hai).

### Lớp `s6-chep-thieu-quy-tac-dung` (P3)
  biểu hiện  : S6 nói "Hai quy tắc dừng của protocol §12 vẫn áp, chép đúng" nhưng thiếu: (i) "nhiều finding cùng lớp chỉ tính một lần"; (ii) "U rỗng thì tỷ lệ không xác định (`N/A`), không phải 0% hay 100%; không ghép hai tỷ lệ thấp qua một chuyển tiếp N/A"; (iii) "Báo riêng các lớp mới tại r+1, lớp tái mở và phần chưa đo; không vào tử số F" (protocol dòng 1043–1052). Thêm (iv): S6 đòi báo chủ kho "TRƯỚC khi soạn revision", còn câu kế chỉ viện comment Q10 (SAU khi r2 đã soạn) "là chỗ chủ kho ghi rằng đã thấy bảng ấy"; đặc tả không có bằng chứng việc báo trước — không kiểm được chứ KHÔNG phải tự mâu thuẫn, nên không xếp P1. Câu "chép đúng" rộng hơn phép đo (ba mệnh đề bị bỏ) nhưng S6 vẫn trỏ protocol là nguồn nên P3.
  phương án  : chép đủ ba mệnh đề, hoặc thay bản chép bằng con trỏ tới §12; nói rõ Q10 chỉ GHI NHẬN, không thay việc báo trước.

### Lớp `head-moi-vi-tri-moi-thanh-vien-qua-loi` (P3)
  biểu hiện  : `objective` khai kiểm "mọi vị trí và mọi thành viên của từng họ ký tự"; §5 M1 cho `head` chỉ ba vị trí neo cho D698 + R698/N698 ở mọi vị trí. Dò ngoài: `x_head_cf2063_at17` (xoá U+2063 ở đúng chỉ số 17), `x_head_cfk_mid_only` (xoá Cf ngoài R698 chỉ ở giữa), `x_head_sm_mid_only` (xoá `Sm` chỉ ở giữa) ⇒ SỐNG 3/3; đối chứng `x_head_cfk_lead_only`, `x_head_cfk_trail_only`, `x_head_nfkc_fwletters` GIẾT 3/3.
  phương án  : thu hẹp lời khai (nêu rõ tổ hợp thành viên ngoài R698 × vị trí ngoài neo KHÔNG đo) — các đột biến này không tự nhiên.
  hạng       : theo luật hạng, "lời khai rộng hơn phép đo" là P2; tôi xếp P3 vì THÂN M1 nêu đúng miền của `head` (ba neo + R698/N698 mọi vị trí), chỉ câu tóm tắt ở `objective` rộng hơn, và một executor làm đúng thân M1 không bị đánh lừa. Điều phối viên có thể nâng lên P2 mà không đổi phương án.

### Lớp `a5-canh-khong-kiem-bang-do` (P3)
  biểu hiện  : A5 "tập tên thêm đúng bằng cột tên mục của bảng nối" — đối chiếu TÊN do chính executor viết ở hai phía; không đòi bộ (mỏ neo, phép thay) của mục bằng từng byte bộ cùng tên dò trong Phụ lục A/C. Một mục canh yếu hơn dò vẫn ra 459 `ok`.
  phép kiểm  : suy từ chữ A5; KHÔNG dựng phản chứng chạy được.
  phương án  : thêm (vi): so (tìm, thay) của 43 mục với bảng `P` của hai phụ lục sau khi nạp mô-đun.

### Lớp `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (P3)
  biểu hiện  : (a) "Bậc hai (A1-ii)" vs mục "(ii)" của ĐẠT KHI (hai nghĩa); (b) nhóm `cf` `tab` `cc` `zs` `dau` `nfkc` "có thể giao nhau … handoff ghi rõ định nghĩa nhóm đã dùng" ⇒ tự khai, không có chốt; (c) §11.1 điểm 8 nói hằng gỡ nhóm (`_GO698`, bảng lọc nhóm, `_n698`) bị BỚT khỏi bản giao, nhưng đặc tả không đính công cụ gỡ nhóm (khác Phụ lục E cho A4-e) và `IMP-R2-GO` không nằm trong đặc tả.
  đo         : dựng 13 cây liên kết cứng từ ứng viên, mỗi cây chỉ khác một hàm (`_ING698`: lọc nhóm khỏi `D698` và `R698`; hoặc bớt một phần của `_luoi_luc_luong`), chạy 32 canh T-B/T-C và 9 canh D bằng `do_reg.py` (xem BẢNG SĂN hàng 13). Nhóm của tôi = MỌI điểm mã có thuộc tính (đúng chữ "đặt theo thuộc tính" của A1): `cf` = Cf; `nfkc` = NFKC khác chính nó; `tab` = U+0009; `zs` = Zs, Zl, Zp; `cc` = Cc; `dau` = Mn hoặc NFD khác chính nó; `ngoai` = `N698`.
               Kết quả: `cf` 11/11, `tab` 5/5, `zs` 2/2, `dau` 1/1, `ngoai` 1/1 khớp bảng; **`nfkc` SỐNG lại 6 thay vì 4** (thêm `s_bk_drop_zs`, `s_mh_drop_zs`: U+00A0, U+2003, U+3000 thuộc cả Zs lẫn NFKC); **`cc` SỐNG lại 6 thay vì 1** (thêm năm canh TAB: U+0009 thuộc Cc). Cùng bảng, hai định nghĩa nhóm hợp lệ theo chữ đặc tả cho hai tập khác nhau. Nhóm `ra` (bỏ 12 ô M2): chỉ `s_ra_expandvars` SỐNG lại (1/1, khớp), 9 canh `ra` còn lại vẫn GIẾT. Họ D (A3): `bq` 3, `tich` 4, `hong` 0, `tk` 0 khớp; `hong,tich` và `tk,tich` cho 5 = 4 (của `tich`) + 1 — bảng §1.8.7 ghi "1", đúng nếu hiểu là phần THÊM so với `tich` (đặc tả không nói rõ nghĩa của hàng ấy). Tổng: 12/14 nhóm khớp, 2/14 lệch vì định nghĩa nhóm. Nhóm `exc` (A8) không đo.
               Lần đo đầu của `ngoai` bị TÔI loại: ứng viên của tôi chép cứng `+ 3` (số phần tử `N698`) vào công thức đếm của cha, nên cây không đột biến đã đỏ ở `t53` và mọi canh bị giết giả (0 SỐNG); sau khi thay bằng `len(_N698)` và kiểm `t53` xanh trên cây chưa đột biến, đo lại cho `m_co_bk` SỐNG đúng như bảng. Mọi cây biến thể đều được kiểm `t53`/`t54` XANH khi chưa đột biến trước khi chạy canh (`sanity_case.py`).
  kết luận   : LỖI P3: tiêu chí khả thi (tái hiện được) nhưng không kiểm được bằng chữ đặc tả, vì định nghĩa nhóm thuộc về handoff; không cổng nào ép hai bên cùng định nghĩa.
  phương án  : đổi số hiệu; CHỐT định nghĩa nhóm trong đặc tả (phân hoạch hay giao; `cc` có gồm TAB không; `nfkc` có gồm Zs không), đính công cụ gỡ nhóm như Phụ lục E hoặc nói thẳng nó nằm ngoài bản giao; coi bảng đo thiếu là lý do đỏ A1/A2/A3/A8.

### Lớp `doc-bang-205-vs-211` (P3)
  biểu hiện  : "Đọc bảng" nêu nền 205 / IMP-MIN 184 / IMP-GEN 138 dò sống; bảng ngay trên ghi tổng 211 / 190 / 144. Chênh đúng 6 dò hàng Z (Z1 4 + Z2 2); bullet IMP-R2F nói "ngoài hai hàng Z" nhưng ba bullet kia thì không.
  phương án  : ghi "ngoài hai hàng Z" ở cả ba chỗ.

### Lớp `s11-1-thieu-cach-doc-q4-q9-q13` (P3)
  biểu hiện  : §11.1 chốt "Ngoài tám điểm trên, không còn câu hỏi mở nào". Nhưng còn ba cách đọc: (Q4) chủ kho "quét trọn miền `0…len(CA)`" ⇒ r2 "trục `0…len(CA)` + tích biên 48" (tích đầy đủ là 6.612 kịch bản; hậu quả đo được: hai biến thể vị từ gắn một HẰNG GIỮA của `bo_qua` với một tọa độ khác — `tien_kiem_bo_qua and len(bo_qua) != 3` và `hong and len(bo_qua) != 3` — SỐNG 2/2 trên ứng viên đúng chữ r2, còn lỗ F50 gốc "đẳng thức trên `bo_qua`" đóng: `or len(bo_qua) == 2` và `== 7` nền SỐNG → ứng viên GIẾT; tích đầy đủ sẽ giết cả hai biến thể SỐNG theo cấu tạo, không dựng); (Q9) chủ kho "coi các context bắt buộc xanh là đủ" ⇒ r2 đòi thêm (b) tám mảnh và (d) `thu-hoi`, mà `thu-hoi` chưa là required check; (Q13) chủ kho "không chặn r1" ⇒ r2 "không chặn packet/land". Không cái nào TRÁI chữ chủ kho (đều an toàn hơn hoặc suy ra được), nhưng đặc tả tự nhận đã liệt kê hết.
  phương án  : thêm điểm (9)–(11) vào §11.1.

### Lớp `a4-d-khong-co-phep-do-may` (P3)
  biểu hiện  : A4-d "git diff … không chạm thân" sáu hàm — kiểm bằng mắt; A4-e có Phụ lục E, A4-d không. Lượt 1 đã nêu đúng hình dạng này ở A4-e (`tieu-chi-nghiem-thu-thieu-chinh-xac` (c)); r2 sửa đúng chỗ được chỉ.
  phương án  : giao khoảng dòng của hunk `git diff -U0` (phía nền) với `[lineno, end_lineno]` của sáu hàm do `ast` trả trên nền; giao khác rỗng ⇒ ĐỎ.

### Lớp `thu-hoi-do-khong-co-diem-dung` (P3)
  biểu hiện  : (1) `required_checks` (d) + Q9 + S7: `thu-hoi` "vẫn bắt buộc"; nhưng `ops/lease_publish.py:1093 SO_THU_HOI_KICH_HOAT = False` và workflow tự ghi "CHƯA KÍCH HOẠT … chưa là required check". (2) S7 chỉ có điểm dừng cho `gate-registry` đỏ; không có điểm dừng nào cho `thu-hoi` đỏ, dù lượt PR #696 từng có `CHAN [12]: KHÔNG_XÁC_ĐỊNH: S c16bec639efa không phải tổ tiên của H cc78b33bd04d` (`trich-log.txt` dòng 765–767).
  phương án  : thêm "`thu-hoi` đỏ ⇒ DỪNG, hỏi chủ kho" và nói vì sao nó vẫn là điều kiện.

## DRY-RUN HINT.patch (nếu có)

`HINT.patch` CHỈ sửa văn bản đặc tả (`--- ops/specs/ci-g5-cong-cu-va-tiep-r2.md`, không tiền tố `a/` `b/`); KHÔNG chứa mã `ops/cong_cu_test.py` (Q14). 16 nhóm, mỗi nhóm mở bằng `# lop: <slug>`; tập slug của HINT BẰNG tập slug của BẢNG LỚP (16).
Mọi số trong các câu chèn là số TÔI đo (Python 3.12.3, sandbox này); revision 3 phải đo lại trước khi giữ.

Lệnh (đúng như PROMPT §3, chạy trên bản sao `cp -a` của `cay-kho`):
```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay" && cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Kết quả (`evidence/hint_dryrun.txt`, 163 dòng): **rc=0**; `17` hunk `succeeded` (16 nhóm, 17 hunk; nhóm `s6-chep-thieu-quy-tac-dung` có 2 hunk), `0` lần lệch dòng (offset), `0` fuzz, `0` FAILED; không tệp `.rej`/`.orig`. Bốn dòng cuối:
```
Using Plan A...
Hunk #1 succeeded at 744.
done
rc=0
```
Kiểm thêm (ngoài lệnh PROMPT): áp THẬT tuần tự lên một bản sao tệp đặc tả (`evidence/hint_apply.txt`): rc=0, `17` hunk, tệp 1653 → 1708 dòng, không `.rej`/`.orig`. Chạy lại `patch --dry-run -N` trên bản đã áp ⇒ patch nhận ra các hunk đã áp (không áp đôi).
Kiểm hình thức: sha256 `HINT.patch` = `83b9df3323d1e2d276c1ff2d2d416a92f2213382347bb8d1cfcf0629cc95e832`; 24152 byte; 0 dấu chéo ngược; 0 CR; 0 ký tự Cf; 0 chuỗi bỏ-qua-CI; 0 tiền tố a/ b/.

## HIỆN VẬT (`cr698-r2/goi/`)

| tệp | byte | sha256 |
|---|---|---|
| `HINT.patch` | 24152 | `83b9df3323d1e2d276c1ff2d2d416a92f2213382347bb8d1cfcf0629cc95e832` |
| `evidence/a4a_nen.txt` | 1274 | `7825e6c3fcaa9946377679a4305e38ec9cf41849e8c3f5ac4b826a650a261dcb` |
| `evidence/a4a_ung_vien.txt` | 1274 | `b69084c81a1eb3e28ceeb418ef5890be2ce17177bece0ac4f882f1387b5ca0cb` |
| `evidence/a4c_ci_dang_ky_nen.txt` | 59329 | `b2b90562dd42d94c02a07b4c21f07aec9f3c2060f7406bc2be3e39e0f691890b` |
| `evidence/a4c_ci_dang_ky_ung_vien.txt` | 59329 | `b2b90562dd42d94c02a07b4c21f07aec9f3c2060f7406bc2be3e39e0f691890b` |
| `evidence/a5_lite.jsonl` | 29312 | `042341fafbacb434998aef0aa8ed11a6af1d7a66ca2f7c508a992486959bcab3` |
| `evidence/bac_hai.jsonl` | 105174 | `57acacf22776577484248fee41e22d900b53b697251151bae3f5ca6d0687b20f` |
| `evidence/bac_hai_ngoai_lan1_BI_LOAI.jsonl` | 10778 | `a5c7efed7bcc702fc5e75c3ad2a241ffd0d7009cf54b22b1b9c8a923d4373d1c` |
| `evidence/baseline_A.jsonl` | 10526 | `c8252f0d368658bfe43507c34a26b245f937161ad1c51207a5e6195581305de0` |
| `evidence/baseline_C.jsonl` | 82990 | `7df4d749868dc0fa3f64130b7a380bb4058ee382f18840cb0ce81dd55d1d3f3b` |
| `evidence/baseline_head.jsonl` | 3800 | `0f3fd9b4bb18240063d99450a5ea5706c90360fda7930bad2039f8d0db85cee0` |
| `evidence/candidate_A.jsonl` | 10046 | `fa97fcdb80528d62b79fdc5cffb5a68b6999b749f75414108deae89f2227c2f0` |
| `evidence/candidate_C.jsonl` | 76900 | `c1539e5744f6619a47523355bf7d6a357682f98da034e13151085686a4b407be` |
| `evidence/candidate_extra.jsonl` | 14944 | `18464314a3b484f46eb23757115b4ec9273d93a1904125565ab57bc9a26671a9` |
| `evidence/canh_msg.txt` | 8287 | `6c1194c3ade865bee9604369c317e0063dc7bef12fc8462e3075ead0f3d2513c` |
| `evidence/case_clock.txt` | 357 | `5f5b0ae32988ac43cdc718caf67218d5faf5b4bc1177806900c239505c43900b` |
| `evidence/caseclock.py` | 527 | `601fc2c4484f24e3b0c56563495afaeaa5945966b16a3cd4b4e1bed8a6c68f1f` |
| `evidence/do_reg.py` | 1691 | `afa7442b9286e236a92e96c8a0a1f0d96d8c76b8256b8e2c41b65dcbadf64ad9` |
| `evidence/extra_probes.py` | 23363 | `b678a50fbe9d3758f5976612ea382295f8fd6b43111d86e99315458dfde13c0e` |
| `evidence/f50_extra.jsonl` | 4218 | `461c70b3111a4fff66165db6d5fde5c271ad7a56cbdef76afccdf52300377657` |
| `evidence/go_tally.py` | 4154 | `ea6968e99bd132096c9e7493215d92bfc440d6ce3dbcc4cde273d267be5ed41f` |
| `evidence/hint_apply.txt` | 5954 | `42a948a8c44950324fae32ee7e7da231a7df62d69ca1661bb62e15cec6dd099e` |
| `evidence/hint_dryrun.txt` | 5835 | `28f813bf1c94adad73c2e0fc888532a43de07f9794cbbdca2465b3d95d8ba29e` |
| `evidence/list_full.jsonl` | 68458 | `4952a9d329dc78dcd7cf1b2c97c616b391cc6601298433d35cf6b4005bf7b867` |
| `evidence/mk_hint.py` | 15691 | `1a856933af616d0b3e49f4b6a3bed4780ea82b977e6d75f9da2dbb75a051b91d` |
| `evidence/phu_luc_B_python3.11.json` | 3331 | `42ca657c282ec38b87170a3b1b98be32b1affd68169bde375540e5d7da1d741d` |
| `evidence/phu_luc_B_python3.12.json` | 3331 | `42ca657c282ec38b87170a3b1b98be32b1affd68169bde375540e5d7da1d741d` |
| `evidence/run_g.sh` | 1478 | `0c159ae9f14d8578f3cb98ceac1b6ff0524f75c2fb20b85cb348c175948e8b2a` |
| `evidence/sanity_case.py` | 425 | `b069d81d6198bf0d46bf4816003c1ff233e539291b2bab3f225e8fd645b1d127` |
| `evidence/sanity_cases.txt` | 645 | `01469e979f541c2c7ae4435512de1e5da015cccc12a7ece71518accaef45b7c3` |
| `evidence/show.py` | 523 | `04fa028a7d13d83b8d86da7453bd6121948ede400843fc095e54af1af1d30bfa` |
| `evidence/static_checks.sh` | 5533 | `3387a725263977465965e9a925ce99dc5dc875768d6284a9d1160bc5a9d15a41` |
| `evidence/static_checks.txt` | 5820 | `6c45b48692c656cff31bf6f4c27676a046c82c2a9c7f675c47c0ce375188f8c2` |
| `evidence/timing.sh` | 1784 | `d799897d04e08697bee144a89dabf7383351f339781d02c4733d8a3d0d20bc48` |
| `evidence/timing.txt` | 511 | `4c66d265011ff7d430f224a9f94f47b69d8e1ca9130fa3a65ea8601f73697808` |
| `evidence/variants.jsonl` | 34294 | `e1b53a22fa122941b51eb203752bde74ada4a2121d35fe38c7967bdb6da7d7cd` |
| `evidence/vet_can.py` | 1207 | `049a8e381e60995614596c6f97ed6f4dd924e3380d3ff94f2147836dfb18c501` |

Công cụ trong `evidence/`: `extra_probes.py` = Phụ lục C của r2 cộng các khối E1–E8 của tôi (E1–E6: 40 dò ngoài tập đóng; E7: 18 dò nhóm Unicode; E8: 6 biến thể F50); `do_reg.py` chạy các đột biến ĐÃ đăng ký trong `DOT_BIEN` của một cây (A5-lite); `run_g.sh` là bộ chạy N tiến trình có canh đĩa; `vet_can.py` là phép vét cạn hai dò tương đương; `static_checks.sh` in lại mọi phép đo tĩnh; `show.py` phân hạng bằng đúng luật Phụ lục D; `mk_hint.py` sinh `HINT.patch`. KHÔNG giao: bản dựng ứng viên (`build_cand.py`) và mọi cây ứng viên/biến thể (Q14: không giao mã `ops/cong_cu_test.py`).
Đo lại bằng: `PYTHONDONTWRITEBYTECODE=1 python3.12 evidence/extra_probes.py <gốc cây> <ra.jsonl> <tên dò>...` (cây nền: bản sao `git` của `fc852ff`; cây ứng viên: bản dựng theo chữ của §5 — tôi không giao).

## SANDBOX, TIẾN TRÌNH VÀ NHỮNG GÌ PHẢI DỌN

Tiến trình (đo lúc ghép `VERDICT.md`; lọc theo tên các script/tiến trình do tôi sinh):
```
$ ps -eo pid,ppid,stat,etime,cmd | grep -E "do_reg|extra|do_dot_bien|run_g|chay_|cong_cu_test" | grep -v grep | wc -l
0
```
Không có tiến trình con của tôi còn chạy, không zombie do tôi sinh (mọi `run_g.sh` chờ `wait` từng con; lượt nền Phụ lục C đầu bị tôi dừng bằng SIGTERM ở 144/221 — chỉ PID tôi sinh).

Cây tạm tôi để lại trong `$R` (KHÔNG xoá được: hệ thống quyền từ chối `rm -rf`, tôi không đi vòng qua chốt đó). Điều phối viên tự xoá khi không cần, và nên xoá TRƯỚC khi trao sandbox cho phiên khác vì `cand/` và `tv_*` chứa bản dựng mã `ops/cong_cu_test.py` mà Q14 không cho giao:
```
tmp.PPZBpxHxVC    191M  bản sao `cp -a` của cay-kho cho lệnh dry-run CUỐI
tmp.Szu0mDNtCY    158K  bản sao tệp đặc tả cho lần áp thật CUỐI
tmp.aS81qabBRf    191M  bản sao cay-kho cho dry-run trước (HINT bản cũ)
tmp.bTzYbIG8z9    2.4G  vùng làm việc chính: cand/, nen/, tv_*, out/, pl/, script, kết quả thô
tmp.jE0HMfMTvY    157K  bản sao tệp đặc tả cho lần áp thật trước (HINT bản cũ)
tmp.l9mU7GC0Ob    1.4M  thử rò thư mục tạm của `t38` (1,4 MB)
tmp.r5ReC8gqah    156K  bản sao nhỏ thử áp HINT sớm
tmp.vYIJ26CReN    150K  bản sao nhỏ thử áp HINT sớm

cây bên trong tmp.bTzYbIG8z9/ :
  tmp.bTzYbIG8z9/cand
  tmp.bTzYbIG8z9/nen
  tmp.bTzYbIG8z9/tv_bmp
  tmp.bTzYbIG8z9/tv_exc
  tmp.bTzYbIG8z9/tv_go_cc
  tmp.bTzYbIG8z9/tv_go_cf
  tmp.bTzYbIG8z9/tv_go_dau
  tmp.bTzYbIG8z9/tv_go_nfkc
  tmp.bTzYbIG8z9/tv_go_ngoai
  tmp.bTzYbIG8z9/tv_go_ra
  tmp.bTzYbIG8z9/tv_go_tab
  tmp.bTzYbIG8z9/tv_go_zs
  tmp.bTzYbIG8z9/tv_god_bq
  tmp.bTzYbIG8z9/tv_god_hong
  tmp.bTzYbIG8z9/tv_god_hong_tich
  tmp.bTzYbIG8z9/tv_god_tich
  tmp.bTzYbIG8z9/tv_god_tk
  tmp.bTzYbIG8z9/tv_god_tk_tich
  tmp.bTzYbIG8z9/tv_head
  tmp.bTzYbIG8z9/tv_ins
  tmp.bTzYbIG8z9/tv_list
  tmp.bTzYbIG8z9/tv_naive
  tmp.bTzYbIG8z9/tv_nora
```
Ghi chú dung lượng: `tv_go_*` dùng liên kết cứng với `cand/`, nên `du` từng cây báo ≈197M nhưng đĩa thật chỉ tăng vài MB mỗi cây.

Hai tệp ngoài vùng cho phép tôi từng ghi nhầm, đều đã xoá ngay bằng `rm -f` và kiểm lại là không còn: `/tmp/__hint_test.patch` (22 KB, thử `patch` lúc soạn) và `/tmp/__x` (tệp rỗng, thử quyền ghi). Không ghi gì khác ngoài `$R/goi/` và `mktemp -d -p $R`; không mạng, không GitHub, không commit/push, không sửa `cay-kho/` (kiểm: `git -C cay-kho status --short` rỗng, HEAD vẫn `c54b502…`).

Thứ tự vá gợi ý cho revision 3 (lời; số liệu trong các câu chèn của `HINT.patch` phải được đo lại):
1. Bốn lớp P2 trước: `m5-ngoai-le-chi-ba-kieu` (dẫn xuất miền ô từ `builtins`), `ra-ha-nguon-main-bo-ghi-chua-co-o` (thêm đường `ra` có cấu trúc vào lưới `main` và bộ ghi), `head-nhieu-dong-chi-tach-lf-chua-co-o` (ô nhiễu + ký tự tách dòng), `t53-thoi-gian-khong-co-tieu-chi-do` (tiêu chí thời gian A4-g).
2. Mười hai lớp P3 sửa văn bản: tám lớp là sửa số/nhãn/câu (`phu-luc-c-dem-209-lech-221`, `s1-8-8-nhan-tag-sai`, `tran-vong-so-10-hai-cho`, `doc-bang-205-vs-211`, `s6-chep-thieu-quy-tac-dung`, `s11-1-thieu-cach-doc-q4-q9-q13`, `thu-hoi-do-khong-co-diem-dung`, `head-moi-vi-tri-moi-thanh-vien-qua-loi`); bốn lớp chính xác hoá tiêu chí (`a1-tap-dong-thieu-do-theo-nhom-unicode`, `a5-canh-khong-kiem-bang-do`, `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`, `a4-d-khong-co-phep-do-may`).
3. Hai trong bốn lớp P2 (`m5-ngoai-le-chi-ba-kieu`, `head-nhieu-dong-chi-tach-lf-chua-co-o`) đã có phép đo "biến thể GIẾT" (`evidence/variants.jsonl`, trường `bien_the` = `v_exc`, `v_head`), nên tiêu chí đóng lớp có thể viết thành "dò X phải GIẾT `t53_…`"; lớp `ra-ha-nguon-main-bo-ghi-chua-co-o` mới đo phía SỐNG (tôi chưa dựng bản vá); lớp `t53-thoi-gian-khong-co-tieu-chi-do` có hai phép đo thời gian (4,2–4,7 s và 63,0–65,5 s).
4. Theo protocol §12 và §8.3: 12 trong 16 lớp lượt này nối với một lớp lượt 1 qua cột "nối" của BẢNG LỚP (chỉ 4 lớp không nối: `phu-luc-c-dem-209-lech-221`, `s1-8-8-nhan-tag-sai`, `doc-bang-205-vs-211`, `s11-1-thieu-cach-doc-q4-q9-q13`). Việc coi một lớp nối là CÙNG lớp hay lớp MỚI để đếm "ba lượt review khác nhau" (S6 (2)) và tính tỷ lệ F/U của chuyển tiếp r1→r2 là việc của điều phối; tôi chỉ cung cấp cột nối và không tự tính F/U.
