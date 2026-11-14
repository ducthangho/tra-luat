# Giao việc executor — GIAM-HOI-P2-ADR-E1-E5 r10 g1 (Codex)

Bạn là **executor** Codex của packet `GIAM-HOI-P2-ADR-E1-E5`, revision 10, generation 1, Packet Issue #1292, lease
`giam-hoi-p2-r10-g1-codex` (`ops/leases/giam-hoi-p2-r10-g1-codex.yaml` trên nhánh `ops/giam-hoi-p2-lease`). Reviewer có
thẩm quyền của packet là chủ kho (`human_audited`); một lượt Codex khác, phiên mới, sẽ phản biện sau bạn. Bạn không review,
không approve, không merge.

## Đọc trước

1. `docs/PROTOCOL_DA_PHIEN.md`: §3.2.1, §4, §5, §7, §10.2, §12, §13.
2. `.agents/skills/work-packet/SKILL.md` (adapter Codex: cú pháp và công cụ).
3. Đặc tả `ops/specs/GIAM-HOI-P2-ADR-E1-E5-r10.md`. Đo sha256 của chính tệp trong checkout; phải bằng
   `1a5786cca5bcf8a72d8d93ecb9f8edbfbe021c5ef69b68f78ac642bc15698d1f`. Khác thì dừng.

## Phạm vi

- Thư mục làm việc là một clone riêng, đang ở nhánh `agent/giam-hoi-p2-g1-codex` tại base
  `c0b8e11d7099f756e65db8bd9a81493cde789a6f` (chứa commit land `bab2279` của `GIAM-HOI-P1-SOAN-SPEC` r7). Thư mục ghi nháp
  ngoài checkout được cấp bằng `--add-dir`; mọi tệp nháp (vị từ trích ra, log, handoff) để ở đó, không để trong checkout.
- Write set đúng ba tệp: `.claude/skills/soan-spec/SKILL.md`, `docs/PROTOCOL_DA_PHIEN.md` và tệp mới
  `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`. Không sửa tệp nào khác.
- Không đổi nhánh, không commit, không push, không gọi GitHub, không dùng mạng. Sandbox Codex trên máy này cấm ghi thư mục
  `.git`, nên phiên điều phối sẽ commit đúng working tree bạn để lại và ghi việc ấy trong thông điệp commit. Không chạy
  `packet_loop.py init`, `begin-attempt` hay lệnh ghi state nào: packet này không dùng state của `packet_loop.py` (hàng
  `executor` của đặc tả).

## Việc

1. Áp đúng các khối `thay` của mục 2 đặc tả cho `PROTOCOL_DA_PHIEN.md` và `SKILL.md`: mỗi khối `cu` trên base thay bằng
   khối `moi` tương ứng, giữ nguyên từng byte (LF, không thêm khoảng trắng cuối dòng). Không viết lại câu chữ, kể cả khi bạn
   thấy chỗ nên sửa: ghi nó vào handoff.
2. Tạo tệp ADR bằng đúng từng byte khối `adr` của mục 2, chỉ thay ba loại chỗ trống theo quy tắc ngay trên khối ấy:
   - `{{TRANG_THAI}}`: ngày là `2026-11-14` (ngày land dự kiến do phiên điều phối chọn), `spec_hash` là sha256 bạn đo ở
     bước Đọc trước, Issue `#1292`, URL `https://github.com/ducthangho/tra-luat/issues/1292#issuecomment-6730487484`
     (comment chủ kho duyệt băm r10).
   - `{{SO}}`, `{{DONG}}`: tự đo trên base bằng đúng lệnh in trên mỗi dòng (`git show <base>:<tệp> | grep -c 'ADR-0067'` và số
     ký tự xuống dòng của tệp). Ghi lệnh và số đo vào handoff.
3. Trích khối ```python của mục 4 đặc tả thành `kiem_p2.py` trong thư mục nháp. Vị từ đọc `HEAD` nên chỉ chạy được sau khi
   phiên điều phối commit; bạn không chạy nó, chỉ ghi sha256 của tệp trích ra vào handoff.
4. Chạy và ghi rc thật (các lệnh này đọc working tree): `python .claude/dev/packet_loop.py doctrine-scan --root .`,
   `python .claude/dev/packet_loop.py adr-song --root .`, `git diff --check`, `git status --short`, `git diff --numstat`
   (số dòng của tệp ADR mới đo bằng `wc -l`). A8 (`python scripts/tl.py --selftest`) do phiên điều phối chạy trên đúng SHA
   sẽ đẩy; bạn không chạy nó.
5. Ghi `HANDOFF.md` trong thư mục nháp: base, các tệp đã đổi kèm số dòng, từng lệnh đã chạy kèm rc và dòng kết luận, sha256
   đặc tả đã đo, sha256 `kiem_p2.py`, số đo `{{SO}}`/`{{DONG}}`, những gì không làm hoặc không đo được, và mọi chỗ bạn thấy
   đặc tả có vấn đề.

## Khi nào dừng

- Khối `cu` nào không có đúng một lần trên base, `docs/adr/0067-*` đã có trên base, hay sha256 đặc tả không khớp: dừng,
  không tự sửa, ghi lý do vào handoff.
- `doctrine-scan` hay `adr-song` khác rc 0 sau khi đã áp đủ: đọc thông báo, sửa phần áp sai của chính bạn; nếu thông báo chỉ
  ra lỗi của đặc tả thì dừng và ghi vào handoff (đặc tả cần revision; mục 5 của đặc tả).
