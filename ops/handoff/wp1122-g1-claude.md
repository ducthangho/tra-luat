# Handoff #1122 LAUNCHER-TEST-WINDOWS-TIN-DUNG-GIA — lease wp1122-r1-g1-claude

Trạng thái lúc 00:05Z 02-11-2026: **ĐỦ ĐIỀU KIỆN MERGE THEO LEASE (M-1 đến M-3), CHƯA MERGE.** Codex lượt 10/10 cho
`approve` trên `9d06bd1`, kết quả 0 P0 · 0 P1 · 0 P2 · 0 P3. Merge thuộc quyền chủ kho; `uy_quyen_merge: false`.

- PR: #1130 (draft). Nhánh `agent/wp1122-g1-claude`, head `9d06bd10ce9f2ec6d07f13308bfb6990eb1ee651`, base `c82047d`.
- Diff: 1 tệp, `.claude/dev/launcher_test.py` **+450/−93**, đúng trần 450 dòng thêm của `ADR-0053`. Để giữ trần, ở lượt 8
  đã bỏ 20 dòng trống trong khối test mới của packet; không bỏ ca, chốt, comment hay docstring nào.
- Spec `ops/specs/wp1122.md`, sha256 `198e06f0…`.

## Phạm vi đã thi công
Gồm spec cộng ba quyết định chủ kho chốt qua AskUserQuestion; write set không đổi:
1. 57 câu `assert` trần và 8 câu `raise AssertionError` đóng vai tín hiệu đổi sang `bang`. Ca khoá AST
   `r1122_khong_assert_tran_trong_ca` có danh sách cho phép đúng 3 ca.
2. Gốc `t73` đã đo được (run 41328709141): `chay()` gọi `text=True` mà không truyền `encoding`, nên Windows giải mã
   bằng cp1252, `_readerthread` chết, `r.stdout` ra `None`. Vá: 14 lời gọi con Python khai
   `encoding="utf-8", errors="replace"`; ca khoá AST đòi đúng giá trị literal.
3. Thông điệp ngoại lệ cắt 160 ký tự (`mo_ta_loi`) ở mọi reporter. stdout/stderr được chuẩn hoá UTF-8. Có biên bắt
   lỗi ở điểm vào CLI.
4. **Quyết định của chủ kho sau Codex lượt 5:** kênh `--lap-ca` KHÔNG mang thông điệp (bỏ `CHI_TIET_HONG`, `ten_loai`,
   `thong_diep`). Trường `loai` là ảnh chụp lấy từ lần lặp NGOÀI có hỏng. `chay_bo_ca` định dạng lỗi một lần, rồi mới
   ghi `LOAI_HONG` (lượt 6), để ca lồng hay `__str__` lồng không đổi được `loai`. Trước đây có tín dụng giết giả ở đúng
   chỗ này, và lỗi đó có sẵn từ base. Chi tiết `loi` của nhánh harness sẽ do #1117 mang qua runner.

## Nghiệm thu (Codex lượt 10 đối chiếu từng mục trên log của đúng SHA)
- **N0 (Windows):** run 41328709141 trên `4423d18` cho `432/436` với dòng `t73…(TypeError: the JSON object must be str…)`.
- **N0′ + A4 (Linux, A/B dựng hai vế trong một lệnh, TMPDIR cô lập):**
  - base `340/350` (hỏng 10), `--dot-bien 523/548`;
  - head `9d06bd1`: `352/362` (hỏng 10), `550/575`.
  - Tập ca hỏng và tập dòng SAI trùng khít giữa hai vế, tức delta = 0. Mười ca đỏ sẵn là ca đường `launcher.py run`
    (`r09`, `r15`, `r925_*`, `r926_*`, `r927_*`) trong container. Đây là nợ ngoài phạm vi, chưa có Issue.
- **A3 (Windows, đúng head):** run 41361328113, job `windows-latest`. Kết quả `DOT BIEN: 461/461 dat` (118 không đo
  được), suite `290/290` (bỏ qua 74, hong 0). Trước bản vá, master ra 430/434.
- **A5:** ruff F base 5 / head 5 (delta 0); `doctrine-scan` rc=0; `git diff --check` rc=0. CI `ci.yml` trên `9d06bd1`:
  26 check run, gồm 25 success và 1 skipped (`launcher` PR, vì chạy bằng nhãn); đủ 23 job CI đều success.
- **A6 (CHƯA ĐO ĐƯỢC):** lượt push master sau merge phải cho `launcher-windows.yml` ra `M/M`. Phiên land đọc log job
  `windows-latest` của merge SHA.

## Codex — 10/10 lời gọi (trần ADR-0055; chủ kho chốt "chạy tới sạch, dừng ở trần 10")
| lượt | head | verdict (P0/P1/P2/P3) | ghi chú |
|---|---|---|---|
| 1 | `30ee4ae` | changes_requested 0/1/1/0 | F01 reporter, F02 khoá encoding |
| 2 | `6cf0cc5` | changes_requested 0/1/0/0 | F01: 4 đường |
| 3 | `4c6f933` | changes_requested 0/1/0/0 | F01: Unicode trên console + reporter mà executor liệt kê sót |
| 4 | `93a9afe` | changes_requested 0/1/0/0 | F01: kênh phát lại chi tiết cũ, lỗi I/O ra traceback |
| 5 | `365c751` | changes_requested 0/1/0/0 | F01: ca lồng ghi đè map; HINT +455 vượt trần ⇒ chủ kho chốt gỡ thông điệp khỏi kênh |
| 6 | `5d21d55` | changes_requested 0/1/0/0 | F01: `__str__` lồng ⇒ tín dụng giả |
| 7 | `cccc5eb` | KHÔNG CÓ | bộ lọc nội dung của nền chặn sau 78 s; vẫn tính 1 lời gọi |
| 8 | `cccc5eb` | changes_requested 0/0/1/0 | P2: ca khoá thứ tự chưa phủ nhánh AssertionError |
| 9 | `9d06bd1` | changes_requested 0/0/0/0 | chỉ thiếu bằng chứng của đúng head trong bundle offline |
| 10 | `9d06bd1` | **approve 0/0/0/0** | bằng chứng Windows/CI/A-B đã đưa vào `luot10/bang-chung/` |

Hiện vật của từng lượt nằm ở `luot{1..10}/` (riêng lượt 7 ở `luot7-bi-chan/`). Mỗi thư mục có PROMPT, VERDICT, HINT và
`run/` kèm `SHA256SUMS`.

## Hình dạng lỗi lặp (L4) — cho packet sau
F01 `reporter-thong-diep` mở lại **6 lần** (lượt 1–6). Lượt 3 lộ ra vì phép liệt kê của executor chỉ quét theo vùng
dòng; lượt 4–6 là hệ quả của map toàn cục `LOAI_HONG`/`CHI_TIET_HONG` dùng làm authority. Gốc của lớp này chỉ đóng hẳn
khi #1117 bỏ kênh `--lap-ca` và chuyển sang runner. Spec r2 của #1117 phải chép số đếm này sang.

## Bài học môi trường (đo được trong phiên này)
- Codex chạy song song với A/B ⇒ sandbox tạo `/tmp/.git` ⇒ 11 ca `r484_*` đỏ giả. Đặt `TMPDIR` riêng cho phép đo (ngoài
  `/tmp`) thì loại được nhiễu này.
- Lúc đo đầu, ruff chưa được cài, nên "1/1" ở handoff #1117 là sai và đã đính chính. Đã cài shellcheck, llm, ruff
  theo yêu cầu của chủ kho.
- Codex CLI 0.166 lấy `flock(LOCK_EX)` trên `CODEX_HOME/auth.lock` khi ghi `auth.json` (strace bằng khoá API giả). Đây là
  căn cứ cho #824 làm CAS thật.
