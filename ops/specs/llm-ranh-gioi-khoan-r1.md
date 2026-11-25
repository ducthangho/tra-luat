# LLM-RANH-GIOI-KHOAN r1: chặn bảo thủ các lỗ ranh giới khoản còn nợ của `llm-khai-niem` và đo Windows bản địa (đặc tả đóng băng)

- **Packet:** #1514. Revision 1, generation 1. Role `executor` (Claude), reviewer Codex. Review Class `sensitive`.
  Lý do: write set chạm mã runtime trong gói phát hành (`scripts/tl_core/llm_route.py`); cổng lease tính lớp `sensitive` cho role
  `executor` (`lease_publish.py check` rc 10 khi khai `routine`).
- **Căn cứ:** Issue #1514; nợ #1512; verdict lượt 11 `ops/reviews/pr1503-review-11-codex/VERDICT.md` (X2, X3, X4).
  Chủ kho giao trong phiên `session_015GtxrZQYT3Vt8PJdXrjEKg` ngày 25-11-2026: *"Xử lý các nợ trong packet riêng đi"*; chọn hướng
  *"Chặn bảo thủ trên văn bản thô"* và trần review Codex **5** lời gọi.
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
- Không sửa `ops_misc.py`, `command_registry.py`, `tl.py`, `tl_selftest.py`, `ci.yml`, `launcher.py`.
- Không bump VERSION; không deploy Package.

## 6. Nghiệm thu
1. `python scripts/tl_core/llm_route_test.py`: mọi ca đạt, mọi đột biến bị giết.
2. `python scripts/tl.py --selftest` N/N; `release-verify RELEASE_MANIFEST.json --strict` đạt; các audit `workflow-audit --strict`,
   `golden-test`, `determinism-audit --strict`, `doc-claims-check --strict` rc 0; ruff F delta 0.
3. Phép đo Windows §3 có kết quả ghi trong `VERDICT.md` (kể cả khi là `not_measured` kèm lý do).
4. Cross-review Codex (trần 5 lời gọi) — kết luận ghi trong `VERDICT.md`.
