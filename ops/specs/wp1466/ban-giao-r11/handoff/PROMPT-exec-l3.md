# Executor wp1466 (#1466), lượt 3: Claude Fable 5.2, effort high — sửa ĐÚNG MỘT dòng ADR

Bạn là EXECUTOR của packet `wp1466`, làm trong kho `ducthangho/tra-luat`. Mọi trao đổi viết tiếng Việt.

Đây là phiên MỚI. Lượt 1 và lượt 2 chạy ở phiên khác; hồ sơ của chúng nằm ở `../out/HANDOFF.md` và `../out/HANDOFF-l2.md`.

Bạn làm việc trong clone `kho/` (thư mục hiện tại), nhánh `claude/wp1466-r9-g2`. HEAD lúc bắt đầu phải là
`d5d96e709e37979986d75742edf0fb9942c18b61`. Nếu khác thì DỪNG và báo.

## Thẩm quyền
- **Lease.** `wp1466-r9-g2-claude`, trên nhánh `origin/ops/wp1466-r9-g2-lease`, commit `c9a7a98`.
  - base: `695916e`.
  - write set: bốn tệp; lượt này chỉ được chạm `docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md`.
- **Đặc tả r9 trên master.** Kiểm `git show 695916e:ops/specs/wp1466.md | sha256sum` ra đúng
  `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c`. Đọc mục 8.1 của đặc tả: quy tắc của dòng Trạng thái.
- **Quyết định Q4 (E5) của chủ kho: "Dẫn r9".** Đã ghi hộ ở #1466, issuecomment-7200558474. Ngày UTC của comment duyệt băm r9
  (`issuecomment-7192181084`) đã đo bằng REST: `created_at = 2026-11-26T12:34:36Z`.

## Việc
1. Dòng 3 của ADR-0068 hiện là:
   ``- **Trạng thái:** Accepted (2026-11-21, chủ kho `ducthangho` duyệt `spec_hash` `98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834` của đặc tả `wp1466` r8 trên Issue #1466: https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058374374)``

   Đổi thành:
   ``- **Trạng thái:** Accepted (2026-11-26, chủ kho `ducthangho` duyệt `spec_hash` `28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c` của đặc tả `wp1466` r9 trên Issue #1466: https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7192181084)``

   Không đổi byte nào khác.
2. **Cách ghi.** Dựng một tệp patch ở `../out/l3/`, rồi áp bằng `git apply`. KHÔNG dùng `git hash-object -w`, `git update-index --cacheinfo`
   hay `git checkout-index`. Nếu `git apply` bị chặn thì DỪNG và báo.
3. **Đo lại trên commit mới.** Mỗi phép đo ghi lệnh, rc và output vào `../out/log/l3-*.log`. Dùng đúng các script đã dựng ở `../out/sc/`
   (xem `../out/HANDOFF-l2.md`, mục 5):
   - N1: `python3 -I -B ../out/sc/do_adr.py . <HEAD mới> so` phải ĐẠT với khối `adr` của r9. Ngày, băm, `r9` và URL phải khớp quy tắc 8.1.
   - Trên một clone SẠCH của HEAD mới, đặt ở `../out/ve4/h`, ghim `core.abbrev 7`, chạy:
     - `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`
     - `python3 -B .claude/dev/packet_loop.py adr-song --root .`
     - `python3 -B scripts/tl.py doc-claims-check --strict --json`. Yêu cầu `"ok": true` và `flags` rỗng.
   - `git diff --numstat 695916e HEAD`: tối đa 450 dòng thêm, tối đa 6 tệp.
   - `git diff d5d96e7 HEAD` chỉ được có đúng một dòng đổi, nằm ở tệp ADR.
4. **Commit cục bộ.** Message tiếng Việt, hai dòng cuối là
   `Co-Authored-By: Claude Fable 5.2 <noreply@anthropic.com>` và
   `Claude-Session: https://claude.ai/code/session_015GtxrcdabvDuhzgezMEE89`.
   KHÔNG viết chuỗi dấu bỏ qua CI (skip + ci trong ngoặc vuông).

## Chỉ thị bắt buộc của chủ kho
- Vá theo lớp (ADR-0060, protocol §8.3).
- Không tự ghi nợ.
- Khai đủ đầu vào cho cổng và đòi bằng chứng dương. Đừng tin rc.

Nếu khi sửa bạn thấy một chỗ khác trong write set cũng dẫn lần duyệt r8 mà lẽ ra phải dẫn r9, ĐỪNG sửa. Ghi nó vào handoff thành câu hỏi kèm mã E.
Lượt này chỉ sửa đúng một dòng.

## Cấm
- Không push, PR, merge, hay gọi API ghi.
- Không tự review, không gọi reviewer.
- Không `workflow_dispatch`, không sửa `ci.yml`.
- Không đụng secrets.
- Không chạy lệnh có `--apply`, `source-delete`, `reg-delete`, `--clear-stale`.
- Không ghi ngoài tệp ADR. Tệp tạm để ở `../out/`.

## Đầu ra
Ghi `../out/HANDOFF-l3.md` theo §7, gồm:
- head SHA và tree;
- diff một dòng;
- bảng phép đo;
- những gì chưa đo;
- câu hỏi, nếu có.

Kết thúc bằng một dòng: `HEAD=<sha> N1=<dat|khong> DOC_CLAIMS=<ok|do> DOCTRINE=<rc> ADR_SONG=<rc> NUMSTAT=<+a -d>`.
