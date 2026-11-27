# Executor wp1466 (#1466), lượt 1 — Claude Fable 5.2, effort high

Bạn là EXECUTOR của packet `wp1466`, kho `ducthangho/tra-luat`. Bạn chạy trong clone riêng: thư mục hiện tại (`kho/`),
nhánh `claude/wp1466-r8-g1`, HEAD = base `1fac6ced8e5a8c76fdb2699edac779a4251f6149`. Mọi trao đổi viết tiếng Việt.

## Thẩm quyền
- Lease: `ops/leases/wp1466-r8-g1-claude.yaml` trên nhánh `origin/ops/wp1466-r8-g1-lease`, commit `d60fc3a`.
  Đọc bằng `git fetch origin ops/wp1466-r8-g1-lease && git show FETCH_HEAD:ops/leases/wp1466-r8-g1-claude.yaml`.
- Đặc tả đóng băng: `ops/specs/wp1466.md` (r8). Kiểm sha256 ĐẦU TIÊN, phải ra
  `98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834`. Lệch thì DỪNG và báo lại.
- Write set có đúng bốn tệp, KHÔNG ghi tệp nào khác trong kho:
  `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` · `docs/PROTOCOL_DA_PHIEN.md` ·
  `docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md`.

## Đọc trước, theo thứ tự
1. `CLAUDE.md`.
2. `SKILL.md`, lõi skill tra-luat. Chủ kho dặn đọc kỹ để vá đúng.
3. `.claude/skills/work-packet/SKILL.md`.
4. `docs/PROTOCOL_DA_PHIEN.md` các mục §5, §7, §8, §8.3, §10, §12, §13.
5. `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`.
6. Toàn văn `ops/specs/wp1466.md`. Đặc biệt mục 5 (write set), 8 (hợp đồng thay đổi), 9 (N1–N16) và 10 (trần), cùng các khối mã:
   - `adr`: nguyên văn ADR-0068;
   - `khoa` và các khối protocol;
   - `do-pham-vi` (N8);
   - `so-dang-ky`.
7. `ops/specs/wp1466/BAN_GIAO_CODEX.md`.

## Việc
1. Lấy nguyên mẫu `ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch`, là diff `48d372e..c35ee03`, numstat +434 −4, và áp lên
   base bằng `git apply -3 -p1`. Đo trước rằng ba tệp áp sạch, còn `packet_loop_test.py` XUNG ĐỘT đúng 1 khối: B4 (#1462) và
   #1236-C đã thêm ca/đột biến vào cùng vùng đăng ký. Giải khối xung đột sao cho GIỮ ĐỦ mọi ca và đột biến của master, đồng
   thời THÊM đủ ca và đột biến của nguyên mẫu.
2. Đối chiếu mã giao nộp với hợp đồng của đặc tả, không chỉ với nguyên mẫu. Đặc tả là nguồn sự thật:
   - nội dung ADR-0068 phải trùng khối `adr`;
   - các khối protocol thêm vào phải trùng các khối p1–p6;
   - hằng `INV_KHOA_PROTOCOL` phải khớp khối `khoa`. Tự băm lại 7 đơn vị trên blob protocol của bạn, theo định nghĩa ở
     mục 8.3 của đặc tả.

   Base mới đã đổi `packet_loop.py`/`packet_loop_test.py` so với `48d372e`, nhưng KHÔNG đổi `docs/PROTOCOL_DA_PHIEN.md`.
   Hãy kiểm lại điều này.
3. Đo lại MỌI tiêu chí N1–N16 đo được tại chỗ trên mã giao nộp, mỗi tiêu chí ghi lệnh, rc và output. Tối thiểu gồm:
   - `python .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .`;
   - chạy TRỌN `python .claude/dev/packet_loop_test.py`, đòi N/N với hai số bằng nhau;
   - vòng đột biến mới và đột biến cũ, theo đúng cách đặc tả và bộ test hiện có;
   - N8, dùng khối `do-pham-vi` chép ra tệp tạm NGOÀI kho, ở hai chế độ `ma` và `test`, giữa blob nền `1fac6ce` và blob của
     bạn;
   - khối `so-dang-ky`;
   - `python3 -m ruff check --select F` cho hai tệp `.py`, so DELTA với base. Delta phải bằng 0 (xem CLAUDE.md);
   - `git diff --numstat 1fac6ce` dưới trần 450 dòng thêm / 6 tệp. Vượt trần thì DỪNG và báo; không cắt bớt cho vừa.

   Phần không đo được tại chỗ thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do, ví dụ N13–N16 vốn cần CI hoặc exact-H.
4. Vá theo LỚP, đúng ADR-0060 M2 và protocol §8.3. Gặp một lỗi thì khái quát nó thành lớp, quét mọi biểu hiện cùng cơ chế
   trong write set, rồi vá cả lớp, mỗi đường vào có một ca đỏ riêng. Đừng chỉ vá đúng chỗ thấy đầu tiên.
5. Commit cục bộ trên nhánh `claude/wp1466-r8-g1`. Message có hai dòng cuối:
   `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` và
   `Claude-Session: https://claude.ai/code/session_015GtxrcdabvDuhzgezMEE89`.
   KHÔNG viết chuỗi dấu bỏ qua CI (skip + ci trong ngoặc vuông) ở bất kỳ đâu.

## Cấm
- KHÔNG push, KHÔNG mở PR, KHÔNG merge, KHÔNG gọi API ghi của GitHub.
- KHÔNG tự review hay tự approve.
- KHÔNG gọi Codex hay bất kỳ reviewer nào.
- KHÔNG `workflow_dispatch`, KHÔNG sửa `ci.yml`.
- KHÔNG đọc hay ghi secrets (`*.enc`, `tl_secrets*`, `*cookie*`, `*token*`, `credentials*`).
- KHÔNG chạy lệnh có `--apply`, `source-delete`, `reg-delete`, `--clear-stale`.
- KHÔNG ghi ngoài write set. Tệp tạm và log đặt ở thư mục cha của clone (`../out/`), không đặt trong kho.

## Đầu ra bắt buộc
Ghi `../out/HANDOFF.md` theo protocol §7, viết tiếng Việt, gồm:
- head SHA và tree;
- `git diff --numstat 1fac6ce`;
- cách đã giải xung đột;
- bảng N1–N16, mỗi dòng có lệnh, rc, kết quả, hoặc `KHÔNG ĐO ĐƯỢC` kèm lý do;
- ruff delta;
- danh sách lớp lỗi bạn tự phát hiện và đã vá, nếu có;
- những gì chưa đo;
- câu hỏi cần chủ kho quyết, nếu có, mỗi câu kèm mã E1–E5 của ADR-0067.

Kết thúc bằng một dòng tóm tắt: `HEAD=<sha> TEST=<n/n> NUMSTAT=<+a -d> TRAN=<dat|vuot>`.
