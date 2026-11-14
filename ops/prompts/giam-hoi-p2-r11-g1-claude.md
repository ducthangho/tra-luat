# Giao việc executor — GIAM-HOI-P2-ADR-E1-E5 r11 g1 (Claude)

Bạn là **executor** Claude (Claude Code CLI, model `claude-fable-5-2`) của packet `GIAM-HOI-P2-ADR-E1-E5`, revision 11, generation 1, Packet Issue #1292, lease
`giam-hoi-p2-r11-g1-claude` (`ops/leases/giam-hoi-p2-r11-g1-claude.yaml` trên nhánh `ops/giam-hoi-p2-lease`). Reviewer có
thẩm quyền của packet là chủ kho (`human_audited`); một lượt Codex, phiên mới, sẽ phản biện sau bạn. Bạn không review,
không approve, không merge.

## Đọc trước

1. `docs/PROTOCOL_DA_PHIEN.md`: §3.2.1, §4, §5, §7, §10.2, §12, §13.
2. `.claude/skills/work-packet/SKILL.md` (adapter Claude: cú pháp và công cụ).
3. Đặc tả `ops/specs/GIAM-HOI-P2-ADR-E1-E5-r11.md`. Tệp KHÔNG nằm trong checkout: nó ở commit
   `d26151370b9a86eb495457193e1a440e0bbeb764` (ref `origin/ops/spec-giam-hoi-p2-r11`); đọc bằng
   `git show d26151370b9a86eb495457193e1a440e0bbeb764:ops/specs/GIAM-HOI-P2-ADR-E1-E5-r11.md` và chép ra thư mục nháp. Đo
   sha256 của byte thô; phải bằng `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9`. Khác thì dừng. Mục 21
   của đặc tả nói r11 khác r10 ở đâu.

## Phạm vi

- Thư mục làm việc là một clone riêng, đang ở nhánh `agent/giam-hoi-p2-g1-codex`, HEAD
  `5b5e6171f81ac8199041d8d569331b0a218860d6`: merge commit của phiên điều phối, cha 1 là head rỗng của PR #1317, cha 2 là base
  `072d45a0595f3d2ff9f0880143a237c9e0ea70c3` (= `origin/master` lúc cấp lease, chứa commit land `bab2279` của
  `GIAM-HOI-P1-SOAN-SPEC` r7); tree của HEAD bằng tree của base. Mọi phép đo "trên base" dùng OID base này. Thư mục ghi nháp
  ngoài checkout được cấp bằng `--add-dir`; mọi tệp nháp (vị từ trích ra, log, handoff) để ở đó, không để trong checkout.
- Write set đúng ba tệp: `.claude/skills/soan-spec/SKILL.md`, `docs/PROTOCOL_DA_PHIEN.md` và tệp mới
  `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`. Không sửa tệp nào khác.
- Không đổi nhánh, không commit, không push, không gọi GitHub, không dùng mạng. Phiên điều phối sẽ commit đúng working tree
  bạn để lại và ghi việc ấy trong thông điệp commit, như các lượt thi công trước của lộ trình. Không chạy
  `packet_loop.py init`, `begin-attempt` hay lệnh ghi state nào: packet này không dùng state của `packet_loop.py` (hàng
  `executor` của đặc tả).

## Việc

1. Áp đúng các khối `thay` của mục 2 đặc tả cho `PROTOCOL_DA_PHIEN.md` và `SKILL.md`: mỗi khối `cu` trên base thay bằng
   khối `moi` tương ứng, giữ nguyên từng byte (LF, không thêm khoảng trắng cuối dòng). Không viết lại câu chữ, kể cả khi bạn
   thấy chỗ nên sửa: ghi nó vào handoff.
2. Tạo tệp ADR bằng đúng từng byte khối `adr` của mục 2, chỉ thay ba loại chỗ trống theo quy tắc ngay trên khối ấy:
   - `{{TRANG_THAI}}`: ngày là `2026-11-15` (ngày land dự kiến do phiên điều phối chọn), `spec_hash` là sha256 bạn đo ở
     bước Đọc trước, Issue `#1292`, URL `https://github.com/ducthangho/tra-luat/issues/1292#issuecomment-6880923050`
     (comment chủ kho duyệt băm r11).
   - `{{SO}}`, `{{DONG}}`: tự đo trên base bằng đúng lệnh in trên mỗi dòng (`git show <base>:<tệp> | grep -c 'ADR-0067'` và số
     ký tự xuống dòng của tệp). Ghi lệnh và số đo vào handoff.
3. Trích khối ```python của mục 4 đặc tả thành `kiem_p2.py` trong thư mục nháp. Vị từ đọc `HEAD` nên chỉ chạy được sau khi
   phiên điều phối commit; bạn không chạy nó, chỉ ghi sha256 của tệp trích ra vào handoff.
4. Chạy và ghi rc thật (các lệnh này đọc working tree): `python .claude/dev/packet_loop.py doctrine-scan --root .`,
   `python .claude/dev/packet_loop.py adr-song --root .`, `python scripts/tl.py doc-claims-check --strict --json` (A9),
   `git diff --check`, `git status --short`, `git diff --numstat`
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
