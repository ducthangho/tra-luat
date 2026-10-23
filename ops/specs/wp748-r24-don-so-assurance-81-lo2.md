# WP748 r24/g24 — dọn sổ reviewer assurance §8.1, lô 2: 18 hồ sơ land `landed: true` chưa đạt assurance

## Thẩm quyền và nguồn gốc

Chủ kho cấp packet ở https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6365380273 (OWNER, 2026-10-23T12:55:59Z).
Executor: Claude Code (`anthropic_claude`, `claude_code`, remote Linux). Reviewer: phiên Codex độc lập chỉ đọc qua
`launcher.py run`, neo đúng head cuối. Review Class `sensitive`. Base `origin/master`
`1d7e642092fb3dda15967be44d095f37bb22ac5f` (tree `2317bd9813c49448bf0739412af06284dcdf59c8`).

Nguồn lớp lỗi: cùng lớp đã sửa ở r23 (PR #882, hồ sơ `ops/land/pr882-wp748-r23-land-evidence.yaml` qua PR #885).
Biên nhận `launcher.py run` (`run.json`) không có khoá model phục vụ, connector Codex cũng không lộ model ⇒ họ model reviewer
`khong_do_duoc` (`docs/PROTOCOL_DA_PHIEN.md` §8); §8.1: "Evidence fallback hoặc không đủ nhận dạng thì chưa nhận assurance".
Phân loại 29 hồ sơ `landed: true` trên `1d7e642` (agent chỉ đọc, 23-10-2026): 18 GAP, 11 UNCLEAR, 0 OK sạch.

## Phán quyết của chủ kho (trong comment uỷ quyền)

`human_audited` được chấp nhận khi comment do chủ kho đăng, neo đúng merged head, đăng trước merge, có câu "tôi tự đọc diff"
và bản lưu đầy đủ trong kho. Các hồ sơ pr689, pr701, pr703, pr707, pr718 giữ nguyên trong lô này; pr666, pr680, pr714,
pr732, pr765, pr778 để packet sau. Hai nhóm ấy KHÔNG thuộc write set.

## Write set hiệu lực (18 tệp)

Lô A — họ model reviewer `khong_do_duoc` (bằng chứng chỉ có `run.json` không khoá model, hoặc connector Codex):
1. `ops/land/pr679-wp678-land-evidence.yaml`
2. `ops/land/pr779-wp775-land-evidence.yaml`
3. `ops/land/pr791-wp782-land-evidence.yaml`
4. `ops/land/pr792-wp484-land-evidence.yaml`
5. `ops/land/pr793-wp784-land-evidence.yaml`
6. `ops/land/pr800-wp794-land-evidence.yaml`
7. `ops/land/pr801-wp795-land-evidence.yaml`
8. `ops/land/pr818-wp788-land-evidence.yaml`
9. `ops/land/pr823-wp802-land-evidence.yaml`
10. `ops/land/pr832-wp831-land-evidence.yaml`
11. `ops/land/pr836-wp812-land-evidence.yaml`
12. `ops/land/pr848-wp744-land-evidence.yaml`
13. `ops/land/pr864-wp858-land-evidence.yaml`
14. `ops/land/pr873-wp868-land-evidence.yaml`

Lô B — human audit không đạt §8 mục 2:
15. `ops/land/pr621-skill-bai-hoc-land-evidence.yaml` (hồ sơ tự khai chưa đạt; chủ kho chấp nhận thay cho audit)
16. `ops/land/pr672-wp574-land-evidence.yaml` (audit neo `76f199e`, merged head `a602a38`; thân comment không được lưu)
17. `ops/land/pr696-wp668-land-evidence.yaml` (audit neo `cc78b33`, merged head `3ddda02`; thân theo mẫu, không câu tự đọc)
18. `ops/land/pr721-wp698-land-evidence.yaml` (thân comment không có câu tự đọc spec/diff)

Không đụng thư mục provenance nào.

## Trần kích thước (ADR-0053) — `nang_tran`

Khai nguyên văn từ comment uỷ quyền: `ai_nang: ducthangho (chủ kho)` · `can_cu: cùng một thay đổi cơ học trên 18 hồ sơ độc
lập; tách thành 3 packet chỉ nhân ba số lượt review mà không giảm rủi ro` · `tran_cu: ≤ 6 tệp / ≤ 450 dòng thêm` ·
`tran_moi: ≤ 18 tệp / ≤ 450 dòng thêm`. Executor đo `git diff --numstat` trên head cuối và báo trong PR.

## Thay đổi (mỗi tệp)

- `landed: true` → `landed: false`.
- Thêm điều kiện assurance §8.1 **CHƯA ĐẠT** kèm lý do cụ thể của hồ sơ đó (lô A: biên nhận nào, thiếu khoá model;
  lô B: mục §8-2 nào không đạt), dẫn `file:line` hoặc tệp provenance đã có trên master.
- Ghi chú (không mở rộng phạm vi, không sửa dữ kiện) các lỗ đã thấy: gate trên đúng merge SHA đỏ (pr823 `dfe5437`,
  pr836 `f1979a5`); SHA được duyệt khác merged head (pr672, pr696, pr792); verdict Codex cuối không phải approve (pr864);
  thiếu biên nhận Codex (pr791, pr793, pr800, pr801).
- Điều kiện mở lại theo khuôn pr846/pr882: (A) `cross_approved` — một lần approve độc lập đã hoàn tất trên ĐÚNG authorized
  head, họ model reviewer phục vụ được xác lập khác `claude` cho CHÍNH lần chạy ấy bằng `do_may`, hoặc `khai_co_audit` kèm
  xác nhận bền của auditor có tên và tự khai yếu hơn `do_may`; cùng họ thì không thành `cross_approved`; HOẶC (B)
  `human_audited` đầy đủ §8 mục 2 trên đúng authorized head. Hồ sơ có gate merge SHA đỏ hoặc head lệch thì điều kiện mở lại
  phải kèm cả lỗ ấy.
- Giữ nguyên mọi dữ kiện đã đo và lịch sử; kết luận cũ `landed: true` được ghi là lịch sử, không xoá.

## Chấp nhận

- `python3 ops/land_evidence_nguon.py --root .` 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC; YAML parse được; quét bí mật sạch; không CR lẻ.
- Không tệp nào ngoài write set đổi; mỗi hồ sơ trong write set có `landed: false`.
- CI xanh trên head cuối.
- Codex review qua `launcher.py run` trên head cuối: 0 P0/P1/P2.
- Chủ kho duyệt lần cuối trên SHA cụ thể trước merge.

## Dừng

Dừng và báo khi: người giữ chồng lấn, cần ghi ngoài write set, cổng `land_evidence_nguon` đòi sửa tệp ngoài write set,
một hồ sơ hoá ra có assurance hợp lệ (khi ấy giữ nguyên và báo), hoặc thiếu bằng chứng dương.
