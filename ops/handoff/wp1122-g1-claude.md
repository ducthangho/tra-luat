# Handoff #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA — lease wp1122-r1-g1-claude

Nhánh thi công là `agent/wp1122-g1-claude`, base `c82047d`, diff gồm 1 tệp (`.claude/dev/launcher_test.py`). Spec
`ops/specs/wp1122.md`, sha256 `198e06f0…`. Đã gọi Codex **1/10** lượt.

## Phạm vi đã thi công
Gồm các mục của spec cộng hai mở rộng mà chủ kho duyệt qua AskUserQuestion, write set không đổi:
- **Mục tiêu 1:** đổi 57 câu `assert` trần trong 11 ca sang `bang`. Mở rộng: 8 câu `raise AssertionError` làm tín
  hiệu của ca (`t33` và 7 câu trong `r484_g2_storage_kernel_guardrails`) đổi sang `bang(False, …)`. Ba ca cố ý ném
  AssertionError trần nằm trong `ASSERT_TRAN_CHO_PHEP`.
- **Mục tiêu 2:** ca khoá `r1122_khong_assert_tran_trong_ca` (AST, bắt cả `assert` lẫn `raise AssertionError`;
  danh sách cho phép phải khớp đúng). Ba đột biến: chèn lại `assert`, chèn lại `raise`, nới danh sách.
- **Mục tiêu 3:** `mo_ta_loi` cắt thông điệp còn 160 ký tự trong `cham_mot_ca`, nhánh hook, `chay_bo_ca`,
  transport và kênh của `cham_lap_ca`. Ca khoá: `r1122_loi_mang_thong_diep_cat_160` và
  `r1122_reporter_giu_loai_va_cat_dung_thong_diep` (lấy từ HINT Codex lượt 1).
- **Mục tiêu 4: gốc của `t73` ĐÃ ĐO.** Run 41328709141 có `UnicodeDecodeError: 'charmap' codec can't decode byte
  0x90` trong `_readerthread`: `chay()` gọi `text=True` mà không truyền `encoding`, nên Windows giải mã bằng cp1252,
  `r.stdout` ra `None`, và `json.loads` ném `TypeError`. Vá: 14 lời gọi con Python khai
  `encoding="utf-8", errors="replace"`. Ca khoá `r1122_con_python_giai_ma_utf8` đòi đúng giá trị literal (HINT
  lượt 1, F02). Ba đột biến: bỏ encoding, cp1252, None.

## Nghiệm thu
- **N0 (Windows):** run 41328709141, head `4423d18`, mới có mục tiêu 3. Kết quả `432/436`; dòng của t73 là
  `t73_doctor_phai_do_bash_va_npm(TypeError: the JSON object must be str, bytes or bytearray, not NoneType)`.
  Đã tái hiện được lỗi.
- **N0' + A4 (Linux, A/B dựng cả hai vế trong cùng một lệnh, môi trường sau khi đã cài shellcheck/llm/ruff):**
  - base `c82047d`: suite `340/350` (hỏng 10), `--dot-bien 523/548`;
  - head `30ee4ae`: suite `343/353` (hỏng 10), `--dot-bien 529/554`.
  - Tập 10 ca hỏng và tập 25 dòng SAI TRÙNG KHÍT giữa hai vế, tức delta = 0. Mười ca này đều là ca đường
    `launcher.py run` (`r09`, `r15`, `r925_*`, `r926_*`, `r927_*`, `rc=1`) và đỏ sẵn trong container. Gọi
    `launcher.py run` trực tiếp thì vẫn rc=0. Đây là nợ ngoài phạm vi, chưa có Issue.
  - Head `fd1f82e` (sau F01/F02): ĐANG ĐO, sẽ ghi bổ sung.
- **A3 (Windows):** run 41330126129, head `30ee4ae`, job `windows-latest`, runner_id 1000032894. Kết quả
  `DOT BIEN: 440/440 dat (118 khong do duoc)`, suite `281/281` (bỏ qua 74, hỏng 0). Head `fd1f82e`: đã gọi lượt mới.
- **A5:** ruff F base 5 / head 5, `doctrine-scan` rc=0, `git diff --check` rc=0. CI PR: chưa có PR.
- **A6:** chỉ đo được sau land.

## Codex
| lượt | run_id | head | thời lượng | model | verdict |
|---|---|---|---|---|---|
| 1 | `e03d300896404d949c69ef6a9a0e4a92` | `30ee4ae` | 834.9 s | `gpt-6.1-sol` theo danh sách khung (trạng thái KHONG_DO_DUOC) | changes_requested (0/1/1/0) |

Lượt 1 có hai finding:
- F01 (P1): reporter chưa cắt đúng 160 ký tự, và kênh lặp tên loại.
- F02 (P2): khoá encoding chỉ kiểm có khoá, không kiểm giá trị.

Cả hai đã vá ở `fd1f82e` bằng HINT.patch áp nguyên văn. Hiện vật nằm ở `luot1/` kèm `SHA256SUMS`. Thư mục
`evidence/` (427M) của reviewer KHÔNG chép vào kho, chỉ giữ trong scratchpad của phiên.

## Ghi chú môi trường
Ruff chưa được cài lúc đo lần đầu. Lệnh `python3 -m ruff` khi đó trả "No module named ruff", và số "1/1" trong
handoff #1117 đã được đính chính (`a9c866d`). Chủ kho yêu cầu cài đủ công cụ: đã cài shellcheck 0.9.0, llm 0.36 và
ruff; `doctor --kiem-song` cho thấy Codex sống.
