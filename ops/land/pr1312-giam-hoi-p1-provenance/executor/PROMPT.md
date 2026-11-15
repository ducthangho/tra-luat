# Giao việc executor — GIAM-HOI-P1-SOAN-SPEC r7 g1 (Codex)

Bạn là **executor** Codex của packet `GIAM-HOI-P1-SOAN-SPEC`, revision 7, generation 1, Packet Issue #1291, lease
`giam-hoi-p1-r7-g1-codex` (`ops/leases/giam-hoi-p1-r7-g1-codex.yaml` trên nhánh `ops/giam-hoi-p1-lease`). Reviewer có thẩm
quyền của packet là chủ kho (`human_audited`); một lượt Codex khác, phiên mới, sẽ phản biện sau bạn. Bạn không review, không
approve, không merge.

## Đọc trước

1. `docs/PROTOCOL_DA_PHIEN.md`: §3.2.1, §4, §5, §7, §10.2, §12, §13.
2. `.agents/skills/work-packet/SKILL.md` (adapter Codex: cú pháp và công cụ).
3. Đặc tả `ops/specs/GIAM-HOI-P1-SOAN-SPEC-r7.md`. Đo sha256 của chính tệp trong checkout; phải bằng
   `353048bc4f77b3ed39d73b51c869deea787d8a4bd59477e4b351a840e3cc8bd3`. Khác thì dừng.

## Phạm vi

- Thư mục làm việc là một clone riêng, đang ở nhánh `agent/giam-hoi-p1-g1-codex` tại base
  `6f32aad6fe9db93867fc87456541740f80bf79a4`. Thư mục ghi nháp ngoài checkout được cấp bằng `--add-dir`; mọi tệp nháp
  (vị từ trích ra, log, handoff) để ở đó, không để trong checkout.
- Write set đúng hai tệp: `.claude/skills/soan-spec/SKILL.md` và `docs/PROTOCOL_DA_PHIEN.md`. Không sửa tệp nào khác.
- Không đổi nhánh, không push, không gọi GitHub, không dùng mạng. Không chạy `packet_loop.py init`, `begin-attempt` hay lệnh
  ghi state nào: packet này không dùng state của `packet_loop.py` (hàng `executor` của đặc tả).

## Việc

1. Áp đúng các khối `thay` của mục 2 đặc tả: mỗi khối `cu` trên base thay bằng khối `moi` tương ứng, giữ nguyên từng byte
   (LF, không thêm khoảng trắng cuối dòng). Không viết lại câu chữ, kể cả khi bạn thấy chỗ nên sửa: ghi nó vào handoff.
2. Trích khối ```python của mục 4 đặc tả thành `kiem_p1.py` trong thư mục nháp, rồi chạy, từ gốc checkout:
   `python <nháp>/kiem_p1.py ops/specs/GIAM-HOI-P1-SOAN-SPEC-r7.md 6f32aad6fe9db93867fc87456541740f80bf79a4`
   sau khi commit (vị từ đọc `HEAD`). Phải ra `ĐẠT`, rc 0.
3. Chạy và ghi rc thật: `python .claude/dev/packet_loop.py doctrine-scan --root .`,
   `python .claude/dev/packet_loop.py adr-song --root .`, `git diff --check 6f32aad6fe9db93867fc87456541740f80bf79a4 HEAD`.
   A6 (`python scripts/tl.py --selftest`) do phiên điều phối chạy trên đúng SHA của bạn; bạn không chạy nó.
4. Một commit trên nhánh hiện tại. Thông điệp: dòng đầu `GIAM-HOI-P1-SOAN-SPEC r7 g1: skill soan-spec mặc định trần
   ADR-0055, L7, cột cổng §20`; thân nêu Issue #1291 và sha256 đặc tả.
5. Ghi `HANDOFF.md` trong thư mục nháp: SHA H và tree của commit, base, `git diff --numstat` so base, từng lệnh đã chạy kèm rc
   và dòng kết luận, sha256 đặc tả đã đo, những gì không làm hoặc không đo được, và mọi chỗ bạn thấy đặc tả có vấn đề.

## Khi nào dừng

- Khối `cu` nào không có đúng một lần trên base, vị từ trả rc 3, hay sha256 đặc tả không khớp: dừng, không tự sửa, ghi lý do
  vào handoff.
- Vị từ trả rc 1 sau khi đã áp đủ khối: đọc thông báo, sửa phần áp sai của chính bạn; nếu thông báo chỉ ra lỗi của đặc tả thì
  dừng và ghi vào handoff.
