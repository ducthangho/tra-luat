# DON-REF-DO-TAG-LUU-TRU r1 — cross-review Codex offline (4/10 lời gọi): approve

Đặc tả `ops/specs/don-ref-do-tag-luu-tru-r1.md` sha256 `7ae7733c3adf8cba87ddc7f2d8b85af215f20a5a92b5d90c241733fe2198e160`,
spec_ref `refs/heads/ops/don-ref-do-tag-luu-tru-spec@9836bf89fa55a0803be840da8922e2b1c31af1c5`; lease
`ops/leases/don-ref-do-tag-luu-tru-r1-g1-claude.yaml`; Issue #1532. Verdict nguyên văn từng lượt nằm trên Issue.

| lượt | run `launcher.py run` | head review | kết luận | comment Issue #1532 |
|---|---|---|---|---|
| 1 | `d8400a5b`, 276 s, `ma_thoat` 0 | `f5f24a3ed6f80beb863725788050d7a6630fcd85` | request_changes: 1 P1, 4 P2, 4 P3 | 7172195884 |
| 2 | `d912d769`, 171 s, `ma_thoat` 0 | `68a00ea6cc76c02c212ae9b2cf87c7baef576b04` | approve; F1–F8 đóng, F9 + G1 (P3) mở | 7172333810 |
| 3 | 118 s, `ma_thoat` 0 | `a2cac7b88594d36fe80865e7bfb709a208766b7e` | approve; G1 đóng, F9 (P3) mở | 7172402264 |
| 4 | 55 s, `ma_thoat` 0 | `6c53bda1cc791fd65892a077da79e7f78582435e` | approve; F9 đóng, 0 finding mở | 7172446447 |

## Finding và cách đóng (reviewer xác nhận ở lượt kế)
- F1 P1 `awk` so SHA kiểu số ⇒ so chuỗi `"sha:"`; ca SHA toàn chữ số. F2 P2 ca tag `other/luu-tru/x`.
- F3 P2 `git` giả xoá theo đích refspec; ca đếm đích. F4 P2 ca compare lỗi + tag giữ ⇒ QUA.
- F5 P2 `GIA_SHA_MAP`, ca hai ref đo từng cặp ghim. F6/F7 P3 đo dòng `cho phép` và đường `Merge vào`.
- F8 P3 đột biến bỏ `local ds` TƯƠNG ĐƯƠNG (hàm chỉ chạy trong `$(...)`), không đổi mã.
- F9 P3 câu "tag tên thường" trong `CLAUDE.md` (3 lần sửa). G1 P3 `git` giả khớp git thật; xoá theo nguyên tên.

## Đo trên head cuối `6c53bda`
- `bash ops/don_ref_chot_test.sh` ⇒ `don_ref: 149/149` (nền `c289a17`: 105/105; bộ test mới trên workflow nền: 118/134 ⇒ ca mới
  đỏ đúng chỗ "chưa làm", ca xoá tag tên thường đạt ở cả hai).
- 21/21 đột biến (M1–M14 của executor, R1–R7 dựng từ finding) giết đúng ca đích; reviewer chạy lại và đọc từng ca đỏ.
- `actionlint` (có `shellcheck`) delta 0 so nền (cùng một `SC1003` có sẵn); `doctrine-scan` rc 0; `doc-claims-check --strict` ok.
- Kích thước: 5 tệp code+hồ sơ, 417 dòng thêm trước tệp này (trần `ADR-0053`: 6 tệp, 450).
- Chưa đo được: API GitHub thật (phân trang, tag chú giải) và thử khô sau land trên `ops/wp1475-r1-g1-lease`.

KET_LUAN: approve
