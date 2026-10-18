# Cross-review độc lập — PR #787 (bookkeeping hồ sơ land pr772-wp766), lượt 2

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao tại `KHO=/home/user/rv773`, detached ở exact head.
- Exact head: `ab4cd428f5a01d69ead7825108593f1092fe78fd` (nhánh `claude/bookkeeping-772-nguon`, PR #787).
- Base: `653fef3`; master hiện `d347d42` (merge sạch). Diff toàn PR: `git -C KHO diff 653fef3 ab4cd42`; vá lượt 1:
  `git -C KHO diff fafbe15 ab4cd42`. Lượt 1 sửa 3 tệp:
  `ops/land/pr772-wp766-land-evidence.yaml`, `ops/land/pr772-wp766-provenance/SHA256SUMS`,
  `ops/land/pr772-wp766-provenance/do-tree-merge-e03d4bf.txt` (mới).
- Đọc thông điệp commit: `git -C KHO show -s fafbe15 ab4cd42`.

## Lượt 1

`VERDICT-luot1.md` trong thư mục ra: P3=1 — `sua_gate_master.do_sau_sua` chỉ phân giải được `RELEASE_MANIFEST.json`
(đầu vào, không phải kết quả). Vá `ab4cd42`: đo lại ba lệnh trên bản sao tách riêng detached ở `1a433a6`, lưu transcript +
ba đầu ra đầy đủ ở `ops/land/pr772-wp766-provenance/do-lai-sau-sua-1a433a6/`, trỏ lời khai vào transcript, SHA256SUMS +4.
Kiểm: vá đóng thật (đầu ra có đúng là của cây `1a433a6`? số khớp lời khai? transcript có tự khai quá phép đo không — vd
"cây không đổi", mục `--ignored` chỉ đo SAU), có mở lỗ mới không (đường dẫn tuyệt đối trong JSON, kích thước, tệp không
ghi SHA). Bạn có thể tự tái đo trên bản sao tạm: `git -C KHO worktree` bị CẤM (KHO read-only) — dùng
`git -C KHO archive 1a433a6 | tar -x -C <tạm>` rồi chạy trong `<tạm>` (selftest ~3–5 phút); không bắt buộc nếu đối
chiếu được bằng cách khác. Rồi soi lại toàn bộ.

## Bối cảnh

Packet #773 thêm bộ kiểm `ops/land_evidence_nguon.py` (PR #778, head `0f4830f`, có trong `KHO`): lời khai `measured` trong
hồ sơ land phải trỏ một token tệp nguồn phân giải được (L1). Hồ sơ `pr772-wp766` vào master SAU ảnh chụp miễn trừ nên bị
đo, và đỏ 4×L1. PR #787 chỉ gắn con trỏ nguồn cho 4 lời khai, cộng một tệp đo mới cho lời khai `khong_xung_dot`. Mục đích:
4 lời khai vẫn ĐÚNG sự thật và mỗi con trỏ trỏ ĐÚNG tệp chứng minh nó — không phải chỉ để qua cổng.

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. Chạy bộ kiểm của #778 trên cây #787:
   `git -C KHO show 0f4830f:ops/land_evidence_nguon.py > /tmp/len.py` rồi
   `cd KHO && python3.13 -B /tmp/len.py --root KHO` (đòi `TỔNG: ĐẠT`, 0 vi phạm) và đối chứng trên `653fef3`
   (`git -C KHO archive 653fef3 ops | tar -x -C <tạm>`; `--root <tạm>` ⇒ 4×L1 trong hồ sơ pr772).
2. Từng con trỏ trỏ đúng tệp chứng minh lời khai chưa? Mở chính tệp được trỏ và đối chiếu số liệu:
   - `spec.nguon` → `ops/specs/wp766.md`: sha256 `da3095b4…` và blob `2176dd0c…` có khớp tệp ấy trong lịch sử (vd
     `git -C KHO show 701f41c:ops/specs/wp766.md | sha256sum`, `git -C KHO rev-parse 701f41c:ops/specs/wp766.md`)?
     Lưu ý: token có phân giải tới tệp trên CÂY hiện tại không — và nếu tệp ấy trên cây khác blob lịch sử thì con trỏ
     có gây hiểu sai không?
   - `khong_xung_dot` → `do-tree-merge-e03d4bf.txt`: tự chạy lại ba lệnh trong tệp trên `KHO` và so; đối chiếu
     `readback-pr-772.json` (base, merge_commit_sha).
   - `codex_connector` → `readback-codex-connector-772.json`: commit 701f41c, completed, không finding, mốc trước merged_at?
   - `human_audit` → `readback-comment-6209427062.json`: tác giả, author_association, app.
3. `SHA256SUMS`: `cd KHO/ops/land/pr772-wp766-provenance && sha256sum -c SHA256SUMS` — đủ dòng, khớp hết, có tệp nào
   trong thư mục KHÔNG có dòng không?
4. Có lời khai nào đổi NGHĨA (không chỉ thêm con trỏ) không? Có token nào phân giải được chỉ vì trùng tên tình cờ
   (vd tên tệp chung chung tồn tại ở `ops/land/` hoặc gốc kho)? Đầu tệp đo mới ghi "kho tại master 653fef3" — có đúng/đo
   được không?
5. Hồ sơ còn lời khai `measured` nào khác mà token phân giải được nhưng trỏ SAI tệp (qua cổng mà không đúng)? Đây là
   phạm vi review: PR này tự nhận làm cho hồ sơ đúng.

**NGƯỠNG: chủ kho đòi hết P1, P2 VÀ P3.** Approve chỉ khi P1=0, P2=0, P3=0. Báo đủ mọi P3 thật đo được, đừng thổi phồng:
thứ ngoài phạm vi ghi ở mục riêng, không tính P3.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: ab4cd428f5a01d69ead7825108593f1092fe78fd`
- Dòng hai: `Verdict: approve` hoặc `Verdict: request_changes`, kèm `P1=a P2=b P3=c`.
- Mỗi finding: mức, tệp:dòng, mô tả, lệnh tái hiện và đầu ra đo được, đề xuất sửa.
- Mục "Đã đo" liệt kê các lệnh đã chạy và kết quả chính; mục "Ngoài phạm vi".
