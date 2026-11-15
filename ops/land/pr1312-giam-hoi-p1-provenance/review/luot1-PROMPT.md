# Review mã GIAM-HOI-P1-SOAN-SPEC r7 g1 — lượt 1 (lời gọi Codex 1/10), reviewer Codex phản biện bổ sung

Bạn là reviewer độc lập, phiên mới, **chỉ đọc** với kho. Không sửa `cay-kho/`, không commit, không đổi HEAD của `cay-kho/`.
Được ghi trong thư mục hiện tại (ngoài `cay-kho/`), nhất là `scratch/`. Sandbox cấm ghi mọi thư mục tên `.git`: muốn đột biến
bằng Git thì dựng kho riêng có tên khác, ví dụ `git clone --bare cay-kho scratch/probe.git` rồi làm việc trên đó. Không dùng
mạng, không đọc `~/.codex`.

## Vai và mức của lượt này

Packet `GIAM-HOI-P1-SOAN-SPEC` revision 7, generation 1, Packet Issue #1291, lease `giam-hoi-p1-r7-g1-codex` (bản chép ở
`LEASE.yaml`). Executor là Codex (họ `openai`); reviewer có thẩm quyền là chủ kho (`human_audited`). Bạn là lượt Codex phản biện
bổ sung, cùng họ với executor nên mức của bạn là `same_provider_approved`. Verdict của bạn vẫn chặn: điều kiện M1 của `ADR-0060`
(0 P0–P2 mở; P3 phải được reviewer xác nhận đóng hoặc chủ kho miễn) xét trên verdict này, và chủ kho chỉ audit head mà lượt này
approve.

## Đối tượng

- `cay-kho/` là checkout tách rời ở SHA ứng viên **H = `68f4f73c3caae73a6a44be1215050ea8938bac65`**, base
  `6f32aad6fe9db93867fc87456541740f80bf79a4`. Cha của H là `83bbb5f79ebcc0c50fc2301f3bc514fbb5aa8673`, một commit rỗng (tree bằng base) dựng để PR draft mở trước khi H được đẩy, cho chủ kho audit H trên PR trước lượt CI đầu tiên của H (`ADR-0063` K4, đường human). Kiểm commit rỗng ấy không đổi tệp nào. Kho không nông, có `refs/remotes/origin/master`.
- Đặc tả: `cay-kho/ops/specs/GIAM-HOI-P1-SOAN-SPEC-r7.md`, sha256 phải là
  `353048bc4f77b3ed39d73b51c869deea787d8a4bd59477e4b351a840e3cc8bd3`.
- Handoff của executor: `HANDOFF-executor.md` (lượt chạy của executor không tạo được commit vì sandbox cấm ghi `.git`; phiên điều
  phối tạo commit H từ đúng working tree ấy, ghi rõ trong thông điệp commit).
- Bằng chứng của phiên điều phối: `EVIDENCE.md`.

## Việc

1. **Danh tính:** đo `git rev-parse H H^{tree} H^1 H^2`, `git diff --numstat <base> H`, `git diff --stat <base> H^1` (phải rỗng). Kỳ vọng tree
   `9acd42b130ea1acdba31b36a7bb8258d86aca589` và đúng hai tệp `.claude/skills/soan-spec/SKILL.md`,
   `docs/PROTOCOL_DA_PHIEN.md`. Đo sha256 của tệp đặc tả.
2. **Vị từ nghiệm thu:** tự trích khối ```python của mục 4 đặc tả thành `scratch/kiem_p1.py`; chạy từ gốc `cay-kho` với
   `<base>` ở trên (vị từ đọc HEAD): phải `ĐẠT` rc 0. Chạy lại trên base (rc 1) và trên vài đột biến ở cột đột biến của bảng
   A1–A6 trong đặc tả (làm trong kho riêng ngoài `.git`), ghi rc từng ca. Chạy `python .claude/dev/packet_loop.py doctrine-scan
   --root .`, `python .claude/dev/packet_loop.py adr-song --root .`, `git diff --check <base> H`.
3. **Hai trục review:**
   - *Spec:* thay đổi có đúng từng byte theo các khối `thay` của đặc tả không; có gì ngoài write set không.
   - *Standards/Security:* văn bản mới của skill `soan-spec` (dòng khai `ADR-0055`, `ADR-0053`, luật L7, mã E1–E3, mục
     `luat_dung`) có mâu thuẫn protocol hiện hành hay ADR đang hiệu lực không; bốn dòng §20 mới (`ADR-0037`, `ADR-0038`,
     `ADR-0043`, `ADR-0048`) có khai đúng cổng ĐO được trong mã ở H không (tự tìm trong `.claude/dev/packet_loop.py`,
     `ops/lease_publish.py`), có con số trần nào bị chép vào chỗ phải là con trỏ không. Đặc tả đã được review và duyệt; lỗi nằm
     trong văn bản đặc tả quy định thì ghi là finding đặc tả (đề xuất revision), không đòi executor sửa khác đặc tả.
4. **Phân loại:** Windows theo `ADR-0060` M3 (kỳ vọng `not_required`: mọi tệp là `*.md`); `full_mutant_audit` theo M9 (kỳ vọng
   không áp). Nếu không đồng ý, chốt kèm lý do.

Khái quát mỗi biểu hiện thành một lớp và quét mọi biểu hiện cùng lớp trên H trước khi báo (`ADR-0060` M2).

## Đầu ra

Ghi `VERDICT.md`, mở đầu:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 68f4f73c3caae73a6a44be1215050ea8938bac65
reviewed_tree: <tree đo được>
spec_sha256: <đo được>
windows: not_required | required (lý do)
```

rồi bảng lệnh đã chạy kèm rc và dòng kết luận, rồi finding `P1-L1-01`… (mức P0–P3, slug lớp, tệp:dòng, bằng chứng chạy được,
hướng sửa), rồi những gì không đo được. DÒNG CUỐI CÙNG của câu trả lời cuối của bạn (stdout) PHẢI đúng một trong:
`KET_LUAN: approve` · `KET_LUAN: changes_requested` · `KET_LUAN: blocked`. `changes_requested` chỉ khi có P0–P2 có bằng chứng
chạy được.
