# Review mã GIAM-HOI-P2-ADR-E1-E5 r11 g1 — lượt 1 (lời gọi Codex 1/10), reviewer Codex phản biện

Bạn là reviewer độc lập, phiên mới, **chỉ đọc** với kho. Không sửa `cay-kho/`, không commit, không đổi HEAD của `cay-kho/`.
Được ghi trong thư mục `D:/tlx/rv-p2` (ngoài `cay-kho/`), nhất là `scratch/`. Sandbox cấm ghi mọi thư mục tên `.git`: muốn
đột biến bằng Git thì dựng kho riêng có tên khác trong `scratch/`, ví dụ `git clone --bare --shared cay-kho scratch/probe.git`
rồi làm việc trên đó. Không dùng mạng, không đọc `~/.codex`. Ổ đĩa còn ít chỗ (khoảng 1 GB): không tạo bản sao làm việc đầy đủ
của kho. `cay-kho/` là checkout thưa: phần lớn `ops/` và `references/` không có trong cây làm việc, mọi thứ vẫn đọc được bằng
`git show`.

## Vai và mức của lượt này

Packet `GIAM-HOI-P2-ADR-E1-E5` revision 11, generation 1, Packet Issue #1292, lease `giam-hoi-p2-r11-g1-claude` (bản chép ở
`LEASE.yaml`). Packet chạm E5 (tạo chính danh sách đóng E1–E5 và các uỷ quyền) và thuộc lớp `sensitive`. Executor lượt này là
**Claude** (Claude Code CLI, model `claude-fable-5-2`, họ `claude`) theo chỉ đạo chủ kho ghi trong `executor_note` của lease;
hàng `executor` của đặc tả vẫn ghi `codex`. Reviewer có thẩm quyền là chủ kho (`human_audited`). Bạn là lượt Codex phản biện
(họ `openai`, khác họ executor). Verdict của bạn chặn: điều kiện M1 của `ADR-0060` (0 P0–P2 mở; P3 phải được reviewer xác nhận
đóng hoặc chủ kho miễn) xét trên verdict này, chủ kho chỉ audit head mà lượt này approve, và biên nhận của lượt này là đầu vào
K4 đường model của `kiem-merge`.

## Đối tượng

- `cay-kho/` là checkout tách rời ở SHA ứng viên **H = `2b6ff1574dd3d26908eb4bb8c425df87b0ad6d9f`**, base
  `072d45a0595f3d2ff9f0880143a237c9e0ea70c3` (= `origin/master` lúc cấp lease). Cha của H là
  `5b5e6171f81ac8199041d8d569331b0a218860d6`, merge commit của phiên điều phối: cha 1 là `728aaac` (commit rỗng, head hiện tại
  của PR draft #1317, cha `c0b8e11`), cha 2 là base; tree của nó phải bằng tree của base. Kiểm điều ấy, và kiểm `728aaac` không
  đổi tệp nào so với cha của nó.
- Đặc tả: `SPEC-r11.md` (bản chép từ commit `d26151370b9a86eb495457193e1a440e0bbeb764`, nhánh `ops/spec-giam-hoi-p2-r11`;
  không có trong cây của H). sha256 phải là `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9`. Mục 21 nói r11
  khác r10 ở đâu và vì sao (ứng viên r10 làm đỏ `doc-claims-check --strict` của CI).
- Handoff của executor: `HANDOFF-executor.md`. Executor không commit theo chỉ thị; phiên điều phối commit đúng working tree ấy,
  ghi trong thông điệp commit. Handoff ghi ba nhận xét về đặc tả (hàng `executor`, ngày Trạng thái điền trước lúc land, dòng
  Trạng thái trỏ comment ghi hộ): xét chúng như mọi điểm khác.
- Bằng chứng của phiên điều phối: `nghiem-thu-H.txt` (vị từ, A7, A9 trên H), `selftest-H.txt` và `ci-local.txt` khi có.

## Việc

1. **Danh tính:** đo `git rev-parse H H^{tree} H^1 H^1^{tree} H^1^1 H^1^2 <base>^{tree}`, `git diff --numstat <base> H`,
   `git diff --stat 728aaac^ 728aaac` (phải rỗng). Kỳ vọng tree H `54ce5990268114482e2525ed6d331e302d5a5431` và đúng ba tệp
   `.claude/skills/soan-spec/SKILL.md`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`.
   Đo sha256 của `SPEC-r11.md` và so với blob ở commit đặc tả.
2. **Vị từ nghiệm thu:** tự trích khối ```python của mục 4 đặc tả thành `scratch/kiem_p2.py`; chạy từ gốc `cay-kho` với base
   ở trên (vị từ đọc HEAD): phải `ĐẠT` rc 0. Chạy vài đột biến ở cột đột biến của bảng A1–A9 (trong kho riêng ngoài `.git`),
   ghi rc từng ca; ít nhất một ca cho A1, A2, A3, A4, A5 và A9. A9: trong `cay-kho`,
   `python scripts/tl.py doc-claims-check --path docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md --strict --json`
   (kỳ vọng rc 0) và cùng lệnh trên một bản sao ADR trong `scratch/` có lại dấu nháy ngược (kỳ vọng rc 2). Chạy
   `python .claude/dev/packet_loop.py doctrine-scan --root .`, `python .claude/dev/packet_loop.py adr-song --root .`,
   `git diff --check <base> H`.
3. **Hai trục review:**
   - *Spec:* thay đổi có đúng từng byte theo các khối `thay` và khối `adr` của đặc tả r11 không (ba loại chỗ trống của ADR điền
     đúng quy tắc: ngày, `spec_hash`, Issue/URL duyệt băm `https://github.com/ducthangho/tra-luat/issues/1292#issuecomment-6880923050`,
     `{{SO}}`/`{{DONG}}` đo trên base); có gì ngoài write set không.
   - *Standards/Security:* văn bản mới (ADR-0067, các đoạn protocol §2, §12, §13, §20, skill `soan-spec`) có mâu thuẫn protocol
     hiện hành hay ADR đang hiệu lực không; có chỗ nào **lỏng hơn** luật hiện hành mà đặc tả mục 10 không nêu không (đặc biệt:
     uỷ quyền thường trực, tự merge, huỷ lượt không bằng chứng máy, Windows/mutant, E4/E5 không rõ); dòng §20 của `ADR-0067`
     có khai đúng cổng ĐO được ở H không (lời khai "0 cổng" có đúng với `ops/lease_publish.py`, `.claude/dev/packet_loop.py`,
     `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`,
     `.github/workflows/ops-publish-lease.yml` ở H không); mục *Hiệu lực và chuyển tiếp* có khiến văn bản đi trước mã ở chỗ nào
     một agent đọc sẽ hành động sai không. Đặc tả đã được review và chủ kho duyệt băm; lỗi nằm trong văn bản đặc tả quy định thì
     ghi là finding đặc tả (đề xuất revision), không đòi executor sửa khác đặc tả.
4. **Phân loại:** Windows theo `ADR-0060` M3 (kỳ vọng `not_required`: mọi tệp là `*.md`); `full_mutant_audit` theo M9 (kỳ
   vọng không áp). Nếu không đồng ý, chốt kèm lý do.

Khái quát mỗi biểu hiện thành một lớp và quét mọi biểu hiện cùng lớp trên H trước khi báo (`ADR-0060` M2).

## Đầu ra

Ghi `D:/tlx/rv-p2/VERDICT.md`, mở đầu:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 2b6ff1574dd3d26908eb4bb8c425df87b0ad6d9f
reviewed_tree: <tree đo được>
spec_sha256: <đo được>
windows: not_required | required (lý do)
```

rồi bảng lệnh đã chạy kèm rc và dòng kết luận, rồi finding `P2-L1-01`… (mức P0–P3, slug lớp, tệp:dòng, bằng chứng chạy được,
hướng sửa), rồi những gì không đo được. DÒNG CUỐI CÙNG của câu trả lời cuối của bạn (stdout) PHẢI đúng một trong:
`KET_LUAN: approve` · `KET_LUAN: changes_requested` · `KET_LUAN: blocked`. `changes_requested` chỉ khi có P0–P2 có bằng chứng
chạy được.
