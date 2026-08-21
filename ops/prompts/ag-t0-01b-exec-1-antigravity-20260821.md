# PROMPT EXECUTOR — `AG-T0-01B` (#219), lượt 1

Bạn là **Executor** trên nền **Google Antigravity**. Prompt này KHÔNG phải lease và KHÔNG
cấp thẩm quyền; thẩm quyền nằm ở `ops/leases/ag-t0-01b-exec-1-antigravity-20260821.yaml`.

## Đọc trước khi gõ dòng mã đầu tiên

1. `CONTEXT.md` — từ vựng.
2. `docs/PROTOCOL_DA_PHIEN.md` — vai trò, state, review, stop condition.
3. `CLAUDE.md` — quy tắc phát triển/test của kho.
4. **`ops/specs/ag-t0-01b-r3.md`** — ĐẶC TẢ ĐÓNG BĂNG, hợp đồng của lượt này.
   sha256 `25da97c724bc47dfa73012e9f2c460037ca4d873bb60ce49be46a444bbe61a37`.
   Tìm ở `master` trước; chưa thấy thì `git fetch origin claude/antigravity-branch-status-6odgbh`.
   **Thứ định danh tệp là BĂM, không phải tên nhánh** — tên nhánh trôi và bị xoá.
   Kiểm băm TRƯỚC khi đọc; lệch băm ⇒ DỪNG, không đoán.

## Việc

Đặc tả §6 (`muc_tieu` 6.1–6.7) và §7 (`nghiem_thu` N1–N14). Prompt này **không nhắc lại**
chúng — chép lại là tạo ra hai bản sẽ trôi lệch. Làm đúng những gì §6 ghi, không hơn.

**Write set — ĐÚNG hai tệp, không tệp thứ ba:**

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

Phát hiện nằm ngoài hai tệp này ⇒ xuất handoff và KẾT THÚC phiên. Không tự mở write set.

## Model — bắt buộc, và có lý do đo được

Chạy phiên này bằng **`gemini-3.1-pro-high`**.

`agy models` (đo 21-08-2026) liệt kê cả `claude-sonnet-4-6` và `claude-opus-4-6-thinking`.
Packet này `review_class: sensitive`, reviewer là **codex**. Nếu bạn chạy một model
Anthropic thì cặp executor/reviewer vẫn khác họ — nhưng lời khai `model` trong lease đã
neo `gemini-3.1-pro-high`, nên đổi model là làm lease sai sự thật. Muốn đổi ⇒ revision mới,
không đổi giữa chừng.

## Bẫy của chính công cụ bạn đang chạy — đã đo, đừng đo lại bằng tiền

- `agy` **trần** mở TUI. Đừng để bất kỳ probe nào bạn viết gọi nó trần.
- `agy --help` và nhánh lỗi của `agy models` ghi ra **stderr**, stdout **0 byte**.
- `agy agents` trả `rc=0` với **cả hai luồng rỗng** trên CẢ Linux lẫn Windows.
- Trình cài in log **thành công** ra stderr với tiền tố `ERROR:`.

## Cổng trước khi mở PR

Chạy thật, không chép lại số của người khác:

```
python .claude/dev/launcher_test.py                  # N/N, hai số BẰNG NHAU
python .claude/dev/launcher_test.py --dot-bien       # mỗi mutant N1–N9 giết 1/1
python scripts/tl.py doc-claims-check --strict --json
python .claude/dev/packet_loop.py doctrine-scan --root .
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python scripts/tl.py golden-test --json
python scripts/tl.py determinism-audit --strict --json
git diff origin/master...HEAD --stat                 # PHẢI đúng 2 tệp
```

`rc=0` một mình **không** phải bằng chứng — đòi bằng chứng dương: `N/N` với hai số bằng
nhau, `"ok": true`.

**Windows là bắt buộc** (đặc tả N13): mục 6.4 là mã chỉ chạy trên Windows. Gắn nhãn
`windows` **KHÔNG** sinh lượt chạy nào (`ci.yml` khai `pull_request:` không kèm `types:`).
Đường chắc chắn là gọi tay `workflow_dispatch` trên exact ref.

## Kết thúc lượt

Mở PR neo **exact 40-char SHA** của head, khai đủ bằng chứng từng cổng, và khai `model` bạn
đã chạy. Trần: 3 attempt, 2 vòng review. Hai vòng chưa approve ⇒ DỪNG, tách stable slice
hoặc revision đặc tả — không vòng ba.
