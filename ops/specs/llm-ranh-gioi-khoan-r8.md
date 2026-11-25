# LLM-RANH-GIOI-KHOAN r8: chặn bảo thủ các lỗ ranh giới khoản còn nợ của `llm-khai-niem` và đo Windows bản địa (đặc tả đóng băng)

- **Packet:** #1514. Revision 8, generation 1 (thay r7; r1–r7 giữ ở `ops/specs/llm-ranh-gioi-khoan-r{1,2,3,4,5,6,7}.md`). Role `executor` (Claude), reviewer Codex. Review Class `sensitive`.
  Lý do: write set chạm mã runtime trong gói phát hành (`scripts/tl_core/llm_route.py`); cổng lease tính lớp `sensitive` cho role
  `executor` (`lease_publish.py check` rc 10 khi khai `routine`).
- **Căn cứ:** Issue #1514; nợ #1512; verdict lượt 11 `ops/reviews/pr1503-review-11-codex/VERDICT.md` (X2, X3, X4).
  Chủ kho giao trong phiên `session_015GtxrZQYT3Vt8PJdXrjEKg` ngày 25-11-2026: *"Xử lý các nợ trong packet riêng đi"*; chọn hướng
  *"Chặn bảo thủ trên văn bản thô"* và trần review Codex **5** lời gọi. Sau lượt 5 (APPROVE, còn hai P2 E1/E2 — ADR-0060 M1
  đòi 0 P2 mở trước merge), chủ kho chọn *"Raise the cap to 6, fix E1/E2, run Codex round 6"*: trần nâng lên **6**. Sau lượt 6 (APPROVE, còn hai P2
  F1/F2 cùng lớp `ranh-gioi-khoan`, tỷ lệ đóng lớp 0/1), chủ kho chọn *"Switch to allowlist, cap 7, one more Codex round"*: trần **7**. Sau lượt 7 (APPROVE, còn một P2 G1), chủ kho chọn
  *"Reject the source when a non-standard first line ends in ':', cap 8, last review"*: trần **8**. Sau lượt 8 (APPROVE, còn một P2
  H1), chủ kho trả lời *"Vá nốt đi, nâng trần"*: trần **9**.
- **Baseline nghiệm thu:** `64b7f2c14776d5d0e1d34a6be4725490956f5bec` (master sau #1513).

## 1. Bất biến giữ nguyên
- Kết quả luôn mang `can_nguoi_duyet: true` và `pham_vi_kiem` (lời khai KHÔNG nâng lên).
- Mọi chốt hiện có của `tach_khoan`/`_dong_mo_ho`/`_tu_noi`/`lech_nguyen_van` giữ nguyên hành vi; packet chỉ THÊM điều kiện từ chối.
- Không đổi đường gọi model (`goi`, `duong_api`, `duong_sub`, `_chay_co_moc`) trừ khi phép đo Windows (§3) tìm ra lỗi thật.
- Điều 3 Luật 134/2025/QH15 (nguồn mất số, 8 khoản, mỗi dòng kết thúc bằng `.`) cùng ba kết quả đã lưu (`tl`/`sub`/`api`) vẫn đạt 8/8.

## 2. Hành vi mới (`scripts/tl_core/llm_route.py`)
### 2.1 X2 — nháy kép thẳng nhiều hơn một cặp
Một dòng (sau `_bo_dau_dong`) chứa từ **3** dấu `"` (U+0022) trở lên ⇒ `_dong_mo_ho` trả True (nguồn mơ hồ, từ chối cả nguồn).
Lý do: hai tầng trích dẫn bị làm phẳng không phân biệt được với hai cụm độc lập. Chặn oan dòng có hai cụm `"…"` độc lập là giới hạn
đã khai.
### 2.2 X3b + X3c — mỗi khoản phải kết thúc bằng dấu câu kết
Sau khi gom điểm và tiếp dòng, văn bản của MỖI khoản (bỏ khoảng trắng và các dấu đóng `)` `"` `”` ở cuối) phải kết thúc bằng một trong
`.` `;` `!` `?`. Khoản nào không thoả ⇒ `tach_khoan` trả None (nguồn mơ hồ).
- X3b (nguồn mất số): dòng gãy giữa câu thành một khoản không kết thúc bằng dấu câu kết ⇒ chặn.
- X3c (nguồn có số): khoản trước một dòng mang số mà không kết thúc bằng dấu câu kết (kể cả kết thúc bằng `:` — tức đang mở tiểu mục)
  ⇒ chặn.
- `:` KHÔNG phải dấu câu kết của khoản: khoản mở bằng `… sau:` hợp lệ khi có các dòng điểm theo sau và dòng điểm cuối kết thúc bằng
  dấu câu kết.
### 2.3 X3 — câu dẫn
Một dòng đứng TRƯỚC khoản đầu chỉ được bỏ như câu dẫn khi khớp (không phân biệt hoa thường, sau khi gộp khoảng trắng)
`(được hiểu|được giải thích)\s+như\s+sau\s*:$`. Dòng đầu kết thúc bằng `:` mà không khớp mẫu ⇒ KHÔNG bỏ: nó được xử lý như một dòng
thường (ở nguồn mất số thành một khoản và bị §2.2 chặn vì kết thúc bằng `:`; ở nguồn có số thành dòng lạ trước khoản đầu ⇒ None).
### 2.4 X4 — so nguyên văn giữ ranh giới dòng
`lech_nguyen_van` so thuật ngữ và định nghĩa với nguồn theo một chuẩn hoá GIỮ xuống dòng: trong mỗi dòng gộp khoảng trắng; giữa các
dòng giữ đúng một `\n`; bỏ dòng rỗng. Định nghĩa của model gộp các dòng điểm thành một dòng ⇒ lệch.
Ngoại lệ có sẵn giữ nguyên: tiếp dòng mở bằng "là" (lượt 4 Q3) nằm ở ranh giới thuật ngữ/từ nối nên không ảnh hưởng.

## 2.5 Bổ sung r2 (cross-review lượt 2 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-2-codex/VERDICT.md`)
Lượt 2 chỉ ra ba dạng tách/bỏ khoản mà luật r1 chưa chặn (A2, P1). r2 thêm ba điều kiện từ chối (vẫn chỉ THÊM, không nới):
- **A2a — `;` không kết khoản:** dấu câu kết của khoản (§2.2) thu hẹp còn `.` `!` `?`. Ngắt dòng sau `;` giữa một định nghĩa dài
  từng tạo hai khoản đều qua kiểm. `;` vẫn hợp lệ ở các dòng điểm KHÔNG phải dòng cuối của khoản.
- **A2b — đánh số nội dòng:** thân khoản (sau khi bỏ số của chính khoản) chứa mẫu `(?:^|\s)\(?\d+[.)](?=\s)` (vd `… 1. …`,
  `… (2) …`) ⇒ nguồn mơ hồ. Tiểu mục đánh số trong khoản cuối có thể trùng số khoản kế. Số thập phân (`1.5`) không khớp.
  Chặn oan câu dẫn chiếu kiểu `khoản 1. Điều 5` là giới hạn đã khai.
- **A2c — tiêu đề có chữ "là":** dòng tiêu đề Điều (§`_RE_TIEU_DE_DIEU`) chứa chữ "là" ở BẤT KỲ đâu ⇒ nguồn mơ hồ (tiêu đề có thể
  dính khoản đầu; `_tu_noi` dừng ở dấu `:` của `Điều 3: …` nên phép dò r1 bỏ sót).
Các vá trong phạm vi r1 cùng lượt: A1 (giữ điều kiện "dòng câu dẫn KHÔNG có từ nối" — §1 bất biến), A3 (§2.2 bỏ CẢ dải đuôi khoảng
trắng + dấu đóng), A4 (§4.6 fixture Điều 3 THẬT 8 khoản + ba kết quả đã lưu).

## 2.6 Bổ sung r3 (cross-review lượt 3 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-3-codex/VERDICT.md`)
- **C1 — tiêu đề (thay A2c):** dòng đầu khớp tiền tố `_RE_TIEU_DE_DIEU` chỉ được BỎ khi CẢ dòng (sau khi gộp khoảng trắng) khớp
  `^Điều\s+\d+[a-zđ]?\s*[.:]\s*(?:Giải thích từ ngữ\s*\.?)?$` (không phân biệt hoa thường). Phần dư khác ⇒ nguồn mơ hồ. Danh sách
  CHO PHÉP hình dạng tiêu đề thay cho dò chữ "là" (bỏ sót khoản dùng từ nối khác và "là" sát dấu câu). Tiêu đề có tên khác
  "Giải thích từ ngữ" bị chặn — giới hạn đã khai.
- **C2 — đánh số nội dòng chỉ trong một dòng (sửa A2b):** mẫu thành `(?:^|[ \t])\(?\d+[.)](?=[ \t])` — số điều ở cuối một dòng điểm
  (theo sau là xuống dòng) không bị bắt nhầm.

## 2.7 Bổ sung r4 (cross-review lượt 4 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-4-codex/VERDICT.md`; đo Windows §3)
- **D1 — khoảng trắng Unicode (sửa §2.6 C2):** mẫu đánh số nội dòng thành `(?:^|[^\S\n])\(?\d+[.)](?=[^\S\n])` — mọi khoảng trắng
  TRỪ xuống dòng (gồm U+00A0); vẫn không so xuyên dòng.
- **D3 — câu dẫn chỉ ở dòng đầu (sửa §2.3):** chỉ dòng ĐẦU (ngay sau tiêu đề) được bỏ như câu dẫn; câu dẫn lặp hoặc muộn không bị bỏ.
- **D2 — giới hạn đã khai:** tiêu đề viết HOA ở tiền tố (`ĐIỀU 3.`) và tên "Giải thích từ ngữ" xuống dòng riêng bị chặn.
- **Windows bản địa (§3, run `45542712141`, job `gate (windows-latest)`):** selftest `r380_llm_khai_niem_bien_dau_vao` (có trên master từ
  PR #1503) đỏ vì phép kiểm giữ quyền 0644 — trên Windows `chmod` chỉ bật/tắt cờ chỉ-đọc. r4 thêm `scripts/tl_selftest.py` vào write
  set; phép kiểm quyền chỉ áp trên POSIX. Hành vi sản phẩm (`_ghi_nguyen_tu_giu_quyen`) không đổi.

## 2.8 Bổ sung r5 (cross-review lượt 5 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-5-codex/VERDICT.md`)
- **E1 — dấu số dính thân (sửa §2.7 D1):** mẫu đánh số nội dòng thành `(?:^|[^\S\n])\(?\d+[.)](?=[^\S\n]|[^\W\d_])` — sau dấu số
  là khoảng trắng (trừ xuống dòng) HOẶC một chữ cái, cùng cú pháp với bộ nhận số đầu dòng `_RE_SO_KHOAN` (`1.Hồ sơ`). Số thập
  phân (`1.5`) và số ở cuối dòng vẫn không bị bắt.
- **E2 — hình dạng câu dẫn (sửa §2.7 D3):** dòng đầu chỉ được bỏ như câu dẫn khi, ngoài các điều kiện cũ, có ĐÚNG MỘT dấu `:` (ở
  cuối) và KHÔNG chứa chữ "là" đứng riêng ở bất kỳ đâu (`(?<!\w)là(?!\w)`, kể cả sát ngoặc). Câu dẫn khác hình dạng ấy bị chặn —
  giới hạn đã khai.
- **Windows bản địa (§3):** run `45553156011` trên `9541e02` — kết quả ghi trong `VERDICT.md`.

## 2.9 Bổ sung r6 (cross-review lượt 6 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-6-codex/VERDICT.md`)
Sáu lượt liên tiếp tìm ra một dạng mới trên CÙNG một lớp (đánh số nội dòng A2b→C2→D1→E1→F1; câu dẫn X3→A1→D3→E2→F2) vì mỗi bản
vá LIỆT KÊ dạng xấu. r6 đảo thành danh sách CHO PHÉP / tập bao:
- **F2 — câu dẫn (thay §2.3, §2.5 A1, §2.7 D3 phần hình dạng, §2.8 E2):** dòng đầu (ngay sau tiêu đề) chỉ được bỏ khi CẢ dòng (gộp
  khoảng trắng, PHÂN BIỆT hoa thường) khớp
  `(?:Trong|Tại) (?:Luật|Bộ luật|Pháp lệnh|Nghị định|Nghị quyết|Thông tư|Thông tư liên tịch|Quyết định) này, (?:các|những)
  (?:từ ngữ|thuật ngữ) (?:dưới đây|sau đây) được (?:hiểu|giải thích) như sau:`. Mọi câu dẫn khác ⇒ không bỏ ⇒ nguồn bị chặn (giới
  hạn đã khai). Điều kiện "chỉ dòng đầu" (D3) giữ nguyên.
- **F1 — đánh số nội dòng (thay §2.5 A2b, §2.6 C2, §2.7 D1, §2.8 E1):** mẫu thành
  `(?<![\w.,])(?:\(\d+\)|\d+[^\S\n]*[.)])(?![\d\n]|$)` — TẬP BAO cú pháp `_RE_SO_KHOAN` đầu dòng (`(N)`, `N.`/`N)` có hoặc không
  khoảng trắng trước dấu, theo sau bởi bất kỳ ký tự nào). Chỉ ba ngoại lệ: theo sau là chữ số (số thập phân), xuống dòng hoặc hết
  chuỗi (số điều cuối dòng điểm, C2); đứng trước là chữ/số, `.` hay `,`. Mã nghiệp vụ dạng `… 2.A …` bị chặn (giới hạn đã khai).
- Mỗi mẫu một đột biến NỚI danh sách cho phép / thu hẹp tập bao về bản r5 ⇒ ca đích phải đỏ.

## 2.10 Bổ sung r7 (cross-review lượt 7 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-7-codex/VERDICT.md`)
- **G1 — dòng đầu kết `:` ở nguồn mất số:** sau khi bỏ tiêu đề và câu dẫn chuẩn (§2.9), nếu nguồn KHÔNG có dòng mang số và dòng ĐẦU
  còn lại (vị trí 0) kết thúc bằng `:` (bỏ dải khoảng trắng + `)` `"` `”` ở cuối) ⇒ `tach_khoan` trả None. Dòng ấy có thể là câu
  dẫn lạ hoặc khoản đầu; giữ nó làm khoản rồi gom các dòng điểm vào là đoán. Khoản mở bằng `… sau:` có điểm theo sau vẫn hợp lệ ở
  mọi vị trí khác (sau câu dẫn chuẩn). Nguồn mất số bắt đầu ngay bằng một khoản như thế mà không có câu dẫn chuẩn bị chặn — giới
  hạn đã khai.

## 2.11 Bổ sung r8 (cross-review lượt 8 — `ops/acceptance/llm-ranh-gioi-khoan/r1/review-8-codex/VERDICT.md`)
- **H1 — chốt theo VAI TRÒ (THAY §2.10):** chốt r7 xét ký tự kết dòng (`:` ASCII) nên `：` (U+FF1A) hay dấu khác lọt. r8 bỏ chốt ấy và
  chặn theo vai trò: ở nguồn KHÔNG có dòng mang số mà KHÔNG có câu dẫn chuẩn được bỏ (§2.9), một dòng điểm nối vào KHOẢN ĐẦU
  ⇒ `tach_khoan` trả None — bất kể dòng đầu kết bằng ký tự gì. Có câu dẫn chuẩn thì khoản đầu có điểm vẫn hợp lệ. Nguồn mất số
  không có câu dẫn chuẩn mà khoản đầu có điểm bị chặn — giới hạn đã khai (thay giới hạn của §2.10).

## 3. Đo Windows bản địa (không sửa CI)
Gọi tay `ci.yml` bằng `workflow_dispatch` với `runner_set=windows-only` trên nhánh của packet. Đọc job `gate-registry (windows-latest)`:
dòng `CI_DANG_KY scripts/tl_core/llm_route_test.py: …`. Ghi kết quả (đạt, đỏ, hay bỏ qua) vào `VERDICT.md`. Đỏ vì lỗi thật của
`_chay_co_moc` trên Windows ⇒ vá trong packet nếu nằm trong write set; ngoài write set ⇒ handoff.

## 4. Test (`scripts/tl_core/llm_route_test.py`)
Mỗi chốt mới một ca (hoặc một mẫu riêng trong ca chung) và ít nhất một đột biến riêng bị giết bằng `TinHieuChotCa` của ca đích:
1. X2: dòng có 4 dấu `"` (hai tầng làm phẳng) ⇒ None; đối chứng một cặp `"…"` vẫn đạt.
2. X3b: nguồn mất số có dòng gãy giữa câu mà cả hai mảnh đều có "là" và hai vế hợp lệ ⇒ None.
3. X3c: nguồn có số với khoản kết thúc `:` rồi dòng mang số kế tiếp; và khoản không dấu câu kết rồi dòng mang số ⇒ None. Đối chứng
   khoản `… sau:` + điểm `a)`, `b)` kết thúc `.` vẫn đạt.
4. X3: dòng đầu `X gồm:` (không khớp mẫu câu dẫn) không bị bỏ ⇒ kết quả bỏ khoản đầu bị chặn; câu dẫn chuẩn (cả "được giải thích
   như sau:") vẫn được bỏ.
5. X4: định nghĩa gộp các dòng điểm thành một dòng ⇒ lệch; giữ đúng xuống dòng ⇒ đạt.
6. Điều 3 thật (văn bản tổng hợp cùng hình dạng trong fixture) vẫn đạt.

## 5. Ngoài phạm vi
- Ranh giới khoản từ nguồn có cấu trúc (danh sách đánh số của .docx) — packet riêng nếu chủ kho mở.
- Không sửa `ops_misc.py`, `command_registry.py`, `tl.py`, `ci.yml`, `launcher.py`. (`tl_selftest.py` được thêm ở r4, §2.7.)
- Không bump VERSION; không deploy Package.

## 6. Nghiệm thu
1. `python scripts/tl_core/llm_route_test.py`: mọi ca đạt, mọi đột biến bị giết.
2. `python scripts/tl.py --selftest` N/N; `release-verify RELEASE_MANIFEST.json --strict` đạt; các audit `workflow-audit --strict`,
   `golden-test`, `determinism-audit --strict`, `doc-claims-check --strict` rc 0; ruff F delta 0.
3. Phép đo Windows §3 có kết quả ghi trong `VERDICT.md` (kể cả khi là `not_measured` kèm lý do).
4. Cross-review Codex (trần 9 lời gọi TÍNH CHUNG cho packet; r1 dùng 2, r2–r7 mỗi bản dùng 1) — kết luận ghi trong `VERDICT.md`.
