# Executor wp1466 (#1466), lượt 2: Claude Fable 5.2, effort high

Đây là lượt 2, tiếp theo phiên của bạn ở lượt 1. Thư mục hiện tại vẫn là clone `kho/`. Mọi trao đổi viết tiếng Việt.

## Đã đổi so với lượt 1
- Chủ kho đã quyết hai câu bạn hỏi trong handoff lượt 1. Ghi hộ ở #1466, issuecomment-7191469520:
  - **Q0 (E3), "Ra đặc tả r9".** Bảng §1.1 bỏ backtick ở cả 18 con trỏ `ca:`. Đoạn dẫn của bảng có thêm một câu luật. Băm `K01` đổi.
  - **Q2 (E5), "Giữ bản vá".** Luật "phần đầu tệp" do bạn tự vá ở lượt 1 nay thành hợp đồng, nằm ở mục 8.3 của đặc tả r9.
- **Q1 đã đóng bằng phép đo.** REST trả `created_at` của issuecomment-7058374374 là `2026-11-21T06:05:55Z`, nên ngày `2026-11-21` trong ADR-0068 là đúng.
- **Q3 chưa quyết.** Đừng làm gì cho Q3 ở lượt này.
- **Đặc tả r9 đã trên master**, qua PR #1550, merge `695916ea3bfffdd7b2e8fcb94b0740b3c421fe70`. Hai lượt review đều sạch:
  - Codex review đặc tả lượt 9: approve, 0 finding P0–P3.
  - Connector GitHub: sạch.
- **Lease mới: `wp1466-r9-g2-claude`**, trên nhánh `origin/ops/wp1466-r9-g2-lease`, commit `c9a7a98`. Lease này thay g1.
  - Base: `695916e`.
  - Nhánh làm việc: `claude/wp1466-r9-g2`.
  - Write set: giữ nguyên bốn tệp.
  - Đọc lease bằng: `git fetch origin ops/wp1466-r9-g2-lease && git show FETCH_HEAD:ops/leases/wp1466-r9-g2-claude.yaml`.

## Kiểm đầu tiên
1. `git fetch origin master`. Kiểm `origin/master` chứa `695916e`.
2. Kiểm `git show 695916e:ops/specs/wp1466.md | sha256sum` ra đúng `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c`. Lệch thì DỪNG và báo.
3. Kiểm bốn tệp của write set giống nhau giữa `1fac6ce` và `695916e`, tức `git diff` rỗng.

## Chỉ thị của chủ kho, bắt buộc từ lượt này
Đọc NGUYÊN VĂN các tệp sau, đừng dựa trí nhớ:
- `.claude/skills/work-packet/SKILL.md`;
- `docs/PROTOCOL_DA_PHIEN.md`, nhất là §7, §8, §8.3 và §12;
- `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`, đọc đủ M1–M12;
- ADR-0062 và ADR-0063.

Tóm tắt dưới đây không thay bản gốc:
- **Vá theo LỚP, không vá theo từng dòng bị chỉ** (§8.3).
  - Trước khi vá, tự liệt kê MỌI đường vào của lớp.
  - Đóng cả lớp bằng một thay đổi chung.
  - Mỗi đường vào có một ca khoá và một đột biến riêng.
  - Nếu vá riêng một biểu hiện thì ghi lý do cơ chế.
- **Đóng lớp.** Một lớp chỉ được ghi là đã vá khi đủ ba điều kiện:
  - mọi biểu hiện trong phạm vi đã đóng;
  - bản vá không sinh biểu hiện mới cùng cơ chế;
  - không còn phần chưa đo.

  Thiếu quan sát, cắt acceptance hay đẩy ra ngoài scope KHÔNG tính là vá. Cấm gộp slug hay đổi hạng để giảm số lớp.
- **Không tự ghi nợ.** P3 chỉ được miễn bằng comment của chủ kho có dòng `mien_p3`. P2 bắt buộc vá.
- **§12.** Nếu cùng một lớp lặp từ 3 lần trở lên thì DỪNG và hỏi.
- **Khai đủ đầu vào cho mọi cổng, và đo lại.** Không tin `rc`; đòi bằng chứng dương, ví dụ `N/N` với hai số bằng nhau, hay `"ok": true`.

## Việc
1. Tạo nhánh `claude/wp1466-r9-g2` từ `origin/master` (`695916e`). Đưa commit lượt 1 `96e4472` lên bằng `git cherry-pick 96e4472`. Ghi kết quả vào handoff; nếu xung đột thì nói rõ đã giải thế nào.
2. Sửa cho khớp đặc tả r9. Đặc tả là nguồn sự thật, xem mục 0 đoạn *Revision 9* và mục 8.3:
   - Bảng §1.1 trong `docs/PROTOCOL_DA_PHIEN.md` phải bằng từng byte nội dung khối `p2-moi` của r9.
   - Hằng `INV_KHOA_PROTOCOL` của `K01` phải bằng khối `khoa` của r9: băm đơn vị `987f952747e26847a5a8e39dd82bf09da72d508dd3e03cef3bfdd42db4e381c5`.
   - Fixture hay ca nào ghi cứng băm hoặc nội dung cũ của `K01` cũng phải khớp lại.

   Hồ sơ dựng máy r9 nằm ở `ops/specs/wp1466/r9/`. Bạn có thể đọc, nhưng hãy tự kiểm.
3. **Cách ghi vào `.claude/dev/*.py`.** Viết bản vá thành tệp patch ở `../out/`, rồi áp bằng `git apply`.
   - KHÔNG dùng `git hash-object -w`, `git update-index --cacheinfo` hay `git checkout-index` để đưa nội dung vào cây. Đó là đường vòng qua chốt của harness mà lượt 1 đã dùng; chủ kho sẽ xét lại đường đó, và lượt này không được dùng lại.
   - Nếu `git apply` cũng bị chặn thì DỪNG, ghi rõ vào handoff rồi thoát. Đừng tìm đường khác.
4. Đo lại MỌI tiêu chí N1–N16 đo được tại chỗ trên H mới. Dùng đúng cách và các script đã dựng ở lượt 1 trong `../out/sc/`. Mỗi tiêu chí ghi lệnh, rc và output. Tối thiểu gồm:
   - `python3 scripts/tl.py doc-claims-check --strict --json`. Đòi `"ok": true`, và mảng `flags` rỗng, trên clone sạch của H mới.
   - `doctrine-scan`, `adr-song`.
   - N5: tự băm độc lập.
   - N6 và N7 trên bộ test: tập bắt buộc, cộng ba ca và ba đột biến "phần đầu tệp".
   - N8, cả hai chế độ, so với blob nền `695916e`.
   - `so-dang-ky`.
   - ruff F: delta so với base phải bằng 0.
   - `git diff --numstat 695916e`: tối đa 450 dòng thêm và tối đa 6 tệp.
   - `tl --selftest` N/N.
   - Bộ test đầy đủ theo 16 mảnh và job gom, đúng như lượt 1.

   **Giới hạn thời gian.** Tác vụ nền bị cắt ở 2 giờ. Ở lượt 1, `run-l1.json` bị mất vì bị cắt. Lượt này hãy dồn phép đo cho xong trong khoảng 100 phút:
   - phần nặng chạy song song khi máy cho phép;
   - ghi handoff SỚM, rồi cập nhật dần.
5. Vá theo lớp nếu bạn tự phát hiện lớp mới, đúng chỉ thị ở trên. Nếu một lớp cần đổi đặc tả thì KHÔNG vá; DỪNG và hỏi kèm mã E.
6. Commit cục bộ trên `claude/wp1466-r9-g2`.
   - Có thể là một commit cherry-pick cộng một commit sửa, hoặc gộp lại; nói rõ trong handoff bạn chọn cách nào.
   - Hai dòng cuối của message: `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` và `Claude-Session: https://claude.ai/code/session_015GtxrcdabvDuhzgezMEE89`.
   - KHÔNG viết chuỗi dấu bỏ qua CI, tức "skip" cộng "ci" trong ngoặc vuông.

## Cấm
Giữ nguyên các mục cấm của lượt 1:
- không push, không PR, không merge, không API ghi;
- không tự review, không gọi reviewer;
- không `workflow_dispatch`, không sửa `ci.yml`;
- không đụng secrets;
- không chạy lệnh có `--apply`, `source-delete`, `reg-delete`, `--clear-stale`;
- không ghi ngoài write set; tệp tạm để ở `../out/`.

Cấm thêm: không dùng các lệnh git plumbing ở mục Việc 3 để ghi vào cây.

## Đầu ra
Ghi `../out/HANDOFF-l2.md` theo §7, viết tiếng Việt:
- head SHA và tree;
- numstat;
- cách đưa lượt 1 lên base mới;
- bảng N1–N16;
- ruff delta;
- `doc-claims-check`;
- lớp lỗi tự phát hiện, nếu có;
- những gì chưa đo;
- câu hỏi cho chủ kho, mỗi câu kèm mã E.

Không để trống ô nào: ô chưa đo thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do. Kết thúc bằng một dòng `HEAD=<sha> TEST=<n/n> NUMSTAT=<+a -d> TRAN=<dat|vuot> DOC_CLAIMS=<ok|do>`.
